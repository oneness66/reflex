import requests
from bs4 import BeautifulSoup
import json

url = "https://vedabase.io/en/library/sb/1/1/1/"

print("Scraping verse content...")
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

verse_data = {
    "canto": 1,
    "chapter": 1,
    "verse": 1,
    "reference": "ŚB 1.1.1"
}

# Find all h2 headers and get content after them
headers = soup.find_all('h2')

for h2 in headers:
    section_name = h2.get_text(strip=True).lower()
    
    # Get the next sibling element (usually contains the content)
    next_elem = h2.find_next_sibling()
    
    if next_elem:
        content = next_elem.get_text(strip=True)
        
        if 'devanagari' in section_name:
            verse_data['sanskrit_devanagari'] = content
        elif 'verb text' in section_name or section_name == 'verse text':
            verse_data['sanskrit_transliterated'] = content
        elif 'synonym' in section_name:
            verse_data['synonyms'] = content
        elif 'translation' in section_name:
            verse_data['translation'] = content
        elif 'purport' in section_name:
            # For purport, get all text content
            purport_div = h2.find_next_sibling()
            if purport_div:
                # Get all paragraphs
                paragraphs = []
                for elem in purport_div.find_all(['p', 'div'], recursive=False):
                    text = elem.get_text(strip=True)
                    if text and len(text) > 10:
                        paragraphs.append(text)
                verse_data['purport'] = '\n\n'.join(paragraphs) if paragraphs else purport_div.get_text(strip=True)

# Print results
print("\n=== SCRAPED VERSE CONTENT ===\n")
print(f"Reference: {verse_data['reference']}")
print(f"\nDevanagari: {verse_data.get('sanskrit_devanagari', 'Not found')[:100]}...")
print(f"\nTransliterated: {verse_data.get('sanskrit_transliterated', 'Not found')[:100]}...")
print(f"\nSynonyms: {verse_data.get('synonyms', 'Not found')[:100]}...")
print(f"\nTranslation: {verse_data.get('translation', 'Not found')[:200]}...")
print(f"\nPurport length: {len(verse_data.get('purport', ''))} characters")

# Save to JSON
with open('verse_1_1_1_content.json', 'w', encoding='utf-8') as f:
    json.dump(verse_data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved full verse content to verse_1_1_1_content.json")
