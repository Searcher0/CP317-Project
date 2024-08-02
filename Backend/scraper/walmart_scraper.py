import requests
from bs4 import BeautifulSoup
from api.models import db, Walmart
import logging
import json
from sqlalchemy import text
import random
import time

logger = logging.getLogger(__name__)

def scrape_walmart():
    base_url = "https://www.walmart.ca"
    
    with open('categories.json', 'r') as file:
        categories = json.load(file)
    
    # No need to drop and recreate the Walmart table
    logger.info("Starting to scrape Walmart data.")

    for category, items in categories.items():
        for item in items:
            number = random.randint(20100100, 20101999)
            headers = {"User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/{number} Firefox/104.0"}
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
            for product in products:
                existing_item = Walmart.query.filter_by(name=product['name']).first()
                if existing_item:
                    existing_item.price = product['price']
                    db.session.merge(existing_item)
                else:
                    new_item = Walmart(name=product['name'], price=product['price'], category=product['category'], generalized_name=product['generalized_name'])
                    db.session.add(new_item)
            
            db.session.commit()
            logger.info(f"Processed {len(products)} Walmart items for category {category}, item {item}.")
            # time.sleep(30) # sleep for 30 seconds to avoid getting blocked by Walmart

if __name__ == "__main__":
    scrape_walmart()