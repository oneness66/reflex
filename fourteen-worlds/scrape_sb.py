import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_sb():
    url = "https://vedabase.io/en/library/sb/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Scraping SB from {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        cantos = []
        # Pattern: /en/library/sb/1/ etc.
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith("/en/library/sb/") and href.count('/') == 5: # e.g. /en/library/sb/1/
                title = link.get_text(strip=True)
                # Extract number from href
                try:
                    number = int(href.strip('/').split('/')[-1])
                    cantos.append({
                        "title": title,
                        "url": "https://vedabase.io" + href,
                        "number": number,
                        "slug": f"canto-{number}"
                    })
                except ValueError:
                    continue
        
        # Sort by number
        cantos.sort(key=lambda x: x['number'])
        
        with open('sb_data.json', 'w', encoding='utf-8') as f:
            json.dump(cantos, f, indent=2)
            
        print(f"Scraped {len(cantos)} cantos.")
        
    except Exception as e:
        print(f"Error scraping SB: {e}")

if __name__ == "__main__":
    scrape_sb()
