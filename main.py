import os
import multiprocessing
import logging
from scraper import GoogleMapsScraper
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_scraper(tqdm_position):
    """
    Runs a scraper instance for the given keywords file.

    Args:
        tqdm_position (int): Unique tqdm position.
    """
    print(f"Starting scraper for {tqdm_position}...")
    scraper = GoogleMapsScraper()
    scraper.scrape(position=tqdm_position) 


def main():
    # Directory where keyword files are stored
    keyword_dir = "./generate_keywords"

    # Dynamically count the number of keyword files
    num_keyword_files = len([f for f in os.listdir(keyword_dir) if f.startswith("keywords_") and f.endswith(".txt")])
    
    if num_keyword_files == 0:
        logging.error("No keyword files found in the directory. Please generate keyword files first.")
        return

    logging.info(f"Found {num_keyword_files} keyword files to process.")

    # Run scrapers in parallel for each keyword file
    processes = []
    for i in range(num_keyword_files):
        process = multiprocessing.Process(
            target=run_scraper,
            args=(i,)  # Pass the tqdm position
        )
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All scrapers have completed.")


if __name__ == "__main__":
    main()
