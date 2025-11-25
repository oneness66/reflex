"""
Parse BTG article HTML files and extract clean content
"""
from bs4 import BeautifulSoup
import json
from pathlib import Path

def parse_article_html(html_file):
    """
    Parse a BTG article HTML file and extract clean content
    
    Args:
        html_file: Path to the HTML file
        
    Returns:
        dict with article data
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = ""
    title_tag = soup.find('h1') or soup.find('h2', class_=lambda x: x and 'title' in x.lower())
    if title_tag:
        title = title_tag.get_text(strip=True)
    
    # Extract article content
    article_content = ""
    
    # Try to find the main article container
    # For Elementor-based sites, look for specific content wrappers
    article_tag = (
        soup.find('div', class_=lambda x: x and 'tts_content_wrapper' in x) or
        soup.find('div', class_=lambda x: x and 'elementor-widget-theme-post-content' in x) or
        soup.find('article') or
        soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'post' in x.lower())) or
        soup.find('main') or
        soup.find('div', class_=lambda x: x and 'elementor' in x.lower())
    )
    
    if article_tag:
        # Remove unwanted elements (scripts, styles, ads, etc.)
        for unwanted in article_tag(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'svg', 'button']):
            unwanted.decompose()
        
        # Also remove common ad/sidebar/share classes
        for ad in article_tag.find_all(class_=lambda x: x and any(kw in x.lower() for kw in ['share', 'social', 'heateor', 'toc', 'table-of-contents', 'sidebar', 'widget'])):
            ad.decompose()
        
        # Get all paragraph tags for cleaner text
        paragraphs = article_tag.find_all(['p', 'blockquote', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if paragraphs:
            # Extract text from each paragraph/heading
            content_parts = []
            for para in paragraphs:
                text = para.get_text(strip=True)
                if text and len(text) > 3:  # Skip very short/empty paragraphs
                    content_parts.append(text)
            article_content = '\n\n'.join(content_parts)
        else:
            # Fallback to getting all text
            article_content = article_tag.get_text(separator='\n\n', strip=True)
    
    # Extract metadata
    author = ""
    author_tag = soup.find(class_=lambda x: x and 'author' in x.lower())
    if author_tag:
        author = author_tag.get_text(strip=True)
    
    date = ""
    date_tag = soup.find('time') or soup.find(class_=lambda x: x and 'date' in x.lower())
    if date_tag:
        date = date_tag.get_text(strip=True)
    
    # Extract featured image
    featured_image = ""
    img_tag = soup.find('img', class_=lambda x: x and ('featured' in x.lower() or 'hero' in x.lower()))
    if not img_tag:
        img_tag = soup.find('img')
    if img_tag:
        featured_image = img_tag.get('src', '')
    
    article_data = {
        'title': title,
        'author': author,
        'date': date,
        'content': article_content,
        'featured_image': featured_image,
        'source_file': str(html_file)
    }
    
    return article_data

def parse_all_articles(articles_dir="btg_articles_content"):
    """
    Parse all HTML article files in the directory
    """
    articles_path = Path(articles_dir)
    
    if not articles_path.exists():
        print(f"Directory not found: {articles_path}")
        return []
    
    html_files = list(articles_path.glob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in {articles_path}")
        return []
    
    print(f"Found {len(html_files)} HTML files to parse\n")
    
    all_articles = []
    
    for idx, html_file in enumerate(html_files, 1):
        print(f"[{idx}/{len(html_files)}] Parsing: {html_file.name}")
        
        try:
            article_data = parse_article_html(html_file)
            all_articles.append(article_data)
            
            print(f"    Title: {article_data['title']}")
            print(f"    Author: {article_data['author']}")
            print(f"    Date: {article_data['date']}")
            print(f"    Content length: {len(article_data['content'])} characters")
            print()
            
            # Save individual text file
            text_file = articles_path / f"{html_file.stem}_parsed.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {article_data['title']}\n")
                f.write(f"Author: {article_data['author']}\n")
                f.write(f"Date: {article_data['date']}\n")
                f.write("=" * 60 + "\n\n")
                f.write(article_data['content'])
            
            print(f"    Saved to: {text_file.name}\n")
            
        except Exception as e:
            print(f"    Error: {e}\n")
    
    # Save all articles to JSON
    json_file = articles_path / "parsed_articles.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*60}")
    print(f"Parsing complete!")
    print(f"Total articles parsed: {len(all_articles)}")
    print(f"JSON file: {json_file}")
    print(f"{'='*60}")
    
    return all_articles

if __name__ == "__main__":
    articles = parse_all_articles()
    
    # Print preview of first article
    if articles:
        print("\n" + "="*60)
        print("PREVIEW OF FIRST ARTICLE:")
        print("="*60)
        print(f"Title: {articles[0]['title']}")
        print(f"Author: {articles[0]['author']}")
        print(f"Date: {articles[0]['date']}")
        print("\nContent Preview (first 500 characters):")
        print(articles[0]['content'][:500])
        print("...")
