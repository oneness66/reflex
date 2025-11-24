import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_list(url, category):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    items = []
    try:
        print(f"Scraping {category} from {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Based on the read_url_content output, these are likely simple links in a list.
        # We need to find the main container. Usually it's a div with a class like 'content' or 'search-results'.
        # Let's inspect all 'a' tags and filter by href pattern.
        
        prefix = f"/en/library/{category}/"
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(prefix) and href != prefix:
                title = link.get_text(strip=True)
                # Avoid "Next" or pagination links if they match the pattern (usually they have ?page=)
                if "?" in href:
                    continue
                    
                items.append({
                    "title": title,
                    "url": "https://vedabase.io" + href,
                    "category": category
                })
        
        # Remove duplicates
        unique_items = {v['url']: v for v in items}.values()
        return list(unique_items)
        
    except Exception as e:
        print(f"Error scraping {category}: {e}")
        return []

def main():
    transcripts = scrape_list("https://vedabase.io/en/library/transcripts/", "transcripts")
    letters = scrape_list("https://vedabase.io/en/library/letters/", "letters")
    
    data = {
        "transcripts": transcripts,
        "letters": letters
    }
    
    with open('library_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Scraped {len(transcripts)} transcripts and {len(letters)} letters.")

if __name__ == "__main__":
    main()
