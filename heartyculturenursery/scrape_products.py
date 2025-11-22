import urllib.request
import re
import json
import html

url = "https://www.heartyculturenursery.com/collections/all"
output_file = "assets/products.json"

try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        page_content = response.read().decode('utf-8')

    products = []
    
    # Strategy: Find product titles and then look around them for price and image
    # This is a bit heuristic but should work for a simple task
    
    # Regex for product titles in the grid
    # Looking for <div class="h4 grid-view-item__title ...">Title</div>
    # Or <a href="..." class="grid-view-item__link ..."> ... <span class="visually-hidden">Title</span> ... </a>
    
    # Let's try to find the JSON data first as it seemed to be there
    # Look for var meta = {"product": ...} or similar, or just the raw JSON structure
    
    # Alternative: Regex for the specific structure seen in the image
    # Title
    # Price "Rs. 99.00"
    
    # Let's try to find blocks that look like products
    # Pattern: <div class="grid-view-item ..."> ... </div>
    
    # We will use a simple regex to find all occurrences of prices and the nearest preceding title and image
    
    # Find all product titles
    # <div class="h4 grid-view-item__title product-card__title" aria-hidden="true">Amaranthus Pygmy Torch_Biocarve Seeds</div>
    title_pattern = re.compile(r'<div class="h4 grid-view-item__title product-card__title" aria-hidden="true">([^<]+)</div>')
    titles = title_pattern.findall(page_content)
    
    # Find all prices
    # <span class="price-item price-item--regular">Rs. 99.00</span>
    # Note: There might be sale prices, but let's stick to regular for now or catch the first one
    price_pattern = re.compile(r'<span class="price-item price-item--regular">\s*([^<]+)\s*</span>')
    prices = price_pattern.findall(page_content)
    
    # Find images
    # <img ... src="//www.heartyculturenursery.com/cdn/shop/products/..." ...>
    # We need to be careful to associate them correctly.
    # Let's try to split the HTML by "grid-view-item" to isolate products
    
    product_blocks = page_content.split('class="grid-view-item')
    
    # Skip the first chunk as it's before the first product
    for block in product_blocks[1:]:
        # Title
        title_match = title_pattern.search(block)
        if not title_match:
            # Try alternative title pattern (inside link)
            # <span class="visually-hidden">Title</span>
            title_match = re.search(r'<span class="visually-hidden">([^<]+)</span>', block)
            
        if title_match:
            title = html.unescape(title_match.group(1)).strip()
            
            # Price
            price_match = price_pattern.search(block)
            price = price_match.group(1).strip() if price_match else "Rs. 0.00"
            
            # Image
            # Look for the main image
            img_match = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', block)
            if img_match:
                img_url = img_match.group(1)
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                
                # Clean up image URL (remove size params if possible to get high res, or keep as is)
                # usually ..._300x300.jpg...
                # Let's keep it simple
            else:
                img_url = ""
                
            products.append({
                "title": title,
                "price": price,
                "image": img_url
            })
            
    print(f"Found {len(products)} products.")
    
    # Save to JSON
    with open(output_file, "w") as f:
        json.dump(products, f, indent=2)
        
except Exception as e:
    print(f"Error: {e}")
