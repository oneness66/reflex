import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

BASE_URL = "https://vedabase.io"
BG_URL = "https://vedabase.io/en/library/bg/"
DATA_DIR = "bg_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_bg_chapters():
    print(f"Scraping BG chapters from {BG_URL}...")
    soup = get_soup(BG_URL)
    if not soup:
        return []

    chapters = []
    # The chapter list is usually in a div with class 'col-12' or similar, inside the main content
    # Based on SB scraping, we look for links in the content area
    
    # Vedabase structure for BG main page:
    # <div class="r-chapter-list"> ... <a href="/en/library/bg/1/">Chapter One...</a>
    
    # Let's try to find all links that look like chapter links
    links = soup.select('a[href^="/en/library/bg/"]')
    
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        
        # Filter out non-chapter links (like "Setting the Scene", "Preface", etc. if we only want chapters)
        # But user might want everything. The user said "Bhagvat gita ... AS iti is", implying the whole book.
        # However, for the "Chapter" structure, we usually focus on the 18 chapters.
        # Let's grab everything that looks like a chapter or front matter.
        
        # Check if it's a chapter (usually has a number or specific path)
        # /en/library/bg/1/ -> Chapter 1
        # /en/library/bg/introduction/ -> Introduction
        
        slug = href.strip('/').split('/')[-1]
        
        # We can categorize them
        is_chapter = slug.isdigit()
        
        chapter_data = {
            "title": text,
            "url": BASE_URL + href,
            "slug": slug,
            "is_chapter": is_chapter,
            "number": int(slug) if is_chapter else None
        }
        
        # Avoid duplicates and self-link
        if href != "/en/library/bg/" and chapter_data not in chapters:
             chapters.append(chapter_data)
             
    print(f"Found {len(chapters)} items.")
    return chapters

def scrape_verses_for_chapter(chapter_url, chapter_num):
    print(f"Scraping verses for Chapter {chapter_num} from {chapter_url}...")
    soup = get_soup(chapter_url)
    if not soup:
        return []
        
    verses = []
    # Verses are usually listed in the chapter page
    # <a href="/en/library/bg/1/1/">Text 1</a>
    
    links = soup.select(f'a[href^="/en/library/bg/{chapter_num}/"]')
    
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        
        # We want "Text 1", "Text 2" etc.
        # The href should be like /en/library/bg/1/1/
        
        parts = href.strip('/').split('/')
        if len(parts) >= 5: # en, library, bg, chapter, verse
            verse_slug = parts[-1]
            
            # Check if it's a verse link (sometimes there are nav links)
            # Usually verse slug is a number
            if verse_slug.replace('.', '').isdigit(): # Handle 1.1 if that happens, but usually just 1
                verse_data = {
                    "title": text,
                    "url": BASE_URL + href,
                    "slug": verse_slug,
                    "number": verse_slug
                }
                if verse_data not in verses:
                    verses.append(verse_data)
                    
    print(f"Found {len(verses)} verses for Chapter {chapter_num}.")
    return verses

def scrape_verse_content(verse_url):
    # print(f"Scraping content from {verse_url}...")
    soup = get_soup(verse_url)
    if not soup:
        return None
        
    content = {}
    
    # All content is in div.s-justify els in order:
    # 0: Verse ID (e.g., "Bg. 1.1")
    # 1: Devanagari
    # 2: Transliteration
    # 3: Synonyms
    # 4: Translation
    # 5+: Purport paragraphs
    
    s_justify_divs = soup.select('div.s-justify')
    
    if len(s_justify_divs) >= 5:
        # Devanagari (div 1)
        devanagari_text = s_justify_divs[1].get_text('\n')
        content['sanskrit_devanagari'] = [line.strip() for line in devanagari_text.split('\n') if line.strip()]
        
        # Transliteration (div 2)
        transliteration_text = s_justify_divs[2].get_text('\n')
        content['sanskrit_transliterated'] = [line.strip() for line in transliteration_text.split('\n') if line.strip()]
        
        # Synonyms (div 3)
        content['synonyms'] = s_justify_divs[3].get_text(strip=True)
        
        # Translation (div 4)
        content['translation'] = s_justify_divs[4].get_text(strip=True)
        
        # Purport (div 5 onwards) - join all remaining divs as paragraphs
        purport_paragraphs = []
        for div in s_justify_divs[5:]:
            text = div.get_text(strip=True)
            # Skip footer/donation text
            if "Donate" in text or "Thanks to" in text:
                continue
            if text:  # Skip empty divs
                purport_paragraphs.append(text)
        
        if purport_paragraphs:
            content['purport'] = "\n\n".join(purport_paragraphs)
            
    return content

def main():
    # 1. Scrape Chapters
    chapters = scrape_bg_chapters()
    
    # Save chapters list
    with open(os.path.join(DATA_DIR, "bg_chapters.json"), "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=4)
        
    # 2. Scrape Verses for each Chapter
    all_verses_metadata = {}
    all_verses_content = {}
    
    for chapter in chapters:
        if not chapter['is_chapter']:
            continue
            
        chapter_num = chapter['number']
        
        verses = scrape_verses_for_chapter(chapter['url'], chapter_num)
        all_verses_metadata[chapter_num] = verses
        
        # Scrape content for each verse
        for verse in verses:
            print(f"Scraping BG {chapter_num}.{verse['number']}...")
            content = scrape_verse_content(verse['url'])
            if content:
                key = f"{chapter_num}-{verse['number']}"
                content['chapter'] = chapter_num
                content['verse'] = verse['number']
                all_verses_content[key] = content
            time.sleep(0.2) # Be gentle
            
    # Save verse metadata
    with open(os.path.join(DATA_DIR, "bg_verses_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(all_verses_metadata, f, indent=4)
        
    # Save verse content
    with open(os.path.join(DATA_DIR, "bg_verses_content.json"), "w", encoding="utf-8") as f:
        json.dump(all_verses_content, f, indent=4)
        
    print("Scraping complete!")

if __name__ == "__main__":
    main()
