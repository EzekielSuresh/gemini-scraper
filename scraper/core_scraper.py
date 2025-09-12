from scrapling.fetchers import PlayWrightFetcher
import os
from google import genai
from google.genai import types
from .utils import get_url_title, parse_scraped_data, get_sub_urls, save_scraped_data

class ScrapedPage:
    def __init__(self, url, title, sub_urls=None, content=None, scraped_at=None):
        self.url = url
        self.title = title
        self.sub_urls = sub_urls or []
        self.content = content
        self.scraped_at = scraped_at
        

def fetch_page(url, logger=None):
    try:
        page = PlayWrightFetcher.fetch(url)
        main_text = page.css_first('body')
        if logger:
            logger.info(f"Fetched {url}")
        # If you want the full HTML, use page
        return main_text if main_text else page
    except Exception as e:
        if logger:
            logger.error(f"Error fetching from {url}: {e}")
        return None

def build_prompt(url, page_html):
    prompt = (
        "You are an expert web scraper. "
        "Given the following HTML, extract the information as described.\n\n"
        "Identify and return website URLs from the HTML that will lead to submenus or subcategories for deep scraping.\n"
        "For each URL you extract, if it is a relative URL (e.g., '/faq'), convert it to an absolute URL by combining it with the base URL of the provided HTML page.\n"
        "Only include absolute URLs (starting with 'http://' or 'https://') that belong to the same domain as the provided HTML.\n"
        "Return the extracted information and the list of website URLs ('website_urls') in JSON format.\n\n"
        f"Base URL: {url}\n"
        f"HTML:\n{page_html}\n\n"
    )
    return prompt

def save_result(data, title, logger=None):
    #TODO: Add filename safety check (Remove forbidden characters) 
    folder = os.path.join("results", f"{title}")
    filename = f"{title}.json"
    filepath = os.path.join(folder, filename)
    save_scraped_data(data, filepath, logger)

def run_gemini_scraper(url, logger=None):
    title = get_url_title(url)
    #Create ScrapedPage object
    page = ScrapedPage(url, title)
    # Fetch and prepare HTML
    if logger:
        logger.info(f"Scraping {url}")
    page_html = fetch_page(url, logger)
    prompt = build_prompt(url, page_html)

    client = genai.Client(
        api_key="AIzaSyD1ORIS7_VMOdd10bZswlHvRsMMrOF310U"
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=f"{prompt}"
        ),
        contents=f"Get all meaningful content from this page"
    )
    
    if logger:
        logger.info(f"Successfully scraped {url}")
    #print(response.text)
    parsed_response = parse_scraped_data(response.text, logger)
    sub_urls = get_sub_urls(parsed_response)
    page.content = parsed_response
    page.sub_urls = sub_urls
    save_result(parsed_response, page.title, logger)
    return page
