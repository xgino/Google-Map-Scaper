"""
Google Maps Scraper
===================

A Playwright-based scraper that searches Google Maps for business listings
using keyword files, extracts structured business data (name, address, website,
phone, reviews, coordinates), and writes results to CSV.

Features:
    - SOCKS5 proxy rotation with automatic fallback to direct connection.
    - Keyword batching with randomised batch sizes (40–50) to reduce detection.
    - Resumable scraping: unprocessed keywords are saved back to disk after
      each batch so the job can be interrupted and restarted.
    - Cookie-consent auto-dismiss for Dutch and English Google overlays.
    - Multi-selector search-box strategy to survive Google Maps DOM changes.

Directory layout expected:
    ./generate_keywords/keywords_<position>.txt   – one search query per line
    ./data/data.csv                                – output (created if missing)
    ./socks5.txt                                   – one proxy per line (ip:port)

Usage:
    python scraper.py
"""

from playwright.sync_api import sync_playwright
import pandas as pd
import os
import logging
import time
import random
from tqdm import tqdm


class GoogleMapsScraper:
    """Scrape Google Maps search results into a CSV file.

    The scraper opens a Chromium browser via Playwright, iterates over keyword
    files split by ``position`` index, and appends extracted business records
    to a shared CSV.  Proxies are rotated per batch, and each batch spawns a
    fresh browser context to keep sessions short.

    Args:
        output_file: Path to the CSV file where results are appended.
        proxy_file:  Path to a newline-delimited list of SOCKS5 proxy addresses.
    """

    def __init__(self, output_file="./data/data.csv", proxy_file="socks5.txt"):
        self.output_file = output_file
        self.proxy_file = proxy_file
        self._prepare_output()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def _load_and_get_proxy(self):
        """Read the proxy file and return a randomly chosen proxy string.

        Returns:
            A proxy address string (e.g. ``socks5://host:port``), or ``None``
            if the file is missing or empty.
        """
        try:
            with open(self.proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                raise Exception("No proxies available.")
            return random.choice(proxies)
        except (FileNotFoundError, Exception) as e:
            logging.error(f"Error loading proxy: {e}")
            return None

    def _load_keywords(self):
        """Load keywords from the .txt file.

        Reads ``self.keyword_file`` (set in :meth:`scrape`) and returns all
        non-empty lines as a list of strings.

        Returns:
            list[str]: Search keywords to process.
        """
        with open(self.keyword_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def _save_remaining_keywords(self, keywords):
        """Save the remaining keywords back to the .txt file.

        This is called after every batch so that if the process is killed,
        already-processed keywords are not repeated on the next run.

        Args:
            keywords: The list of keywords that have **not** been scraped yet.
        """
        with open(self.keyword_file, "w", encoding="utf-8") as f:
            f.write("\n".join(keywords))

    def _prepare_output(self):
        """Create the output CSV with headers if it does not already exist."""
        if not os.path.exists(self.output_file):
            pd.DataFrame(columns=[
                "name", "adres", "website", "telefoon",
                "reviews_count", "reviews_average",
                "latitude", "longitude", "search_keyword",
            ]).to_csv(self.output_file, index=False)

    def _extract_coordinates(self, url):
        """Parse latitude and longitude from a Google Maps URL.

        Google Maps encodes coordinates in the URL after the ``/@`` marker,
        e.g. ``…/@52.3676,4.9041,15z/…``.

        Args:
            url: The full browser URL of the current Maps page.

        Returns:
            tuple[float | None, float | None]: ``(latitude, longitude)`` or
            ``(None, None)`` if extraction fails.
        """
        try:
            if "/@" in url:
                coords = url.split("/@")[-1].split("/")[0].split(",")
                if len(coords) >= 2:
                    lat, lng = coords[0].strip(), coords[1].strip()
                    return float(lat), float(lng)
        except ValueError as ve:
            pass
        except Exception as e:
            pass
        return None, None

    def _accept_cookies(self, page):
        """Dismiss the Google cookie-consent overlay if present.

        Tries a list of common button labels (Dutch and English) via
        case-insensitive XPath matching, then falls back to a known Material
        Design button class.

        Args:
            page: The Playwright ``Page`` object.

        Returns:
            bool: ``True`` if a cookie button was found and clicked.
        """
        # Common accept-button labels across NL / EN Google overlays
        cookie_words = [
            "Accepteren", "Akkoord", "Cookies Accepteren", "Accept Cookies",
            "Allow Cookies", "Agree", "OK", "I Agree", "Accept All"
        ]

        # Strategy 1: match button text (case-insensitive)
        for word in cookie_words:
            try:
                button = page.locator(f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{word.lower()}')]")
                if button.count() > 0:
                    button.first.click()
                    page.wait_for_timeout(1000)
                    return True
            except Exception as e:
                logging.debug(f"Failed to click cookie button for word '{word}': {e}")

        # Strategy 2: match by Google's Material Design button class
        try:
            button = page.locator('//button[contains(@class, "VfPpkd-LgbsSe")]')
            if button.count() > 0:
                button.first.click()
                page.wait_for_timeout(1000)
                return True
        except Exception as e:
            logging.debug(f"Failed to click cookie button by class name: {e}")

        logging.info("No cookie acceptance button found.")
        return False

    def _fill_search_box(self, page, keyword):
        """Fill the Maps search box using multiple selector strategies.

        Google Maps periodically changes element IDs and class names, so this
        method tries several CSS selectors in order of reliability before
        falling back to an XPath query.

        Args:
            page:    The Playwright ``Page`` object.
            keyword: The search string to type into the box.

        Returns:
            bool: ``True`` if the search box was found and filled successfully.
        """
        # Ordered from most stable (name attr) to least stable (class name)
        selectors = [
            'input[name="q"]',
            '#searchboxinput',
            'input.UGojuc',
            'input[role="combobox"]',
        ]
        for sel in selectors:
            try:
                loc = page.locator(sel)
                if loc.is_visible(timeout=3000):
                    loc.fill(keyword)
                    return True
            except Exception:
                continue

        # Last resort: XPath
        try:
            loc = page.locator('//form//input[@name="q"]')
            if loc.is_visible(timeout=3000):
                loc.fill(keyword)
                return True
        except Exception:
            pass

        logging.warning(f"Could not find search box for keyword: {keyword}")
        return False

    def _scrape_details(self, page):
        """Extract structured business data from the currently open Maps listing.

        Each field is scraped with a primary selector and one or more fallbacks
        so the scraper degrades gracefully when Google changes the DOM.

        Args:
            page: The Playwright ``Page`` object positioned on a place detail
                  panel.

        Returns:
            dict | None: A dictionary with keys ``name``, ``adres``,
            ``website``, ``telefoon``, ``reviews_count``, ``reviews_average``,
            ``latitude``, ``longitude``.  Returns ``None`` on complete failure.
        """
        try:
            timeout = 1500  # ms – keep low to avoid stalling on missing elements

            # ----- helper -----
            def get_text(locator, strip=True, slice_after=None):
                """Safely extract text from a Playwright locator.

                Args:
                    locator:     A Playwright ``Locator`` object.
                    strip:       Whether to strip whitespace.
                    slice_after: If set, return ``text[slice_after:]``.

                Returns:
                    str | None: The extracted text, or ``None`` on failure.
                """
                try:
                    if locator.is_visible(timeout=timeout) and locator.is_enabled(timeout=timeout):
                        text = locator.text_content(timeout=timeout)
                        if strip:
                            text = text.strip()
                        if slice_after:
                            text = text[slice_after:]
                        return text
                except Exception:
                    return None

            # ----- business name -----
            def get_business_name():
                """Return the business name from the heading or the page title."""
                try:
                    name_locator = page.locator('h1.DUwDvf.lfPIob')
                    if name_locator.is_visible(timeout=timeout):
                        name = name_locator.text_content(timeout=timeout).strip()
                        if name:
                            return name
                except Exception:
                    pass
                # Fallback: parse the <title> tag (format: "Name - Google Maps")
                try:
                    title_text = page.title()
                    if " - Google Maps" in title_text:
                        return title_text.replace(" - Google Maps", "").strip()
                except Exception:
                    pass
                return "N/A"

            # ----- address -----
            def get_address():
                """Return the street address from the info panel."""
                # Primary: the shared info-row class inside the address button
                try:
                    address_locator = page.locator('//button[@data-item-id="address"]//div[contains(@class, "Io6YTe")]')
                    if address_locator.is_visible(timeout=timeout):
                        return address_locator.text_content(timeout=timeout).strip()
                except Exception:
                    pass
                # Fallback: older data-item-id selector without class filter
                try:
                    address_locator = page.locator('//button[@data-item-id="address"]//div')
                    if address_locator.is_visible(timeout=timeout):
                        return address_locator.text_content(timeout=timeout).strip()
                except Exception:
                    pass
                # Fallback: legacy span
                try:
                    address_span = page.locator('span.LrzXr')
                    if address_span.is_visible(timeout=timeout):
                        return address_span.text_content(timeout=timeout).strip()
                except Exception:
                    pass
                return "N/A"

            # ----- website -----
            def get_website():
                """Return the business website URL."""
                # Primary: anchor with data-item-id="authority"
                try:
                    website_link = page.locator('//a[@data-item-id="authority"]')
                    if website_link.is_visible(timeout=timeout):
                        href = website_link.get_attribute('href', timeout=timeout)
                        if href:
                            return href.strip()
                except Exception:
                    pass
                # Fallback: anchor with aria-label containing "Website"
                try:
                    website_link = page.locator('//a[contains(@href, "http") and contains(@aria-label, "Website")]').first
                    if website_link.is_visible(timeout=timeout):
                        href = website_link.get_attribute('href', timeout=timeout)
                        if href:
                            return href.strip()
                except Exception:
                    pass
                # Fallback: text content from the Io6YTe div inside a website link
                try:
                    website_text = page.locator('//a[@data-item-id="authority"]//div[contains(@class, "Io6YTe")]')
                    if website_text.is_visible(timeout=timeout):
                        return website_text.text_content(timeout=timeout).strip()
                except Exception:
                    pass
                # Fallback: legacy div class
                try:
                    website_div = page.locator('div.rogA2c.ITvuef')
                    if website_div.is_visible(timeout=timeout):
                        return website_div.text_content(timeout=timeout).strip()
                except Exception:
                    pass
                return "N/A"

            # ----- phone -----
            def get_phone_number():
                """Return the phone number from the info panel or a tel: link."""
                from urllib.parse import unquote
                # Primary: Io6YTe div inside the phone button
                try:
                    phone_locator = page.locator('//button[contains(@data-item-id, "phone")]//div[contains(@class, "Io6YTe")]')
                    if phone_locator.is_visible(timeout=timeout):
                        phone_text = phone_locator.text_content(timeout=timeout).strip()
                        if phone_text:
                            return phone_text
                except Exception:
                    pass
                # Fallback: older phone button selector without class filter
                try:
                    phone_locator = page.locator('//button[contains(@data-item-id, "phone")]//div')
                    if phone_locator.is_visible(timeout=timeout):
                        phone_text = phone_locator.text_content(timeout=timeout).strip()
                        if phone_text:
                            return phone_text
                except Exception:
                    pass
                # Fallback: tel: link
                try:
                    tel_link = page.locator('a[href^="tel:"]').first
                    if tel_link.is_visible(timeout=timeout):
                        href = tel_link.get_attribute('href', timeout=timeout)
                        if href:
                            return unquote(href.replace('tel:', ''))
                except Exception:
                    pass
                return "N/A"

            # ----- collect all fields -----
            name = get_business_name()
            adres = get_address()
            website = get_website()
            telefoon = get_phone_number()

            # Reviews – average star rating
            avg_review = 0.0
            try:
                # Primary: aria-hidden span with the numeric rating (e.g. "4,6")
                avg_review_locator = page.locator('span[aria-hidden="true"]').first
                if avg_review_locator.is_visible(timeout=timeout):
                    text = avg_review_locator.text_content(timeout=timeout).strip()
                    if text and text.replace(",", "").replace(".", "").isdigit():
                        avg_review = float(text.replace(",", "."))
            except Exception:
                pass
            # Fallback: original F7nice selector
            if avg_review == 0.0:
                try:
                    avg_review_locator = page.locator('div.F7nice span').nth(0)
                    if avg_review_locator.is_visible(timeout=timeout) and avg_review_locator.is_enabled(timeout=timeout):
                        avg_review = float(avg_review_locator.text_content(timeout=timeout).replace(",", "."))
                except Exception:
                    pass
            # Fallback: parse from the star-icon span's aria-label (e.g. "4,6 sterren")
            if avg_review == 0.0:
                try:
                    star_span = page.locator('span.ceNzKf[role="img"]')
                    if star_span.is_visible(timeout=timeout):
                        label = star_span.get_attribute('aria-label', timeout=timeout)
                        if label:
                            # Extract leading number from e.g. "4,6 sterren " or "4.6 stars"
                            num_str = label.split()[0].replace(",", ".")
                            avg_review = float(num_str)
                except Exception:
                    pass

            # Reviews – total count
            total_reviews = 0
            try:
                total_reviews_locator = page.locator('div.F7nice span:nth-child(2) span span')
                if total_reviews_locator.is_visible(timeout=timeout) and total_reviews_locator.is_enabled(timeout=timeout):
                    total_reviews = int(
                        total_reviews_locator.text_content(timeout=timeout)
                        .replace("(", "")
                        .replace(")", "")
                        .replace(".", "")
                    )
            except Exception:
                pass
            # Fallback: aria-label on the reviews button (e.g. "1.234 reviews")
            if total_reviews == 0:
                try:
                    reviews_btn = page.locator('//button[contains(@aria-label, "review")]')
                    if reviews_btn.is_visible(timeout=timeout):
                        label = reviews_btn.get_attribute('aria-label', timeout=timeout)
                        if label:
                            num_str = ''.join(c for c in label.split()[0] if c.isdigit())
                            if num_str:
                                total_reviews = int(num_str)
                except Exception:
                    pass

            # Coordinates from the browser URL
            latitude, longitude = None, None
            try:
                latitude, longitude = self._extract_coordinates(page.url)
            except Exception:
                pass

            data = {
                "name": name,
                "adres": adres,
                "website": website,
                "telefoon": telefoon,
                "reviews_count": total_reviews,
                "reviews_average": avg_review,
                "latitude": latitude,
                "longitude": longitude,
            }
            return data

        except Exception as e:
            logging.warning(f"Error scraping details: {e}")
            return None

    def scrape(self, position=0):
        """Run the main scraping loop.

        Loads keywords from ``./generate_keywords/keywords_<position>.txt``,
        splits them into randomised batches, and for each batch:

        1. Launches a headless Chromium browser with a random SOCKS5 proxy.
        2. Navigates to Google Maps and dismisses the cookie overlay.
        3. Searches each keyword, clicks every place link in the results, and
           extracts business details.
        4. Appends the batch results to the output CSV.
        5. Saves remaining (unprocessed) keywords back to disk.

        Duplicate listings within a single keyword search are tracked by
        website URL; scraping for that keyword stops early after 5 consecutive
        duplicates.

        Args:
            position: Index used to select the keyword file and to label the
                      tqdm progress bar (useful when running multiple scrapers
                      in parallel).
        """
        self.keyword_file = f"./generate_keywords/keywords_{position}.txt"
        keywords = self._load_keywords()
        total_results = 0

        # Estimate the number of batches for the progress bar
        total_keywords = len(keywords)
        min_batch_size, max_batch_size = 40, 50
        estimated_batches = total_keywords // ((min_batch_size + max_batch_size) // 2) + (
            1 if total_keywords % ((min_batch_size + max_batch_size) // 2) else 0
        )

        batch_progress = tqdm(total=estimated_batches, desc=f"Scraper:{position} - Total Batches", position=position, leave=True)

        while keywords:
            # Pick a random batch size to vary request patterns
            batch_size = random.randint(min_batch_size, max_batch_size)
            current_batch = keywords[:batch_size]
            keywords = keywords[batch_size:]

            proxy = None
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)

                # Attempt up to 7 proxies before falling back to direct
                context = None
                for attempt in range(7):
                    proxy = self._load_and_get_proxy()
                    try:
                        context = (
                            browser.new_context(proxy={"server": proxy})
                        )
                        break
                    except Exception as e:
                        proxy = None
                        if context:
                            context.close()

                # Fallback: no proxy
                if not proxy and not context:
                    context = browser.new_context()

                page = browser.new_page()
                page.goto("https://www.google.com/maps", timeout=60000)
                self._accept_cookies(page)

                data_batch = []  # accumulate results for the current batch

                for keyword in current_batch:
                    seen_websites = set()  # de-duplicate within a keyword

                    try:
                        # Type the keyword into the search box and submit
                        if not self._fill_search_box(page, keyword):
                            continue
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(2000)

                        # Collect all place-detail links in the results panel
                        links = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]')
                        duplicates_found = 0

                        for i in range(links.count()):
                            link = links.nth(i)
                            if link.is_visible() and link.is_enabled():
                                link.click()
                                page.wait_for_load_state("domcontentloaded")
                                data = self._scrape_details(page)
                                if data:
                                    if data["website"] not in seen_websites:
                                        seen_websites.add(data["website"])
                                        data["search_keyword"] = keyword
                                        data_batch.append(data)
                                        total_results += 1
                                    else:
                                        duplicates_found += 1
                                    # Stop early if we keep hitting duplicates
                                    if duplicates_found >= 5:
                                        break

                    except Exception as e:
                        pass

                # Flush batch to CSV
                if data_batch:
                    pd.DataFrame(data_batch).to_csv(
                        self.output_file, mode="a", header=not pd.io.common.file_exists(self.output_file), index=False
                    )
                context.close()
                browser.close()

            batch_progress.update(1)

            # Persist remaining keywords so the job is resumable
            self._save_remaining_keywords(keywords)

        batch_progress.close()
        logging.info(f"Total results scraped: {total_results}")


if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    scraper.scrape()
