"""
Scrape magazine cover images from BTG India website
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def scrape_btg_magazine_images(output_dir="btg_magazine_images"):
    """
    Scrape magazine cover images from BTG India website
    
    Args:
        output_dir: Directory to save downloaded images
    """
    url = "https://btgindia.com/read-english-monthly-btg-magazine/"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching page: {url}")
    
    # Use headers to avoid 406 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all images - try multiple selectors
        images = []
        
        # Look for magazine cover images (adjust selectors based on actual HTML structure)
        # Common patterns for magazine sites
        img_tags = soup.find_all('img')
        
        print(f"Found {len(img_tags)} images on the page")
        
        downloaded_count = 0
        
        for idx, img in enumerate(img_tags, 1):
            img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            
            if not img_url:
                continue
            
            # Skip very small images, icons, logos
            width = img.get('width', '')
            height = img.get('height', '')
            alt = img.get('alt', '')
            
            # Convert to absolute URL
            img_url = urljoin(url, img_url)
            
            # Skip data URIs and non-http URLs
            if not img_url.startswith('http'):
                continue
                
            print(f"\n[{idx}] Image URL: {img_url}")
            print(f"    Alt text: {alt}")
            print(f"    Dimensions: {width}x{height}")
            
            # Download the image
            try:
                img_response = requests.get(img_url, headers=headers, timeout=30)
                img_response.raise_for_status()
                
                # Extract filename from URL or create one
                filename = os.path.basename(img_url.split('?')[0])
                if not filename or '.' not in filename:
                    filename = f"btg_magazine_{idx}.jpg"
                
                # Sanitize filename
                filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
                
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"    ✓ Downloaded: {filepath} ({len(img_response.content)} bytes)")
                downloaded_count += 1
                
                # Be respectful - add delay between downloads
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ Failed to download: {e}")
        
        print(f"\n{'='*60}")
        print(f"Download complete!")
        print(f"Total images downloaded: {downloaded_count}")
        print(f"Saved to: {os.path.abspath(output_dir)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        print("\nTrying alternative approach with selenium...")
        scrape_with_selenium(output_dir)

def scrape_with_selenium(output_dir="btg_magazine_images"):
    """
    Fallback method using Selenium for JavaScript-heavy sites
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        
        print("Using Selenium to scrape...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            url = "https://btgindia.com/read-english-monthly-btg-magazine/"
            print(f"Loading page: {url}")
            driver.get(url)
            
            # Wait for images to load
            time.sleep(3)
            
            # Scroll to load lazy images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Find all images
            img_elements = driver.find_elements(By.TAG_NAME, 'img')
            
            print(f"Found {len(img_elements)} images")
            
            downloaded_count = 0
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            for idx, img in enumerate(img_elements, 1):
                try:
                    img_url = img.get_attribute('src') or img.get_attribute('data-src')
                    
                    if not img_url or not img_url.startswith('http'):
                        continue
                    
                    alt = img.get_attribute('alt') or ''
                    
                    print(f"\n[{idx}] Downloading: {img_url}")
                    print(f"    Alt: {alt}")
                    
                    # Download
                    img_response = requests.get(img_url, headers=headers, timeout=30)
                    img_response.raise_for_status()
                    
                    filename = os.path.basename(img_url.split('?')[0])
                    if not filename or '.' not in filename:
                        filename = f"btg_magazine_{idx}.jpg"
                    
                    filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"    ✓ Saved: {filepath}")
                    downloaded_count += 1
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}")
            
            print(f"\n{'='*60}")
            print(f"Total downloaded: {downloaded_count}")
            print(f"Saved to: {os.path.abspath(output_dir)}")
            
        finally:
            driver.quit()
            
    except ImportError:
        print("\nSelenium not installed. Install with: pip install selenium")
        print("You also need to install ChromeDriver")
    except Exception as e:
        print(f"Selenium error: {e}")

if __name__ == "__main__":
    scrape_btg_magazine_images()
