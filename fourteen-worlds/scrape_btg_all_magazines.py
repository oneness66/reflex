"""
Download BTG magazine content from the main magazine page
"""
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time
import os

def scrape_btg_all_magazines(output_file="btg_all_magazines.json"):
    """
    Scrape all available magazine issues from BTG India
    """
    base_url = "https://btgindia.com/magazine/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    print(f"Scraping: {base_url}\n")
    
    try:
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}\n")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        magazines = []
        
        # Find all magazine issues/links
        # Look for links, articles, divs with magazine information
        
        # Try to find all links
        all_links = soup.find_all('a', href=True)
        
        print(f"Found {len(all_links)} total links on the page\n")
        
        # Filter for magazine-related links
        magazine_links = []
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Look for patterns that indicate magazine issues
            if any(keyword in href.lower() for keyword in ['magazine', 'issue', '202', 'english', 'monthly']):
                full_url = urljoin(base_url, href)
                
                # Get associated image if any
                img = link.find('img')
                img_url = None
                if img:
                    img_url = img.get('src') or img.get('data-src')
                    if img_url:
                        img_url = urljoin(base_url, img_url)
                
                magazine_links.append({
                    'title': text,
                    'url': full_url,
                    'image_url': img_url
                })
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_magazines = []
        for mag in magazine_links:
            if mag['url'] not in seen_urls:
                seen_urls.add(mag['url'])
                unique_magazines.append(mag)
                print(f"Found: {mag['title']}")
                print(f"  URL: {mag['url']}")
                print(f"  Image: {mag['image_url']}")
                print()
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_magazines, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"Found {len(unique_magazines)} magazine issues")
        print(f"Saved to: {output_file}")
        print(f"{'='*60}")
        
        return unique_magazines
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def download_magazine_pdfs(magazines, output_dir="btg_pdfs"):
    """
    Try to download PDF versions of magazines if available
    """
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    downloaded = 0
    
    for idx, mag in enumerate(magazines, 1):
        try:
            # Check if the URL points to a PDF
            if mag['url'].endswith('.pdf'):
                print(f"[{idx}] Downloading PDF: {mag['title']}")
                
                response = requests.get(mag['url'], headers=headers, timeout=60)
                response.raise_for_status()
                
                filename = f"{mag['title'].replace('/', '-')}.pdf"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"    Saved: {filepath}\n")
                downloaded += 1
                time.sleep(1)
                
        except Exception as e:
            print(f"Error downloading {mag['title']}: {e}\n")
    
    print(f"\nDownloaded {downloaded} PDFs")

if __name__ == "__main__":
    magazines = scrape_btg_all_magazines()
    
    # Optionally try to download PDFs
    # download_magazine_pdfs(magazines)
