"""
Download BTG Magazine covers by constructing URLs based on patterns
"""
import os
import requests
from datetime import datetime
import time

def download_btg_magazine_covers(output_dir="btg_magazine_covers"):
    """
    Download BTG magazine covers by trying multiple URL patterns
    """
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    }
    
    # Months to try for 2025
    months = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    
    # Common filename patterns for magazine covers
    patterns = [
        "cover.jpg",
        "cover.png",
        "front-cover.jpg",
        "front-cover.png",
        "magazine-cover.jpg",
        "magazine-cover.png",
        "BTG-{month}-2025.jpg",
        "BTG-{month}-2025.png",
        "BTG_{month}_2025.jpg",
        "BTG_{month}_2025.png",
        "btg-{month}-2025.jpg",
        "btg-{month}-2025.png",
        "{month}-2025.jpg",
        "{month}-2025.png",
        "BTG-Cover-{month}-2025.jpg",
        "BTG-Cover-{month}-2025.png",
    ]
    
    downloaded_count = 0
    
    print("Attempting to download magazine covers...\n")
    print("="*60)
    
    # Try different URL structures
    base_urls = [
        "https://btgindia.com/wp-content/uploads/2025/{month}/",
        "https://btgindia.com/wp-content/uploads/2025/",
    ]
    
    tried_urls = set()
    
    for month_num, month_name in months:
        print(f"\n--- {month_name} 2025 ---")
        
        for base_url in base_urls:
            for pattern in patterns:
                # Replace placeholders
                filename = pattern.format(month=month_num)
                full_base = base_url.format(month=month_num)
                url = full_base + filename
                
                # Skip if already tried
                if url in tried_urls:
                    continue
                tried_urls.add(url)
                
                try:
                    response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
                    
                    if response.status_code == 200:
                        # File exists, download it
                        print(f"  ✓ Found: {url}")
                        
                        img_response = requests.get(url, headers=headers, timeout=30)
                        img_response.raise_for_status()
                        
                        # Save with month name
                        ext = os.path.splitext(filename)[1]
                        save_filename = f"BTG_{month_name}_{month_num}_2025{ext}"
                        filepath = os.path.join(output_dir, save_filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(img_response.content)
                        
                        file_size_kb = len(img_response.content) / 1024
                        print(f"    Downloaded: {save_filename} ({file_size_kb:.1f} KB)")
                        downloaded_count += 1
                        
                        time.sleep(0.5)
                        break  # Found this month, move to next
                        
                except requests.exceptions.RequestException:
                    pass  # URL doesn't exist, continue trying
    
    print(f"\n{'='*60}")
    print(f"Download Summary:")
    print(f"  Total covers downloaded: {downloaded_count}")
    print(f"  Saved to: {os.path.abspath(output_dir)}")
    print(f"{'='*60}")
    
    if downloaded_count == 0:
        print("\nNo images found with automatic URL patterns.")
        print("Let me try to scrape the actual page to find image URLs...")
        return scrape_page_for_images(output_dir)
    
    return downloaded_count

def scrape_page_for_images(output_dir):
    """
    Scrape the magazine page itself to extract image URLs
    """
    from bs4 import BeautifulSoup
    
    url = "https://btgindia.com/read-english-monthly-btg-magazine/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    print("\nScraping magazine page for cover images...\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for images that are likely magazine covers
        # They're usually in specific containers or have certain classes
        all_imgs = soup.find_all('img')
        
        downloaded_count = 0
        
        for idx, img in enumerate(all_imgs):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            alt = img.get('alt', '')
            
            if not src:
                continue
            
            # Filter for likely magazine covers
            # They usually have "2025", "BTG", "cover" in the URL or are .jpg/.png from uploads
            if ('2025' in src or '2024' in src or 'BTG' in src or 
                'cover' in src.lower() or 'magazine' in src.lower()):
                
                if not src.startswith('http'):
                    src = 'https://btgindia.com' + src if src.startswith('/') else src
                
                print(f"[{idx+1}] Found potential cover: {src}")
                print(f"    Alt: {alt}")
                
                try:
                    img_response = requests.get(src, headers=headers, timeout=30)
                    img_response.raise_for_status()
                    
                    # Create filename
                    filename = os.path.basename(src.split('?')[0])
                    if not filename:
                        filename = f"cover_{idx+1}.jpg"
                    
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    file_size_kb = len(img_response.content) / 1024
                    print(f"    ✓ Downloaded: {filename} ({file_size_kb:.1f} KB)\n")
                    downloaded_count += 1
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}\n")
        
        print(f"\nTotal images downloaded: {downloaded_count}")
        return downloaded_count
        
    except Exception as e:
        print(f"Error scraping page: {e}")
        return 0

if __name__ == "__main__":
    download_btg_magazine_covers()
