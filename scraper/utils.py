from urllib import urlparse
import re
import json

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
    parsed_dict = json.load(parsed)
    return parsed_dict