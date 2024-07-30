import requests
from bs4 import BeautifulSoup
from api.models import db, Walmart
import logging
import json
from sqlalchemy import text

logger = logging.getLogger(__name__)

def scrape_walmart():
    base_url = "https://www.walmart.ca"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.15; rv:104.0) Gecko/20100111 Firefox/104.0"
    }
    
    with open('categories.json', 'r') as file:
        categories = json.load(file)
    
    # Drop and recreate the Walmart table to reset auto-increment ID
    db.session.execute(text('DROP TABLE IF EXISTS walmart'))
    db.create_all()
    logger.info("Cleared existing data from the Walmart table.")

    for category, items in categories.items():
        for item in items:
            search_url = f"{base_url}/search?q={item}"
            response = requests.get(search_url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch Walmart data for query {item}, status code: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            div_content = soup.find_all('div', class_='sans-serif mid-gray relative flex flex-column w-100 hide-child-opacity')
            
            products = []
            
            for product in div_content:
                product_id = product.get('data-item-id', 'N/A')
                product_name_element = product.find('span', {'data-automation-id': 'product-title'})
                product_name = product_name_element.text.strip() if product_name_element else 'N/A'
                price_element = product.find('div', class_='mr1 mr2-xl b black lh-copy f5 f4-l')
                product_price = price_element.text.strip() if price_element else 'N/A'
                
                # Handle different price formats
                if product_price != 'N/A':
                    if '¢' in product_price:
                        product_price = float(product_price.replace('¢', '')) / 100
                    else:
                        product_price = float(product_price.replace('$', '').replace(',', ''))
                else:
                    continue
                
                product_info = {
                    'id': product_id,
                    'name': product_name,
                    'price': product_price,
                    'category': category,
                    'generalized_name': item
                }
                
                products.append(product_info)
            
            for product in products:
                print(product)
            
            # Store data in the database
            db_items = [Walmart(name=product['name'], price=product['price'], category=product['category'], generalized_name=product['generalized_name']) for product in products]
            
            if db_items:
                db.session.bulk_save_objects(db_items)
                db.session.commit()
                logger.info(f"Committed {len(db_items)} Walmart items to the database for category {category}, item {item}.")
            else:
                logger.info(f"No items found for Walmart for category {category}, item {item}.")

if __name__ == "__main__":
    scrape_walmart()