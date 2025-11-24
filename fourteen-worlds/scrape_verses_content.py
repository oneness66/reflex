import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_verse_content(canto, chapter, verse):
    """Scrape content for a single verse"""
    url = f"https://vedabase.io/en/library/sb/{canto}/{chapter}/{verse}/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        verse_data = {
            "canto": canto,
            "chapter": chapter,
            "verse": verse,
            "url": url,
        }
        
        # Extract Sanskrit verse (Devanagari)
        devanagari_elem = soup.find('div', class_='r')
        if devanagari_elem:
            verse_data["sanskrit_devanagari"] = devanagari_elem.get_text(strip=True)
        
        # Extract transliterated Sanskrit
        verse_text_elem = soup.find('div', class_='v')
        if verse_text_elem:
            verse_data["sanskrit_transliterated"] = verse_text_elem.get_text(strip=True)
        
        # Extract synonyms (word-by-word)
        synonyms_elem = soup.find('div', class_='s')
        if synonyms_elem:
            verse_data["synonyms"] = synonyms_elem.get_text(strip=True)
        
        # Extract translation
        translation_elem = soup.find('div', class_='t')
        if translation_elem:
            verse_data["translation"] = translation_elem.get_text(strip=True)
        
        # Extract purport
        purport_elem = soup.find('div', class_='p')
        if purport_elem:
            # Get all text from purport, preserving some structure
            purport_paragraphs = []
            for p in purport_elem.find_all(['p', 'div']):
                text = p.get_text(strip=True)
                if text and text not in purport_paragraphs:
                    purport_paragraphs.append(text)
            verse_data["purport"] = "\n\n".join(purport_paragraphs) if purport_paragraphs else purport_elem.get_text(strip=True)
        
        return verse_data
        
    except Exception as e:
        print(f"Error scraping verse {canto}.{chapter}.{verse}: {e}")
        return None

def main():
    # Load the verse list from sb_full_content.json
    print("Loading verse list...")
    with open('sb_full_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sb_verses = data['sb_verses']
    all_verse_content = {}
    
    total_verses = sum(len(verses) for verses in sb_verses.values())
    print(f"Found {total_verses} verses to scrape across {len(sb_verses)} chapters")
    print("This will take approximately 3-6 hours with respectful delays...")
    print()
    
    processed = 0
    
    for chapter_key in sorted(sb_verses.keys()):
        canto, chapter = map(int, chapter_key.split('-'))
        verses = sb_verses[chapter_key]
        
        print(f"Processing Canto {canto}, Chapter {chapter} ({len(verses)} verses)...")
        
        for verse_meta in verses:
            verse_num = verse_meta['number']
            
            # Scrape the verse content
            verse_content = scrape_verse_content(canto, chapter, verse_num)
            
            if verse_content:
                key = f"{canto}-{chapter}-{verse_num}"
                all_verse_content[key] = verse_content
                processed += 1
                
                # Progress indicator
                percent = (processed / total_verses) * 100
                print(f"  Progress: {processed}/{total_verses} ({percent:.1f}%) - Verse {verse_num}", end='\r')
            
            # Be very respectful to the server
            time.sleep(random.uniform(1.0, 2.0))
        
        print()  # New line after chapter
        
        # Save after each chapter as backup
        with open('sb_verse_content_backup.json', 'w', encoding='utf-8') as f:
            json.dump(all_verse_content, f, indent=2, ensure_ascii=False)
    
    print()
    print("Scraping complete!")
    print(f"Successfully scraped {len(all_verse_content)} verses")
    
    # Save final version
    with open('sb_verse_content.json', 'w', encoding='utf-8') as f:
        json.dump(all_verse_content, f, indent=2, ensure_ascii=False)
    
    print("Saved to sb_verse_content.json")

if __name__ == "__main__":
    main()
