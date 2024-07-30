import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_loblaws():
    url = "https://www.loblaws.ca/search?search-bar=eggs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch Loblaws page, status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    product_section = soup.find_all('div', {'data-testid': 'price-product-tile'})
    
    for product in product_section:
        print(product.prettify())

if __name__ == "__main__":
    scrape_loblaws()