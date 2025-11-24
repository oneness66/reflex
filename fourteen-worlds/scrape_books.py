import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_library():
    url = "https://vedabase.io/en/library/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books = []
        # Based on the screenshot, books are likely in a grid.
        # Inspecting the likely structure (common in such sites)
        # Usually .book-item or similar.
        # Let's look for links that contain images.
        
        # Finding the main container for the library
        # The user mentioned "Fourteen worlds chapters Header Section" -> "Library"
        # The page has a list of books.
        
        # Let's try to find all 'a' tags that have an 'img' inside them, 
        # and the href starts with /en/library/
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/en/library/') and href.count('/') == 4: # e.g. /en/library/bg/
                img = link.find('img')
                if img:
                    title = img.get('title') or img.get('alt') or link.get_text(strip=True)
                    img_src = img.get('src')
                    if img_src:
                        if not img_src.startswith('http'):
                            img_src = "https://vedabase.io" + img_src
                            
                        books.append({
                            "title": title,
                            "url": "https://vedabase.io" + href,
                            "image_url": img_src,
                            "slug": href.strip('/').split('/')[-1]
                        })
        
        # Remove duplicates based on url
        unique_books = {v['url']: v for v in books}.values()
        
        unique_books_list = list(unique_books)
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(unique_books_list, f, indent=2)
        print(f"Saved {len(unique_books_list)} books to books.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_library()
