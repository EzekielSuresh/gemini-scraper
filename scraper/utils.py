from urllib.parse import urlparse
import re
import json
from pathlib import Path
import logging

#TODO: get sub_urls
#TODO: parse and save result (page content)

def get_url_title(url):
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    if path == '':
        return re.sub(r'[^\w\-]', '_', parsed.netloc)
    else:
        return path.split('/')[-1]
    
def get_sub_urls(data):
    sub_urls = data["website_urls"]
    return sub_urls

def parse_scraped_data(data):
    start = data.find('{')
    end = data.rfind('}')
    if start == -1 or end == -1 or end < start:
        # No valid JSON found
        return None
    parsed = data[start:end+1]
    parsed_dict = json.loads(parsed)
    return parsed_dict

def save_scraped_data(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
def filter_sub_urls(sub_urls, base_url, limit=10):
    filtered = [url for url in sub_urls if url.startswith(base_url)]
    #print(filtered[:limit])
    return filtered[:limit]

def setup_logger(log_path='logs/scraper.log'):
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("scraper")
    logger.setLevel(logging.INFO)
    # Setup file handler
    fh = logging.FileHandler(log_path, encoding='utf-8')
    fh.setLevel(logging.INFO)
    # Setup stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    # Format logs
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    # Add handler
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
    