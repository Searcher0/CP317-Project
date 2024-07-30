import requests
from bs4 import BeautifulSoup
from api.models import db, Superstore
import logging

logger = logging.getLogger(__name__)

def scrape_superstore():
    url = "https://www.superstore.ca/en/grocery/fruits-vegetables/fruits/N-3851"
    response = requests.get(url)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch Superstore page, status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    items = []
    
    for product in soup.select('.product'):
        name = product.select_one('.product-name').text.strip()
        price = product.select_one('.price-current').text.strip()
        category = 'produce'
        generalized_name = 'Fruits'
        
        item = Superstore(
            name=name,
            price=float(price.replace('$', '')),
            category=category,
            generalized_name=generalized_name
        )
        items.append(item)
    
    if items:
        db.session.bulk_save_objects(items)
        db.session.commit()
        logger.info(f"Committed {len(items)} Superstore items to the database.")
    else:
        logger.info("No items found for Superstore.")