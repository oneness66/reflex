import requests
from bs4 import BeautifulSoup

url = "https://vedabase.io/en/library/sb/1/1/1/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

headers = soup.find_all('h2')
for h2 in headers:
    if "purport" in h2.get_text(strip=True).lower():
        print("Found Purport H2")
        curr = h2.find_next_sibling()
        count = 0
        while curr and count < 10:
            print(f"Sibling {count}: <{curr.name}> Class: {curr.get('class')}")
            if curr.name == 'div':
                text = curr.get_text(strip=True)
                print(f"  Text start: {text[:50]}...")
            curr = curr.find_next_sibling()
            count += 1
