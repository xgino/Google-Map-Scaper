from playwright.sync_api import sync_playwright
import pandas as pd
import os
import logging
import time
import random
from tqdm import tqdm

class GoogleMapsScraper:
    def __init__(self, config, output_file="data.csv", proxy_file="socks5.txt"):
        self.output_file = output_file
        self.proxy_file = proxy_file
        self.keywords = self._generate_keywords(config)
        self._prepare_output()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def _generate_keywords(self, config):
        """
        Generate keyword combinations sorted by country, then place, and finally keyword.

        Returns:
            list: A list of strings in the format "country, place, keyword", first iterating 
            through all country-place-keyword combinations, followed by all place-keyword-country 
            combinations.
        """
        countries = config.get("countries", [])
        places = config.get("places", [])
        keyword_list = config.get("keywords", [])

        # Generate country-first and place-first combinations
        keywords = (
            [f"{c}, {p}, {k}" for c in countries for p in places for k in keyword_list] +
            [f"{c}, {p}, {k}" for p in places for k in keyword_list for c in countries]
        )
        logging.info(f"Loaded {len(keywords)} keyword combinations.")
        return keywords
    
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

    def _prepare_output(self):
        if not os.path.exists(self.output_file):
            pd.DataFrame(columns=["name", "adres", "website", "telefoon", "reviews_count", "reviews_average", "latitude", "longitude"]).to_csv(self.output_file, index=False)

    def _extract_coordinates(self, url):
        try:
            coords = url.split("/@")[-1].split("/")[0].split(",")
            return float(coords[0]), float(coords[1])
        except Exception as e:
            logging.warning(f"Error extracting coordinates: {e}")
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
                    logging.info(f"Clicked cookie button with text: {word}")
                    return True
            except Exception as e:
                logging.debug(f"Failed to click cookie button for word '{word}': {e}")

        # Check for buttons using specific class name
        try:
            button = page.locator('//button[contains(@class, "VfPpkd-LgbsSe")]')
            if button.count() > 0:
                button.first.click()
                page.wait_for_timeout(1000)  # Wait for any overlay to disappear
                logging.info("Clicked cookie button with specific class name.")
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

            # Scrape all data with fallback to defaults
            name = get_text(page.locator('h1.DUwDvf.lfPIob')) or "Unknown"
            adres = get_text(page.locator('//button[@data-item-id="address"]//div'), slice_after=1) or "N/A"
            website = get_text(page.locator('div.rogA2c.ITvuef')) or "N/A"
            telefoon = get_text(page.locator('//button[contains(@data-item-id, "phone:tel:")]//div'), slice_after=1) or "N/A"

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
        total_results = 0
        proxy = self._load_and_get_proxy()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # Check if a proxy is applied and create a browser context accordingly
            if proxy:
                # https://github.com/TheSpeedX/PROXY-List
                context = browser.new_context(proxy={'server': proxy})
                print(f"Proxy applied: {proxy}")
            else:
                context = browser.new_context()
                print("No proxy applied")

            page = browser.new_page()
            page.goto("https://www.google.com/maps", timeout=60000)
            self._accept_cookies(page)

            for keyword in tqdm(self.keywords, desc=f"Scraper {position}", position=position, leave=True):

                logging.info(f"Scraping keyword: {keyword}")
                
                # Reset memory for the new keyword
                seen_websites = set()
                data_batch = []

                page.fill("#searchboxinput", keyword)
                page.keyboard.press("Enter")
                page.wait_for_timeout(2000)

                duplicates_found = 0  # Counter for consecutive duplicates
                break_outer = False  # Flag to break out of the keyword loop

                while True:
                    links = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]')

                    for i in range(links.count()):
                        try:
                            link = links.nth(i)
                            if link.is_visible() and link.is_enabled():  # Check visibility and actionability
                                link.click()
                                page.wait_for_load_state("domcontentloaded")  # Wait for content to load

                                data = self._scrape_details(page)
                                if data:
                                    if data['website'] in seen_websites:
                                        duplicates_found += 1
                                    else:
                                        data['search_keyword'] = keyword  # Add the search keyword to the data
                                        seen_websites.add(data['website'])
                                        data_batch.append(data)
                                        total_results += 1
                                        duplicates_found = 0  # Reset duplicate counter
                                        time.sleep(random.uniform(0.5, 1.5))

                                    # Break the loop if 5 consecutive duplicates are found
                                    if duplicates_found >= 5:
                                        logging.info("5 consecutive duplicates found. Moving to next keyword.")
                                        break_outer = True
                                        break

                        except Exception as e:
                            logging.warning(f"Error processing link: {e}")

                    if break_outer or links.count() == 0:
                        break

                # Write batch data to CSV after each keyword
                if data_batch:
                    pd.DataFrame(data_batch).to_csv(
                        self.output_file, mode="a", header=not pd.io.common.file_exists(self.output_file), index=False
                    )
                    data_batch.clear()  # Clear batch after writing

            browser.close()

        logging.info(f"Total results scraped: {total_results}")
        
if __name__ == "__main__":
    # Load custom keywords dynamically
    configs = {
        "countries": ["Nederland"],
        "places": [
            'Wijk 00 Urk', 'Wijk 22 Stadshagen', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noordoost', 'Wijk 54 Barneveld'
        ],
        "keywords": ["marketing", "e commerce", "social media"]
    }

    # Create an instance of GoogleMapsScraper with the configs
    scraper = GoogleMapsScraper(config=configs)

    # Start scraping
    scraper.scrape()
