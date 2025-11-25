"""
Scrape articles from BTG India magazine pages
"""
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

def scrape_btg_magazine_articles(url, output_file="btg_articles.json"):
    """
    Scrape article information from a BTG magazine issue page
    
    Args:
        url: URL of the magazine issue page
        output_file: JSON file to save the scraped data
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    print(f"Scraping: {url}\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        
        # Look for article containers - adjust selectors based on actual page structure
        # Common patterns: article, .post, .article-card, .entry, etc.
        
        # Try multiple selectors
        article_containers = (
            soup.find_all('article') or
            soup.find_all(class_=lambda x: x and ('article' in x.lower() or 'post' in x.lower())) or
            soup.find_all('div', class_=lambda x: x and 'card' in x.lower())
        )
        
        print(f"Found {len(article_containers)} article containers\n")
        
        for idx, container in enumerate(article_containers, 1):
            try:
                # Extract title
                title_tag = (
                    container.find('h1') or 
                    container.find('h2') or 
                    container.find('h3') or
                    container.find(class_=lambda x: x and 'title' in x.lower())
                )
                
                title = title_tag.get_text(strip=True) if title_tag else "No title found"
                
                # Extract link
                link_tag = container.find('a', href=True)
                link = urljoin(url, link_tag['href']) if link_tag else None
                
                # Extract reading time
                time_text = container.find(string=lambda text: text and 'min' in text.lower())
                reading_time = time_text.strip() if time_text else None
                
                # Extract date
                date_tag = container.find(class_=lambda x: x and 'date' in x.lower())
                date = date_tag.get_text(strip=True) if date_tag else None
                
                # Extract premium status
                is_premium = bool(container.find(string=lambda text: text and 'premium' in text.lower()))
                
                # Extract image
                img_tag = container.find('img')
                image_url = None
                if img_tag:
                    image_url = img_tag.get('src') or img_tag.get('data-src')
                    if image_url:
                        image_url = urljoin(url, image_url)
                
                article_data = {
                    'title': title,
                    'link': link,
                    'reading_time': reading_time,
                    'date': date,
                    'is_premium': is_premium,
                    'image_url': image_url
                }
                
                articles.append(article_data)
                
                print(f"[{idx}] {title}")
                print(f"    Link: {link}")
                print(f"    Time: {reading_time}")
                print(f"    Premium: {is_premium}")
                print(f"    Image: {image_url}")
                print()
                
            except Exception as e:
                print(f"Error processing article {idx}: {e}")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"Scraped {len(articles)} articles")
        print(f"Saved to: {output_file}")
        print(f"{'='*60}")
        
        return articles
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

def scrape_article_content(article_url):
    """
    Scrape the full content of an individual article
    
    Args:
        article_url: URL of the article to scrape
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        response = requests.get(article_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract article content
        content_container = (
            soup.find('article') or
            soup.find(class_=lambda x: x and 'content' in x.lower()) or
            soup.find('main')
        )
        
        if content_container:
            # Remove script and style elements
            for script in content_container(['script', 'style']):
                script.decompose()
            
            content = content_container.get_text(separator='\n', strip=True)
            return content
        
        return None
        
    except Exception as e:
        print(f"Error scraping article content: {e}")
        return None

if __name__ == "__main__":
    # November 2025 issue URL
    nov_2025_url = "https://btgindia.com/read-english-monthly-btg-magazine/english-monthly-november-2025/"
    
    articles = scrape_btg_magazine_articles(nov_2025_url, "btg_november_2025_articles.json")
    
    # Optionally scrape individual article content
    # Note: This may be blocked for premium content
    # for article in articles[:1]:  # Test with first article
    #     if article['link']:
    #         print(f"\nScraping content for: {article['title']}")
    #         content = scrape_article_content(article['link'])
    #         if content:
    #             article['content'] = content
