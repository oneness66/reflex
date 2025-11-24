import requests
from bs4 import BeautifulSoup
import json
import os
import time

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
        # Pattern: /en/library/sb/{canto_num}/{chapter_num}/
        prefix = f"/en/library/sb/{canto_num}/"
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(prefix) and href.count('/') == 6:
                # e.g. /en/library/sb/1/1/
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
        print(f"Error scraping chapters: {e}")
        return []

def scrape_verses(canto_num, chapter_num):
    url = f"https://vedabase.io/en/library/sb/{canto_num}/{chapter_num}/"
    print(f"Scraping Verses for Canto {canto_num} Chapter {chapter_num} from {url}...")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        verses = []
        # Pattern: /en/library/sb/{canto_num}/{chapter_num}/{verse_num}/
        prefix = f"/en/library/sb/{canto_num}/{chapter_num}/"
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(prefix) and href.count('/') == 7:
                # e.g. /en/library/sb/1/1/1/
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
        print(f"Error scraping verses: {e}")
        return []

def main():
    # Scrape Canto 1 Chapters
    canto_1_chapters = scrape_chapters(1)
    
    # Scrape Chapter 1 Verses
    canto_1_chapter_1_verses = scrape_verses(1, 1)
    
    data = {
        "canto_1_chapters": canto_1_chapters,
        "canto_1_chapter_1_verses": canto_1_chapter_1_verses
    }
    
    with open('sb_content_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Scraped {len(canto_1_chapters)} chapters and {len(canto_1_chapter_1_verses)} verses.")

if __name__ == "__main__":
    main()
