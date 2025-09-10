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
        

def fetch_page(url):
    page = PlayWrightFetcher.fetch(url)
    main_text = page.css_first('body')
    # If you want the full HTML, use page
    return main_text if main_text else page

def build_prompt(page_html):
    prompt = (
        "You are an expert web scraper. "
        "Given the following HTML, extract the information as described.\n\n"
        "Identify and return website URLs from the HTML that will lead to submenus or subcategories for deep scraping.\n"
        "Return the extracted information and the list of website URLs ('website_urls') in JSON format.\n\n"
        f"HTML:\n{page_html}\n\n"
    )
    return prompt

def save_result(data, title):
    #TODO: Add filename safety check (Remove forbidden characters) 
    folder = os.path.join("results", f"{title}")
    filename = f"{title}.json"
    filepath = os.path.join(folder, filename)
    save_scraped_data(data, filepath)

#TODO: Implement log file system
def update_logs():
    return

def run_gemini_scraper(url):
    title = get_url_title(url)
    #Create ScrapedPage object
    page = ScrapedPage(url, title)
    # Fetch and prepare HTML
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
    sub_urls = get_sub_urls(parsed_response)
    page.content = parsed_response
    page.sub_urls = sub_urls
    save_result(parsed_response, page.title)
    return page
