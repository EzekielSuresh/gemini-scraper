from scraper.core_scraper import run_gemini_scraper
 
def main():
    url = input("Enter the URL to scrape: ").strip()
    run_gemini_scraper(url)

if __name__ == "__main__":
    main()