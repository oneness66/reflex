import os
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import time

BASE_URL = "https://www.iskcon-truth.com/bhu-mandala/"
OUTPUT_DIR = "bhu-mandala"

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.links.append(value)

def download_file(url, dest_path):
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        print(f"Downloading {url} -> {dest_path}")
        
        # Check if it's a directory (ends with /)
        if url.endswith('/'):
            # It's a directory, we need to crawl it
            crawl_and_download(url, dest_path)
        else:
            # It's a file
            if not os.path.exists(dest_path):
                urllib.request.urlretrieve(url, dest_path)
                time.sleep(0.1) # Be nice to the server
            else:
                print(f"Skipping {dest_path}, already exists")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def crawl_and_download(current_url, current_output_dir):
    print(f"Crawling {current_url}")
    try:
        response = urllib.request.urlopen(current_url)
        html_content = response.read().decode('utf-8')
        
        parser = LinkParser()
        parser.feed(html_content)
        
        for link in parser.links:
            # Skip query parameters, parent directory, etc.
            if link.startswith('?') or link.startswith('#') or link == '../' or link == './':
                continue
            
            # Handle absolute URLs (ignore external)
            if link.startswith('http'):
                if not link.startswith(BASE_URL):
                    continue
                # If it is a full URL to our target, convert to relative path logic if needed
                # But simpler to just use relative links if possible.
                # If the site returns full URLs, we handle them.
            
            # Clean up link
            clean_link = link.split('?')[0]
            if not clean_link:
                continue
                
            # Construct full URL
            full_url = urllib.parse.urljoin(current_url, link)
            
            # Ensure we are still within the base URL scope
            if not full_url.startswith(BASE_URL):
                continue

            # Calculate local path
            # Get the relative path from the BASE_URL
            rel_path = full_url[len(BASE_URL):]
            if rel_path.startswith('/'):
                rel_path = rel_path[1:]
            
            local_path = os.path.join(OUTPUT_DIR, urllib.parse.unquote(rel_path))
            
            # Avoid processing the same directory we are in if it maps to empty relative path
            if not rel_path:
                continue

            download_file(full_url, local_path)
            
    except Exception as e:
        print(f"Error crawling {current_url}: {e}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    crawl_and_download(BASE_URL, OUTPUT_DIR)
