import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

def scrape_verse_content(canto, chapter, verse):
    """Scrape individual verse content from Vedabase"""
    url = f"https://vedabase.io/en/library/sb/{canto}/{chapter}/{verse}/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        verse_data = {
            "canto": canto,
            "chapter": chapter,
            "verse": verse,
            "reference": f"ŚB {canto}.{chapter}.{verse}"
        }
        
        # Find all h2 headers and extract content
        headers = soup.find_all('h2')
        
        for h2 in headers:
            section_name = h2.get_text(strip=True).lower()
            next_elem = h2.find_next_sibling()
            
            if next_elem:
                if 'devanagari' in section_name:
                    full_text = next_elem.get_text('\n', strip=True)
                    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                    verse_data['sanskrit_devanagari'] = lines if len(lines) > 1 else [full_text]
                    
                elif 'verse text' in section_name:
                    full_text = next_elem.get_text('\n', strip=True)
                    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                    verse_data['sanskrit_transliterated'] = lines if len(lines) > 1 else [full_text]
                    
                elif 'synonym' in section_name:
                    verse_data['synonyms'] = next_elem.get_text(strip=True)
                    
                elif 'translation' in section_name:
                    verse_data['translation'] = next_elem.get_text(strip=True)
                    
                elif 'purport' in section_name:
                    purport_paragraphs = []
                    curr = h2.find_next_sibling()
                    while curr and curr.name != 'h2':
                        if curr.name in ['div', 'p']:
                            text = curr.get_text(separator=' ', strip=True)
                            if text:
                                purport_paragraphs.append(text)
                        curr = curr.find_next_sibling()
                    verse_data['purport'] = '\n\n'.join(purport_paragraphs)
        
        return verse_data
        
    except Exception as e:
        return None

def scrape_canto(canto_num, output_dir="verse_data", resume=True, force=False):
    """Scrape all verses for a specific canto using sb_full_content.json"""
    output_file = os.path.join(output_dir, f"canto_{canto_num}_verses.json")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load existing scraped data
    existing_data = {}
    if resume and not force and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"Resuming: {len(existing_data)} verses already scraped\n")
    
    # Load verses structure
    with open('sb_full_content.json', 'r', encoding='utf-8') as f:
        sb_data = json.load(f)
    
    sb_verses = sb_data['sb_verses']
    
    # Get all chapter keys for this canto
    canto_chapters = {k: v for k, v in sb_verses.items() if k.startswith(f"{canto_num}-")}
    
    print(f"\n{'='*70}")
    print(f"  CANTO {canto_num}: {len(canto_chapters)} chapters")
    print(f"{'='*70}\n")
    
    total_verses = 0
    scraped_count = 0
    
    for chapter_key in sorted(canto_chapters.keys(), key=lambda x: int(x.split('-')[1])):
        verses = canto_chapters[chapter_key]
        chapter_num = int(chapter_key.split('-')[1])
        
        print(f"Chapter {canto_num}.{chapter_num}: {len(verses)} verses")
        print(f"{'-'*70}")
        
        for verse_info in verses:
            verse_num = verse_info['number']
            verse_id = f"{canto_num}-{chapter_num}-{verse_num}"
            total_verses += 1
            
            if not force and verse_id in existing_data:
                print(f"  ✓ {verse_id} (cached)")
                continue
            
            print(f"  → {verse_id}...", end='', flush=True)
            verse_content = scrape_verse_content(canto_num, chapter_num, verse_num)
            
            if verse_content:
                existing_data[verse_id] = verse_content
                scraped_count += 1
                print(" ✓")
            else:
                print(" ✗")
            
            time.sleep(random.uniform(1.0, 2.0))
        
        # Save after each chapter
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {len(existing_data)} verses\n")
    
    print(f"{'='*70}")
    print(f"  COMPLETE! Canto {canto_num}")
    print(f"  Total verses: {total_verses}")
    print(f"  Newly scraped: {scraped_count}")
    print(f"  Database size: {len(existing_data)}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    import sys
    force = "force" in sys.argv
    canto = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "canto" else 1
    scrape_canto(canto, force=force)
