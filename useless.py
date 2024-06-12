import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import certifi

# Function to get the HTML content of a page
def get_html(url, headers):
    response = requests.get(url, headers=headers, verify=certifi.where())
    return response.text

# Function to parse the HTML and extract product data
def parse_html(html, ranking_start):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    data = []
    for rank, product in enumerate(products, start=ranking_start):
        try:
            brand = product.find('span').text.strip()
        except AttributeError:
            brand = None

        try:
            price = product.find('span', class_='a-price-whole').text.replace(',', '').strip()
            price = int(price)
        except (AttributeError, ValueError):
            price = None

        try:
            rating = product.find('span', class_='a-icon-alt').text.split()[0]
            rating = float(rating)
        except (AttributeError, ValueError):
            rating = None

        try:
            rating_count = product.find('span', {'class': 'a-size-base'}).text.replace(',', '').strip()
            rating_count = int(rating_count)
        except (AttributeError, ValueError):
            rating_count = None

        try:
            review_count = product.find('span', {'class': 'a-size-base'}).text.replace(',', '').strip()
            review_count = int(review_count)
        except (AttributeError, ValueError):
            review_count = None
        
        try:
            url = 'https://www.amazon.in' + product.find('a', class_='a-link-normal')['href']
        except AttributeError:
            url = None

        data.append({
            'Brand name': brand,
            'Price': price,
            'Rating': rating,
            'Rating count': rating_count,
            'Review count': review_count,
            'Ranking': rank,
            'URL': url
        })
    
    return data

# Main function to scrape multiple pages
def scrape_amazon(base_url, pages, headers):
    all_data = []
    ranking_start = 1

    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"
        html = get_html(url, headers)
        page_data = parse_html(html, ranking_start)
        all_data.extend(page_data)
        ranking_start += len(page_data)
        
        # Sleep to prevent getting blocked
        time.sleep(2)
    
    return all_data

# URL for the smart locks search on Amazon
base_url = "https://www.amazon.in/s?k=smart+lock"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Scrape data from the first 20 pages
data = scrape_amazon(base_url, 20, headers)

# Create a pandas DataFrame and save it to a CSV file
print('end.............................')
df = pd.DataFrame(data)
df_ffill = df.fillna(method="ffill")
df.to_csv('smart_locks.csv', index=False)