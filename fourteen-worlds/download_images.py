import json
import os
import requests
import time

def download_images():
    with open('books.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    os.makedirs('assets/books', exist_ok=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for book in books:
        image_url = book['image_url']
        slug = book['slug']
        filename = f"assets/books/{slug}.jpg"
        
        if os.path.exists(filename):
            print(f"Skipping {slug}, already exists.")
            continue
            
        print(f"Downloading {slug} from {image_url}...")
        try:
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved {filename}")
            time.sleep(0.5) # Be nice to the server
            
        except Exception as e:
            print(f"Failed to download {slug}: {e}")

if __name__ == "__main__":
    download_images()
