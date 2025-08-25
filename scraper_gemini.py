# gemini_scraper.py

from scrapling.fetchers import PlayWrightFetcher
import os
import datetime
from google import genai
from google.genai import types

def fetch_page(url):
    page = PlayWrightFetcher.fetch(url)
    main_text = page.css_first('body')
    # If you want the full HTML, use page.html
    return main_text if main_text else page

def build_prompt(page_html):
    prompt = (
        "You are an expert web scraper. "
        "Given the following HTML, extract the information as described.\n\n"
        f"HTML:\n{page_html}\n\n"
    )
    return prompt

def run_gemini_scraper(url, instruction):
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
        contents=f"{instruction}"
    )
    
    print(response.text)

def save_result(data):
    if not os.path.exists("results"):
        os.makedirs("results")
        
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
    url_slug = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    filename = f"{timestamp}_{url_slug}.txt"
    filepath = os.path.join("results", filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data) 
    print(f"Result saved to {filepath}")
    update_logs()

def update_logs():
    return

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ").strip()
    instruction = input("Describe what you want to extract: ").strip()
    run_gemini_scraper(url, instruction)
