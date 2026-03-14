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
                "reviews_count", "reviews_average", "category",
                "latitude", "longitude", "google_maps_url", "search_keyword",
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

        All fields are extracted in a single page.evaluate() call to guarantee
        consistency — every value comes from the same DOM snapshot, preventing
        stale data from a previous listing bleeding into the current one.

        Args:
            page: The Playwright ``Page`` object positioned on a place detail
                  panel.

        Returns:
            dict | None: A dictionary with keys ``name``, ``adres``,
            ``website``, ``telefoon``, ``reviews_count``, ``reviews_average``,
            ``category``, ``latitude``, ``longitude``, ``Maps_url``.
            Returns ``None`` on complete failure.
        """
        try:
            # Scroll the detail panel to trigger lazy-loaded content
            try:
                panel = page.locator('div[role="main"]')
                if panel.count() > 0:
                    panel.first.evaluate('el => el.scrollTop = el.scrollHeight')
                    page.wait_for_timeout(500)
                    panel.first.evaluate('el => el.scrollTop = 0')
                    page.wait_for_timeout(300)
            except Exception:
                pass

            # Single atomic DOM read — all fields extracted in one JS call
            data = page.evaluate(r'''() => {
                const result = {
                    name: "N/A",
                    adres: "N/A",
                    website: "N/A",
                    telefoon: "N/A",
                    reviews_count: 0,
                    reviews_average: 0.0,
                    category: "N/A",
                };
                
                // Enhanced helper to handle text like "4,1(79)" or "79 reviews"
                const extractReviewCountFromXPath = (xpath) => {
                    try {
                        const node = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (node && node.textContent) {
                            const text = node.textContent.trim();
                            
                            // 1. Look for a number inside parentheses: "(79)" or "(1.234)"
                            const parenMatch = text.match(/\(([\d.,]+)\)/);
                            if (parenMatch) {
                                const cleanNum = parseInt(parenMatch[1].replace(/[.,]/g, ''), 10);
                                if (!isNaN(cleanNum)) return cleanNum;
                            }
                            
                            // 2. Look for a number followed by "reviews": "79 reviews"
                            const textMatch = text.match(/^([\d.,]+)\s*(review|recensie|reseña)/i);
                            if (textMatch) {
                                const cleanNum = parseInt(textMatch[1].replace(/[.,]/g, ''), 10);
                                if (!isNaN(cleanNum)) return cleanNum;
                            }
                            
                            // 3. Last resort fallback: just grab the numbers
                            const fallbackMatch = text.match(/([\d.,]+)/);
                            if (fallbackMatch) {
                                const cleanNum = parseInt(fallbackMatch[1].replace(/[.,]/g, ''), 10);
                                if (!isNaN(cleanNum)) return cleanNum;
                            }
                        }
                    } catch (e) {}
                    return 0;
                };

                // ===== NAME =====
                const h1 = document.querySelector("h1.DUwDvf.lfPIob");
                if (h1) {
                    const text = h1.textContent.trim();
                    if (text) result.name = text;
                }
                if (result.name === "N/A") {
                    const title = document.title || "";
                    if (title.includes(" - Google Maps")) {
                        result.name = title.replace(" - Google Maps", "").trim();
                    }
                }

                // ===== ADDRESS =====
                const addrBtn = document.querySelector('button[data-item-id="address"]');
                if (addrBtn) {
                    const io = addrBtn.querySelector('div.Io6YTe');
                    if (io) {
                        result.adres = io.textContent.trim();
                    } else {
                        const div = addrBtn.querySelector("div");
                        if (div) result.adres = div.textContent.trim();
                    }
                }
                if (result.adres === "N/A") {
                    const span = document.querySelector("span.LrzXr");
                    if (span) result.adres = span.textContent.trim();
                }

                // ===== WEBSITE =====
                const wsLink = document.querySelector('a[data-item-id="authority"]')
                    || document.querySelector('a[aria-label*="Website"]')
                    || document.querySelector('a[aria-label*="website"]');
                if (wsLink) {
                    const href = wsLink.getAttribute("href");
                    if (href) result.website = href.trim();
                }
                if (result.website === "N/A") {
                    const wsDiv = document.querySelector("div.rogA2c.ITvuef");
                    if (wsDiv) result.website = wsDiv.textContent.trim();
                }

                // ===== PHONE =====
                const phoneBtn = document.querySelector('button[data-item-id^="phone"]');
                if (phoneBtn) {
                    const io = phoneBtn.querySelector("div.Io6YTe");
                    if (io) {
                        result.telefoon = io.textContent.trim();
                    } else {
                        const div = phoneBtn.querySelector("div");
                        if (div) result.telefoon = div.textContent.trim();
                    }
                }
                if (result.telefoon === "N/A") {
                    const tel = document.querySelector('a[href^="tel:"]');
                    if (tel) {
                        const href = tel.getAttribute("href") || "";
                        result.telefoon = decodeURIComponent(href.replace("tel:", ""));
                    }
                }

                // ===== REVIEWS =====
                
                // Helper to clean and parse numbers like "1.248" or "1,248"
                const parseReviewCount = (str) => {
                    const cleanStr = str.replace(/[.,]/g, ''); // strip dots and commas
                    const num = parseInt(cleanStr, 10);
                    return isNaN(num) ? 0 : num;
                };

                // Strategy 1: Proximity. Look inside the known rating container
                const f7 = document.querySelector("div.F7nice");
                if (f7) {
                    // Extract Average
                    const avgSpan = f7.querySelector("span[aria-hidden='true']") || f7.querySelector("span");
                    if (avgSpan) {
                        const avgText = avgSpan.textContent.trim().replace(",", ".");
                        const avgNum = parseFloat(avgText);
                        if (!isNaN(avgNum) && avgNum > 0 && avgNum <= 5) {
                            result.reviews_average = avgNum;
                        }
                    }

                    // Extract Count from the whole container's text
                    const fullText = f7.textContent;
                    // Look for "(1.248)" OR "1.248 reviews"
                    const countMatch = fullText.match(/\(([\d.,]+)\)/) || fullText.match(/([\d.,]+)\s*(review|recensie|reseña)/i);
                    if (countMatch) {
                        result.reviews_count = parseReviewCount(countMatch[1]);
                    }
                }

                // Strategy 2: Accessibility labels (Highly reliable fallback)
                if (result.reviews_count === 0) {
                    const reviewElements = document.querySelectorAll('[aria-label*="review" i], [aria-label*="recensie" i]');
                    for (const el of reviewElements) {
                        const label = el.getAttribute('aria-label');
                        const match = label.match(/([\d.,]+)\s*(review|recensie)/i);
                        if (match) {
                            result.reviews_count = parseReviewCount(match[1]);
                            break;
                        }
                    }
                }

                // Strategy 3: Target the exact span structure you found
                if (result.reviews_count === 0) {
                    const spans = document.querySelectorAll('span');
                    for (const span of spans) {
                        const text = span.textContent.trim();
                        // Matches exactly "1.248 reviews" or "1,248 recensies"
                        const match = text.match(/^([\d.,]+)\s*(reviews|recensies|reseñas)$/i);
                        if (match) {
                            result.reviews_count = parseReviewCount(match[1]);
                            break;
                        }
                    }
                } 
                                                                

                // ===== CATEGORY =====
                const catBtn = document.querySelector("button.DkEaL");
                if (catBtn) {
                    result.category = catBtn.textContent.trim();
                } else {
                    const catSpan = document.querySelector("span.DkEaL");
                    if (catSpan) {
                        result.category = catSpan.textContent.trim();
                    }
                }
                // Fallback: sibling after the rating line
                if (result.category === "N/A" && f7 && f7.parentElement) {
                    const parent = f7.parentElement.parentElement;
                    if (parent) {
                        const last = parent.children[parent.children.length - 1];
                        if (last) {
                            const text = last.textContent.trim();
                            if (text && !text.match(/^[\d.,()]+$/)) {
                                result.category = text;
                            }
                        }
                    }
                }

                return result;
            }''')

            if not data or data.get("name") == "N/A":
                return None

            # Coordinates from the browser URL (can't do this in JS due to SPA routing)
            latitude, longitude = self._extract_coordinates(page.url)

            data["latitude"] = latitude
            data["longitude"] = longitude
            data["google_maps_url"] = page.url

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
                                old_url = page.url
                                old_name = page.locator('h1.DUwDvf.lfPIob').text_content() if page.locator('h1.DUwDvf.lfPIob').count() > 0 else ""
                                link.click()
                                try:
                                    page.wait_for_function(
                                        r'''(args) => {
                                            const [oldUrl, oldName] = args;
                                            const urlChanged = window.location.href !== oldUrl;
                                            const h1 = document.querySelector("h1.DUwDvf.lfPIob");
                                            const nameChanged = h1 && h1.textContent.trim() !== oldName.trim();
                                            const reviewsLoaded = document.querySelector('div.F7nice')
                                                || document.querySelector('div.HHrUdb');
                                            return urlChanged && nameChanged && reviewsLoaded;
                                        }''',
                                        [old_url, old_name],
                                        timeout=5000,
                                    )
                                    page.wait_for_timeout(500)
                                except Exception:
                                    page.wait_for_timeout(2500)  # fallback: just wait
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