"""
Scrape BTG magazine articles using browser automation with authentication
Requires: pip install selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from pathlib import Path

def scrape_btg_articles_authenticated():
    """
    Scrape BTG magazine articles using Selenium with user authentication
    """
    # November 2025 articles
    articles_to_scrape = [
        {
            "title": "The Technique For Universal Love",
            "url": "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/",
            "filename": "technique_for_universal_love.txt"
        },
        {
            "title": "How Gita Wisdom Helped Me Transcend Polio",
            "url": "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/",
            "filename": "gita_wisdom_transcend_polio.txt"
        },
        {
            "title": "The Forgotten Are Awakening",
            "url": "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/",
            "filename": "forgotten_are_awakening.txt"
        },
        {
            "title": "From Bollywood to Bhagavad-gita",
            "url": "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/",
            "filename": "bollywood_to_bhagavad_gita.txt"
        }
    ]
    
    # Create output directory
    output_dir = Path("btg_articles_content")
    output_dir.mkdir(exist_ok=True)
    
    # Set up Chrome options
    chrome_options = Options()
    # Don't use headless mode so you can see the browser and log in if needed
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    print("Initializing browser...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the main magazine page first
        print("\nNavigating to BTG India...")
        driver.get("https://btgindia.com/")
        time.sleep(3)
        
        print("\n" + "="*60)
        print("PLEASE LOG IN TO YOUR ACCOUNT IN THE BROWSER WINDOW")
        print("="*60)
        print("\nInstructions:")
        print("1. If you're not already logged in, please log in now")
        print("2. Once logged in, press ENTER here to continue...")
        input("\nPress ENTER when you're logged in and ready to continue...")
        
        all_articles_data = []
        
        # Navigate to November 2025 page
        nov_2025_url = "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/"
        print(f"\nNavigating to November 2025 articles page...")
        driver.get(nov_2025_url)
        time.sleep(5)
        
        # Find all article links on the page
        print("\nFinding article links...")
        article_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='btgindia.com']")
        
        # Extract unique article URLs
        article_urls = {}
        for link in article_links:
            try:
                href = link.get_attribute('href')
                text = link.text.strip()
                
                # Look for article-specific URLs
                if href and '/202' in href and 'article' in href.lower() or any(keyword in text.lower() for keyword in ['technique', 'gita', 'forgotten', 'bollywood', 'awakening', 'polio']):
                    if text and len(text) > 5:
                        article_urls[text] = href
            except:
                pass
        
        print(f"\nFound {len(article_urls)} unique article links:")
        for title, url in article_urls.items():
            print(f"  - {title}")
            print(f"    {url}")
        
        # If no specific article URLs found, try to scrape from the current page
        if not article_urls:
            print("\nNo individual article URLs found. Scraping content from main page...")
            
            # Look for article content on the page
            try:
                # Wait for content to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
                
                # Find all article elements
                articles = driver.find_elements(By.TAG_NAME, "article")
                
                for idx, article in enumerate(articles, 1):
                    try:
                        title = article.find_element(By.CSS_SELECTOR, "h1, h2, h3, .title").text
                        content = article.text
                        
                        article_data = {
                            "title": title,
                            "content": content,
                            "url": nov_2025_url
                        }
                        
                        all_articles_data.append(article_data)
                        
                        # Save to file
                        filename = f"article_{idx}_{title[:30].replace(' ', '_').replace('/', '_')}.txt"
                        filepath = output_dir / filename
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {title}\n")
                            f.write(f"URL: {nov_2025_url}\n")
                            f.write("="*60 + "\n\n")
                            f.write(content)
                        
                        print(f"\n[{idx}] Saved: {filename}")
                        
                    except Exception as e:
                        print(f"Error processing article {idx}: {e}")
                
            except Exception as e:
                print(f"Error finding articles: {e}")
        else:
            # Scrape individual article pages
            for idx, (title, url) in enumerate(article_urls.items(), 1):
                try:
                    print(f"\n[{idx}/{len(article_urls)}] Scraping: {title}")
                    driver.get(url)
                    time.sleep(3)
                    
                    # Wait for article content to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "article"))
                    )
                    
                    # Extract content
                    article_element = driver.find_element(By.TAG_NAME, "article")
                    content = article_element.text
                    
                    article_data = {
                        "title": title,
                        "content": content,
                        "url": url
                    }
                    
                    all_articles_data.append(article_data)
                    
                    # Save to individual file
                    filename = f"{idx}_{title[:50].replace(' ', '_').replace('/', '_')}.txt"
                    filepath = output_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {title}\n")
                        f.write(f"URL: {url}\n")
                        f.write("="*60 + "\n\n")
                        f.write(content)
                    
                    print(f"    Saved to: {filename}")
                    
                    time.sleep(2)  # Be polite
                    
                except Exception as e:
                    print(f"    Error: {e}")
        
        # Save all articles to JSON
        json_file = output_dir / "all_articles.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Total articles scraped: {len(all_articles_data)}")
        print(f"Saved to directory: {output_dir.absolute()}")
        print(f"JSON file: {json_file}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nClosing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    print("BTG Magazine Article Scraper (Authenticated)")
    print("="*60)
    print("This script will open a browser window.")
    print("Please log in to your BTG India account when prompted.")
    print("="*60)
    
    scrape_btg_articles_authenticated()
