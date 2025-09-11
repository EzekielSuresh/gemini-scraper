from scrapling.fetchers import PlayWrightFetcher
import os
from google import genai
from google.genai import types
from .utils import save_scraped_data, get_url_title, parse_scraped_data
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_page(url):
    page = PlayWrightFetcher.fetch(url)
    main_text = page.css_first('body')
    # If you want the full HTML, use page
    return main_text if main_text else page

def build_prompt(page_html):
    prompt = (
        "You are an expert web scraper. "
        "Given the following HTML, extract the information as described.\n\n"
        "Return the extracted information in JSON format.\n\n"
        f"HTML:\n{page_html}\n\n"
    )
    return prompt

#TODO: Update this
def save_result(data, title, sub_url_title):
    #TODO: Add filename safety check (Remove forbidden characters) 
    folder = os.path.join("results", f"{title}")
    filename = f"{sub_url_title}.json"
    filepath = os.path.join(folder, filename)
    save_scraped_data(data, filepath)

def run_concurrent_scraper(url, title, logger=None):
    sub_url_title = get_url_title(url)
    #Create ScrapedPage object
    #page = ScrapedPage(url, title)
    # Fetch and prepare HTML
    if logger:
        logger.info(f"Scraping {url}")
    page_html = fetch_page(url)
    prompt = build_prompt(page_html)

    client = genai.Client(
        api_key="AIzaSyD1ORIS7_VMOdd10bZswlHvRsMMrOF310U"
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=f"{prompt}"
        ),
        #TODO: Set hard-coded instruction for every scraping process
        contents=f"Get all meaningful content from this page"
    )
    
    #print(response.text)
    parsed_response = parse_scraped_data(response.text)
    #sub_urls = get_sub_urls(parsed_response)
    #page.content = parsed_response
    #page.sub_urls = sub_urls
    save_result(parsed_response, title, sub_url_title)
    
def scrap_suburls(sub_urls, title, max_workers=4, logger=None):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(run_concurrent_scraper, url, title, logger): url 
            for url in sub_urls
        }
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
                if logger:
                    logger.info(f"Successfully scraped {url}")
            except Exception as e:
                if logger:
                    logger.error(f"Error scraping {url}: {e}")