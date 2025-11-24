import json
import os

def convert_scraped_to_python(canto_num):
    """Convert scraped JSON data to Python format for sb_verse_content.py"""
    input_file = f"verse_data/canto_{canto_num}_verses.json"
    
    if not os.path.exists(input_file):
        print(f"No data found for Canto {canto_num}")
        return {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)
    
    print(f"Converting Canto {canto_num}: {len(scraped_data)} verses")
    return scraped_data

def update_verse_content_file():
    """Update sb_verse_content.py with all scraped verses"""
    all_verses = {}
    
    # Check for all canto files
    for canto in range(1, 13):
        canto_verses = convert_scraped_to_python(canto)
        all_verses.update(canto_verses)
    
    if not all_verses:
        print("No scraped data found!")
        return
    
    # Generate Python file
    output_file = "fourteen_worlds/data/sb_verse_content.py"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Scraped verse content for Srimad Bhagavatam\n")
        f.write("# Auto-generated from scraped data\n\n")
        f.write("verse_content = ")
        
        # Use json.dumps for clean formatting, then convert to Python syntax
        json_str = json.dumps(all_verses, indent=4, ensure_ascii=False)
        f.write(json_str)
        f.write("\n")
    
    print(f"\n✅ Updated {output_file}")
    print(f"   Total verses: {len(all_verses)}")
    print(f"   File size: {os.path.getsize(output_file) / 1024:.1f} KB")

if __name__ == "__main__":
    update_verse_content_file()
