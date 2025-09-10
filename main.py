from scraper.core_scraper import run_gemini_scraper
from scraper.utils import filter_sub_urls
from scraper.concurrent_scraper import scrap_suburls
 
def main():
    url = input("Enter the URL to scrape: ").strip()
    scraped_page = run_gemini_scraper(url)
    sub_urls = filter_sub_urls(scraped_page.sub_urls, scraped_page.url)
    scrap_suburls(sub_urls, scraped_page.title)
    print("Scraping complete!")    
    
if __name__ == "__main__":
    main()