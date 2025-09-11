from scraper.core_scraper import run_gemini_scraper
from scraper.utils import filter_sub_urls, setup_logger
from scraper.concurrent_scraper import scrap_suburls
 
logger = setup_logger()

def main():
    url = input("Enter the URL to scrape: ").strip()
    logger.info(f"Starting scrap for main page: {url}")
    scraped_page = run_gemini_scraper(url, logger)
    sub_urls = filter_sub_urls(scraped_page.sub_urls, scraped_page.url)
    logger.info(f"Starting scrap for subpages")
    scrap_suburls(sub_urls, scraped_page.title, logger=logger)
    logger.info("All scraping tasks completed!")   
    
if __name__ == "__main__":
    main()