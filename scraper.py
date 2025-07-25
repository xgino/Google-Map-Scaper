from playwright.sync_api import sync_playwright
import pandas as pd
import os
import logging
import time
import random
from tqdm import tqdm

class GoogleMapsScraper:
    def __init__(self, output_file="./data/data.csv", proxy_file="socks5.txt"):
        self.output_file = output_file
        self.proxy_file = proxy_file
        self._prepare_output()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    
    def _load_and_get_proxy(self):
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
        """Load keywords from the .txt file."""
        with open(self.keyword_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def _save_remaining_keywords(self, keywords):
        """Save the remaining keywords back to the .txt file."""
        with open(self.keyword_file, "w", encoding="utf-8") as f:
            f.write("\n".join(keywords))

    def _prepare_output(self):
        if not os.path.exists(self.output_file):
            pd.DataFrame(columns=["name", "adres", "website", "telefoon", "reviews_count", "reviews_average", "latitude", "longitude", "search_keyword"]).to_csv(self.output_file, index=False)

    def _extract_coordinates(self, url):
        try:
            # Ensure the URL contains the '@' delimiter before splitting
            if "/@" in url:
                coords = url.split("/@")[-1].split("/")[0].split(",")
                if len(coords) >= 2:
                    lat, lng = coords[0].strip(), coords[1].strip()
                    return float(lat), float(lng)
            #logging.warning(f"Invalid URL structure for extracting coordinates: {url}")
        except ValueError as ve:
            pass
            #logging.warning(f"Error converting coordinates to float: {ve} (URL: {url})")
        except Exception as e:
            pass
            #logging.warning(f"Unexpected error extracting coordinates: {e} (URL: {url})")
        return None, None

    def _accept_cookies(self, page):
        """
        Look for and click the 'Accept Cookies' button using text or specific class name.

        Args:
            page: The Playwright page object.

        Returns:
            bool: True if a cookie button was found and clicked, False otherwise.
        """
        # List of words to match text-based cookie banners
        cookie_words = [
            "Accepteren", "Akkoord", "Cookies Accepteren", "Accept Cookies", 
            "Allow Cookies", "Agree", "OK", "I Agree", "Accept All"
        ]
        
        # Check for buttons based on text
        for word in cookie_words:
            try:
                button = page.locator(f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{word.lower()}')]")
                if button.count() > 0:
                    button.first.click()
                    page.wait_for_timeout(1000)  # Wait for any overlay to disappear
                    #logging.info(f"Clicked cookie button with text: {word}")
                    return True
            except Exception as e:
                logging.debug(f"Failed to click cookie button for word '{word}': {e}")

        # Check for buttons using specific class name
        try:
            button = page.locator('//button[contains(@class, "VfPpkd-LgbsSe")]')
            if button.count() > 0:
                button.first.click()
                page.wait_for_timeout(1000)  # Wait for any overlay to disappear
                #logging.info("Clicked cookie button with specific class name.")
                return True
        except Exception as e:
            logging.debug(f"Failed to click cookie button by class name: {e}")

        logging.info("No cookie acceptance button found.")
        return False

    def _scrape_details(self, page):
        try:
            timeout = 1500  # 1.5 second timeout for checks

            # Helper function to check visibility, enabled state, and get text content
            def get_text(locator, strip=True, slice_after=None):
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

            def get_phone_number():
                from urllib.parse import unquote
                # First try the known button path
                try:
                    phone_locator = page.locator('//button[contains(@data-item-id, "phone")]//div')
                    if phone_locator.is_visible(timeout=timeout):
                        phone_text = phone_locator.text_content(timeout=timeout).strip()
                        if phone_text:
                            return phone_text
                except Exception:
                    pass

                # Fallback: search for tel: links
                try:
                    tel_link = page.locator('a[href^="tel:"]').first
                    if tel_link.is_visible(timeout=timeout):
                        href = tel_link.get_attribute('href', timeout=timeout)
                        if href:
                            return unquote(href.replace('tel:', ''))
                except Exception:
                    pass

                return "N/A"

            # Scrape all data with fallback to defaults
            name = get_text(page.locator('h1.DUwDvf.lfPIob')) or "Unknown"
            adres = get_text(page.locator('//button[@data-item-id="address"]//div'), slice_after=1) or "N/A"
            website = get_text(page.locator('div.rogA2c.ITvuef')) or "N/A"
            telefoon = get_phone_number()

            # Reviews Average
            avg_review = 0.0
            try:
                avg_review_locator = page.locator('div.F7nice span').nth(0)
                if avg_review_locator.is_visible(timeout=timeout) and avg_review_locator.is_enabled(timeout=timeout):
                    avg_review = float(avg_review_locator.text_content(timeout=timeout).replace(",", "."))
            except Exception:
                pass

            # Total Reviews
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

            # Extract coordinates from the URL
            latitude, longitude = None, None
            try:
                latitude, longitude = self._extract_coordinates(page.url)
            except Exception:
                pass

            # Build the data dictionary
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
        self.keyword_file = f"./generate_keywords/keywords_{position}.txt"
        keywords = self._load_keywords()
        total_results = 0

        # Estimate total number of batches
        total_keywords = len(keywords)
        min_batch_size, max_batch_size = 40, 50
        estimated_batches = total_keywords // ((min_batch_size + max_batch_size) // 2) + (
            1 if total_keywords % ((min_batch_size + max_batch_size) // 2) else 0
        )

        batch_progress = tqdm(total=estimated_batches, desc=f"Scraper:{position} - Total Batches", position=position, leave=True)

        while keywords:
            # Random batch size for each iteration
            batch_size = random.randint(min_batch_size, max_batch_size)
            current_batch = keywords[:batch_size]
            keywords = keywords[batch_size:]  # Remove processed keywords

            proxy = None
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = None
                for attempt in range(7):
                    proxy = self._load_and_get_proxy()
                    try:
                        context = (
                            browser.new_context(proxy={"server": proxy})
                        )
                        #print(f"Proxy applied: {proxy}")
                        break
                    except Exception as e:
                        proxy = None
                        if context:
                            context.close()

                # Fallback to no proxy after 3 failed attempts
                if not proxy and not context:
                    context = browser.new_context()
                    #print("No proxy applied")

                
                page = browser.new_page()
                page.goto("https://www.google.com/maps", timeout=60000)
                self._accept_cookies(page)

                data_batch = []
                for keyword in current_batch:
                    #logging.info(f"Scraping keyword: {keyword}")
                    seen_websites = set()

                    try:
                        page.fill("#searchboxinput", keyword)
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(2000)

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
                                    if duplicates_found >= 5:
                                        break

                    except Exception as e:
                        pass
                        #logging.warning(f"Error processing keyword {keyword}: {e}")

                if data_batch:
                    pd.DataFrame(data_batch).to_csv(
                        self.output_file, mode="a", header=not pd.io.common.file_exists(self.output_file), index=False
                    )
                context.close()
                browser.close()

            # Update batch progress
            batch_progress.update(1)

            # Save the remaining keywords
            self._save_remaining_keywords(keywords)

        batch_progress.close()
        logging.info(f"Total results scraped: {total_results}")

        
if __name__ == "__main__":
    # Create an instance of GoogleMapsScraper with the configs
    scraper = GoogleMapsScraper()

    # Start scraping
    scraper.scrape()
