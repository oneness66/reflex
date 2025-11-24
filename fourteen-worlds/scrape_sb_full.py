import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_chapters(canto_num):
    url = f"https://vedabase.io/en/library/sb/{canto_num}/"
    print(f"Scraping Chapters for Canto {canto_num} from {url}...")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        chapters = []
        prefix = f"/en/library/sb/{canto_num}/"
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(prefix) and href.count('/') == 6:
                title = link.get_text(strip=True)
                try:
                    chapter_num = int(href.strip('/').split('/')[-1])
                    chapters.append({
                        "title": title,
                        "url": "https://vedabase.io" + href,
                        "number": chapter_num,
                        "slug": f"chapter-{chapter_num}"
                    })
                except ValueError:
                    continue
        
        chapters.sort(key=lambda x: x['number'])
        return chapters
    except Exception as e:
        print(f"Error scraping chapters for Canto {canto_num}: {e}")
        return []

def scrape_verses(canto_num, chapter_num):
    url = f"https://vedabase.io/en/library/sb/{canto_num}/{chapter_num}/"
    # print(f"Scraping Verses for Canto {canto_num} Chapter {chapter_num}...") 
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        verses = []
        prefix = f"/en/library/sb/{canto_num}/{chapter_num}/"
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(prefix) and href.count('/') == 7:
                text = link.get_text(strip=True)
                if "Text" in text:
                    try:
                        verse_num = int(href.strip('/').split('/')[-1])
                        verses.append({
                            "title": text,
                            "url": "https://vedabase.io" + href,
                            "number": verse_num,
                            "slug": f"verse-{verse_num}"
                        })
                    except ValueError:
                        continue
        
        verses.sort(key=lambda x: x['number'])
        return verses
    except Exception as e:
        print(f"Error scraping verses for Canto {canto_num} Chapter {chapter_num}: {e}")
        return []

def main():
    all_chapters = {}
    all_verses = {}
    
    # Loop through all 12 Cantos
    for canto_num in range(1, 13):
        print(f"\n--- Processing Canto {canto_num} ---")
        chapters = scrape_chapters(canto_num)
        all_chapters[canto_num] = chapters
        
        # Loop through all chapters in this Canto
        for chapter in chapters:
            chapter_num = chapter['number']
            print(f"  Scraping Canto {canto_num}, Chapter {chapter_num}...", end="\r")
            verses = scrape_verses(canto_num, chapter_num)
            
            key = f"{canto_num}-{chapter_num}"
            all_verses[key] = verses
            
            # Be polite to the server
            time.sleep(random.uniform(0.5, 1.5))
            
    print("\nScraping complete!")
    
    data = {
        "sb_chapters": all_chapters,
        "sb_verses": all_verses
    }
    
    # Save to a temporary JSON file first
    with open('sb_full_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Saved data to sb_full_content.json")

if __name__ == "__main__":
    main()
