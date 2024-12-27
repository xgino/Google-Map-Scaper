from playwright.sync_api import sync_playwright
import pandas as pd
import os
import logging
import time
import random
from tqdm import tqdm

class GoogleMapsScraper:
    def __init__(self, output_file="data.csv"):
        self.output_file = output_file
        self.keywords = self._load_keywords()
        self._prepare_output()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def _load_keywords(self):
        # List of countries
        countries = ["Nederland"]
        # List of places (cities and locations)
        places = ['Kampen', 'Wijk 01 Emmeloord', 'Raalte', 'Wijk 00 Urk', 'Wijk 22 Stadshagen', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noordoost', 'Wijk 54 Barneveld', 'Beuningen', 'Culemborg Oost', 'Ede-West', 'Wijk 00 Epe', 'Schil rondom het centrum', 'Nijkerk-stad', 'Nijmegen-Oost', 'Nijmegen-Oud-West', 'Nijmegen-Nieuw-West', 'Nijmegen-Midden', 'Nijmegen-Zuid', 'Dukenburg', 'Nijmegen-Noord', 'Wijk 00 Putten', 'Wijk 00 Dieren', 'Wijk 02 Velp', 'Tiel kern', 'Wijk 01 Twello-Nijbroek', 'Wijk 00 Stad', 'Wijk 01 Wijchen kern', 'Zevenaar', 'Wijk 00 Nunspeet', 'Wijk 00', 'Wijk 01 West', 'Wijk 02 Noordwest', 'Wijk 03 Overvecht', 'Wijk 04 Noordoost', 'Wijk 05 Oost', 'Wijk 06 Binnenstad', 'Wijk 07 Zuid', 'Wijk 08 Zuidwest', 'Wijk 09 Leidsche Rijn', 'Wijk 10 Vleuten-De Meern', 'Wijk 00 Wijk bij Duurstede', 'Wijk 00 IJsselstein', 'Zeist Centrum', 'Zeist-Noord', 'Zuid', 'De Mare', 'Jordaan', 'Oostelijke Eilanden/Kadijken', 'Landlust', 'Staatsliedenbuurt', 'Geuzenveld', 'Osdorp-Oost', 'Westlandgracht', 'Museumkwartier', 'Oude Pijp', 'Nieuwe Pijp', 'Scheldebuurt', 'Buitenveldert-West', 'Oostelijk Havengebied', 'Frankendael', 'Middenmeer', 'Wijk 02 Volendam', 'Oude Stad', 'Hoofddorp', 'Nieuw-Vennep', 'Wijk 00 Heemstede-Centrum', 'Zuid', 'Oost', 'Wijk 33 Kersenboogerd-Zuid', 'Wijk 02 Overwhere', 'Wijk 07 Weidevenne', 'Kerk en Zanen', 'Boskoop', 'Wijk 11 Binnenstad', 'Wijk 24 Voorhof', 'Wijk 25 Buitenhof', 'Wijk 28 Wippolder', 'Wijk 09 Sterrenburg', 'Wijk 11 Stadspolders', 'Wijk 04 Benoordenhout', 'Wijk 07 Scheveningen', 'Wijk 09 Geuzen- en Statenkwartier', 'Wijk 12 Bomen- en Bloemenbuurt', 'Wijk 17 Loosduinen', 'Wijk 18 Waldeck', 'Wijk 20 Valkenboskwartier', 'Wijk 21 Regentessekwartier', 'Wijk 25 Mariahoeve en Marlot', 'Wijk 26 Bezuidenhout', 'Wijk 27 Stationsbuurt', 'Wijk 28 Centrum', 'Wijk 29 Schildersbuurt', 'Wijk 31 Rustenburg en Oostbroek', 'Wijk 32 Leyenburg', 'Wijk 33 Bouwlust', 'Wijk 34 Morgenstond', 'Wijk 36 Moerwijk', 'Wijk 38 Laakkwartier en Spoorwijk', 'Wijk 40 Wateringse Veld', 'Wijk 42 Ypenburg', 'Wijk 44 Leidschenveen', 'Katwijk aan Zee', 'Rijnsburg', 'Wijk 00 Krimpen aan den IJssel', 'Binnenstad-Noord', 'Leiden-Noord', 'Roodenburgerdistrict', 'Bos- en Gasthuisdistrict', 'Wijk 00', 'Noordwijk Binnen', 'Rotterdam Centrum', 'Delfshaven', 'Overschie', 'Noord', 'Hillegersberg-Schiebroek', 'Kralingen-Crooswijk', 'Feijenoord', 'IJsselmonde', 'Prins Alexander', 'Charlois', 'Hoogvliet', 'Wijk 06 Nieuwland', 'Centrum', 'Wijk 00', 'Wijk 01 Noordoostelijk deel der gemeente', 'Wijk 01 Woerden-Midden', 'Centrum', 'Meerzicht', 'Buytenwegh de Leyens', 'Seghwaert', 'Rokkeveen', 'Oosterheem', 'Wijk 01 Goes', 'Mijdrecht', 'Wijk 00 Bergen op Zoom-Oude stad en omgeving', 'Wijk 02 Bergen op Zoom-Oost', 'Wijk 00 Best', 'Wijk 00 Boxtel', 'Breda centrum', 'Breda noord', 'Breda oost', 'Breda zuid-oost', 'Breda west', 'Breda noord-west', 'Dongen', 'Putten', 'Erp', 'Ontginning', 'Aanschot', 'Oud-Strijp', 'Oud-Gestel', 'Noord woongebied', 'Rijen', 'Wijk 10 Binnenstad', 'Binnenstad', 'Zuidoost', 'Graafsepoort', 'Noord', 'Maaspoort', 'West', 'Wijk 01 Drunen', 'Wijk 05 Vlijmen', 'Wijk 00 Nuenen', 'Wijk 00 Valkenswaard', 'Wijk 00 Veldhoven', 'Wijk 00 Waalre', 'Waalwijk', 'Wijk 00 Schaesberg', 'Wijk 00 Kerkrade-West', 'Wijk 01 Kerkrade-Oost', 'Wijk 00 Centrum', 'Wijk 02 Buitenwijk West', 'Wijk 04 Buitenwijk Oost', 'Wijk 06 Buitenwijk Zuidoost', 'Driebergen', 'Wijk 00 Roden', 'Huissen', 'Steenwijk', 'Wijk 00 Zevenbergen', 'Geldrop', 'Wijk 01 Naaldwijk', "Wijk 04 's-Gravenzande", 'Wijk 01 Sittard', 'Wijk 02 Overhoven', 'Wijk 05 Geleen', 'Nieuwerkerk aan den IJssel wijk 04', 'Wijk 00 Winschoten', 'Wijk 01 Sneek', 'Wijk 01 Maarssen', 'Wijk 12 Maarssenbroek', 'Pijnacker', 'Nootdorp', 'Naarden', 'Schijndel', 'Sint-Oedenrode', 'Veghel', 'Wijk 02 Didam', 'Oud-Beijerland', 'Cuijk', 'Uden']
        
        # List of keywords for different types of businesses/places
        keywords = [
            'E-commerceservice', 'E-commercebureau',
        ]
        
        return [f"{country}, {place}, {keyword}" for country in countries for place in places for keyword in keywords]
    

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

    def _scrape_details(self, page):
        try:
            timeout = 2000  # 2 seconds timeout for each locator

            # Name Locator
            try:
                name_locator = page.locator('h1.DUwDvf.lfPIob')
                name = name_locator.text_content(timeout=timeout).strip() if name_locator.count() > 0 else "Unknown"
            except Exception:
                name = "Unknown"

            # Address Locator
            try:
                adres_locator = page.locator('//button[@data-item-id="address"]//div')
                adres = adres_locator.first.text_content(timeout=timeout).strip()[1:] if adres_locator.count() > 0 else ""
            except Exception:
                adres = ""

            # Website Locator
            try:
                website_locator = page.locator('div.rogA2c.ITvuef')
                website = website_locator.first.text_content(timeout=timeout).strip() if website_locator.count() > 0 else ""
            except Exception:
                website = ""

            # Phone Locator
            try:
                phone_locator = page.locator('//button[contains(@data-item-id, "phone:tel:")]//div')
                telefoon = phone_locator.first.text_content(timeout=timeout).strip()[1:] if phone_locator.count() > 0 else ""
            except Exception:
                telefoon = ""

            # Reviews Average
            try:
                avg_review_locator = page.locator('div.F7nice span').nth(0)
                avg_review = (
                    float(avg_review_locator.text_content(timeout=timeout).replace(",", "."))
                    if avg_review_locator.count() > 0
                    else 0.0
                )
            except Exception:
                avg_review = 0.0

            # Total Reviews
            try:
                total_reviews_locator = page.locator('div.F7nice span:nth-child(2) span span')
                total_reviews = (
                    int(
                        total_reviews_locator.text_content(timeout=timeout)
                        .replace("(", "")
                        .replace(")", "")
                        .replace(".", "")
                    )
                    if total_reviews_locator.count() > 0
                    else 0
                )
            except Exception:
                total_reviews = 0

            # Coordinates
            try:
                latitude, longitude = self._extract_coordinates(page.url)
            except Exception:
                latitude, longitude = None, None

            # Build data dictionary
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

    def scrape(self):
        total_results = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            context = browser.new_context()
            page = browser.new_page()
            page.goto("https://www.google.com/maps", timeout=60000)

            for keyword in tqdm(self.keywords):
                logging.info(f"Scraping keyword: {keyword}")
                page.fill("#searchboxinput", keyword)
                page.keyboard.press("Enter")
                page.wait_for_timeout(2000)

                while True:
                    links = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]')
                    duplicates_found = 0  # Counter for duplicate checks
                    break_outer = False  # Flag to break the outer loop

                    for i in range(links.count()):
                        try:
                            link = links.nth(i)
                            link.click()
                            page.wait_for_load_state('networkidle')

                            data = self._scrape_details(page)
                            if data:
                                df = pd.read_csv(self.output_file)

                                # Check for duplicates based on 'name' and 'website'
                                if (df['website'] == data['website']).any():
                                    #logging.info(f"Duplicate found for {data['name']}. Skipping...")
                                    duplicates_found += 1
                                else:
                                    # Append new data if no duplicates
                                    pd.DataFrame([data]).to_csv(self.output_file, mode="a", header=False, index=False)
                                    #logging.info(f"Cat:{keyword}, Append CSV: {data['name']}")
                                    total_results += 1
                                    duplicates_found = 0  # Reset duplicate counter
                                    time.sleep(random.uniform(0.5, 1.5)) # half sec or 1,5 sec

                                # Free up memory by deleting the DataFrame
                                del df

                            # If 3 consecutive duplicates found, set the flag to break the outer loop
                            if duplicates_found >= 5:
                                logging.info("5 consecutive duplicates found. Moving to next keyword.")
                                break_outer = True
                                break  # Break the inner loop

                        except Exception as e:
                            logging.warning(f"Error processing link: {e}")

                    # If flag is set to True, break the outer loop
                    if break_outer:
                        break

                    # If no more links, break out of the while loop
                    if links.count() == 0:
                        break

            browser.close()
        logging.info(f"Total results scraped: {total_results}")
        
if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    scraper.scrape()
