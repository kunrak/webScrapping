from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to scrape Amazon search results
def scrape_amazon_selenium(base_url, pages):
    all_data = []
    ranking_start = 1

    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"
        driver.get(url)
        time.sleep(5)  # Allow time for JavaScript to load

        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
        
        for rank, product in enumerate(products, start=ranking_start):
            try:
                brand = product.find_element(By.CSS_SELECTOR, 'span.a-text-normal').text.strip()
            except:
                brand = None

            try:
                price = product.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text.replace(',', '').strip()
                price = int(price)
            except:
                price = None

            try:
                rating = product.find_element(By.CSS_SELECTOR, 'span.a-icon-alt').get_attribute('innerText').split()[0]
                rating = float(rating)
            except:
                rating = None

            try:
                rating_count = product.find_element(By.CSS_SELECTOR, 'span.a-size-base').text.replace(',', '').strip()
                rating_count = int(rating_count)
            except:
                rating_count = None

            try:
                review_count = rating_count  # Assuming rating_count is the review count here
            except:
                review_count = None

            try:
                url = product.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute('href')
            except:
                url = None

            all_data.append({
                'Brand name': brand,
                'Price': price,
                'Rating': rating,
                'Rating count': rating_count,
                'Review count': review_count,
                'Ranking': rank,
                'URL': url
            })
        
        ranking_start += len(products)
        time.sleep(2)
    
    driver.quit()
    return all_data

# URL for the smart locks search on Amazon
base_url = "https://www.amazon.in/s?k=smart+lock"

# Scrape data from the first 5 pages (adjust the number as needed)
data = scrape_amazon_selenium(base_url, 5)

# Create a pandas DataFrame and save it to a CSV file
df = pd.DataFrame(data)
df.to_csv('smart_locks_selenium.csv', index=False)
print(df)
