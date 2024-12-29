# Google Maps Business Scraper  

The **Google Maps Business Scraper** is a powerful and reliable **Python-based tool** for extracting detailed business information directly from Google Maps. Designed with performance and scalability in mind, it offers a robust solution for data scraping needs.  

Built for efficiency, this scraper is ideal for **targeting specific locations and categories**, making it perfect for businesses, researchers, and data analysts seeking actionable insights.  

## Why Choose This Scraper?  
- **Reliable Data Scraping**: Handles large-scale data extraction seamlessly.  
- **Efficient and Robust**: Built for continuous operation with minimal errors.  
- **Terminal-Friendly**: Easily operate the scraper directly from your terminal.  

Whether you need to build a comprehensive business database or analyze market trends, this tool delivers **accurate, scalable, and efficient results**.  

**Example Use Cases**:  
- Building business contact lists for marketing.  
- Collecting geospatial data for research or analysis.  
- Generating location-based insights for decision-making.  
---

## Features

1. **Proxy Rotation**: Rotate proxies to **prevent IP blocks** and keep scraping uninterrupted.  
2. **Keyword Generation**: Optimize keywords for **maximum data collection** by making them as detailed as possible.  
3. **Headless Scraping**: Saves RAM, handles cookie acceptance, and works seamlessly via the terminal.  
4. **Batch Processing**: Process in **batches** instead of items to save RAM and improve efficiency.  
5. **Automatic Browser Restart**: Closes and starts a **new browser with a fresh proxy** after each batch to optimize RAM usage.  
6. **Detailed Data Extraction**: Extracts more **comprehensive data from Google Maps** (details below).  
7. **Progress Tracking**: Added progress feedback to make the terminal less boring—no dancing cat, unfortunately.  
8. **Duplicate Prevention**: Avoids duplicate saves by **tracking current batch items** in memory.  
   - **Note**: Multiprocessing may still cause duplicates if keywords overlap; future work involves improving this with a `drop_duplicates` approach.  
9. **Timeouts and Fallbacks**: Respects servers by **timing out to avoid overloads** and maintains continuous scraping despite errors.  
10. **Resume with Keywords**: Uses `keywords.txt` to **resume from where you left off**.  
    - Unused keywords stay in the file, so you can pick up where you stopped—even for a mid-bathroom break emergency.  
11. **Continuous Data Appending**: Appends new data to an **existing CSV**, ensuring a continuously growing dataset.  

---

## Instructions

1. **Python Version**: Use Python 3.12 (older versions may work, but not guaranteed).
2. **Install Dependencies**:  
   - Clone the repo:  
     ```bash
     git clone https://github.com/xgino/Google-Map-Scaper.git
     cd google-maps-scraper  
     ```
   - Install required Python packages:  
     ```bash
     pip install -r requirements.txt  
     ```
   - Install Playwright for browser automation:  
     ```bash
     pip install playwright  
     playwright install  
     ```

3. **Prepare Files**:  
   - `socks5.txt`: Proxy list (from [TheSpeedX Proxy List](https://github.com/TheSpeedX/PROXY-List)).
   - `generate_keywords.py`: Generate keywords based on location and category (e.g., "Netherlands", "Amsterdam", "Restaurant").
   - `get_region.py`: Get region data for your country (modify based on your country’s data).
   - `keyword_{i}.txt`: Remaining keywords for scraping.

4. **Run the Scraper**:
   - First, run `get_regions.py` to generate `regions.txt`.
   - Then, copy `regions.txt` into `generate_keywords.py` and run it to create keyword files (e.g., `keyword_1.txt`).
   - Finally, run `main.py` to start scraping.

---

## Credits
- Proxy list sourced from [TheSpeedX/PROXY-List](https://github.com/TheSpeedX/PROXY-List).
- All other code was written from scratch, taking an entire week. Feel free to use it. If you find it useful, consider donating via [Ko-Fi](https://ko-fi.com/xgino) to fuel my next coding session.  ## Instructions


## Scraper Output  
The scraped data is saved in `./data/data.csv` with the following columns:

- **name**: Business name
- **address**: Business address
- **website**: Business website
- **phone**: Phone number
- **reviews_count**: Number of reviews
- **reviews_average**: Average review rating
- **latitude**: Latitude of the business
- **longitude**: Longitude of the business
- **search_keyword**: Keyword used for search

---

## Notes
- **System Requirements**: Tested with Python 3.12 and 16GB RAM. If using lower configurations, adjust the number of processes accordingly.
- **Proxy Rotation**: Ensure that the `socks5.txt` file contains valid, up-to-date proxies.
---

## Limitations
- **Hardware Requirements**: Performance and multiprocessing capabilities depend on the hardware; more processes require more system resources.
- **Google Maps Infrastructure**: The scraper relies on Google Maps’ infrastructure; any changes to the site may cause the scraper to break.
- **Coordinate Availability**: Coordinates may not always be provided by Google Maps, depending on the data available for the business.
- **Proxy Maintenance**: The proxy list (`socks5.txt`) needs to be manually updated to ensure functionality.

---

## Support  
If you find this useful, please consider supporting me by getting me a coffee on [Ko-fi](https://ko-fi.com/xgino). Every sip helps fuel a new line of code. Thank you for your support, and keep coding!
