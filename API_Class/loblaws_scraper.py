import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import json

# Setup logging
logger = logging.getLogger('scraper.loblaws')
logging.basicConfig(level=logging.INFO)

# MySQL connection configuration
class Config:
    DB_HOST = 'srv1207.hstgr.io'
    DB_USER = 'u593794933_grocery_guru'
    DB_PASSWORD = 'Grocery_guru1'
    DB_NAME = 'u593794933_grocery_guru'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create MySQL engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

# Define Loblaws table structure
class Loblaws(Base):
    __tablename__ = 'loblaws'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Float)
    category = Column(String(255))
    generalized_name = Column(String(255))
    source_collection = Column(String(255))

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Load categories.json
with open('categories.json') as f:
    categories = json.load(f)

def find_generalized_name_and_category(product_name, categories):
    for category, items in categories.items():
        for item in items:
            if item.lower() in product_name.lower():
                return item, category
    return 'unknown', 'unknown'

def create_table():
    # Create the table if it doesn't exist
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Created the loblaws table.")

def scrape_loblaws(base_link, retries):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    attempt = 0
    page_number = 1
    all_products = []

    while attempt < retries:
        try:
            driver.get(base_link)
            while True:
                products = grab_html_content(driver)
                if products:
                    all_products.extend(products)
                    print(f'HTML content of page {page_number} saved.')
                    page_number += 1
                else:
                    print(f"Failed to grab HTML content for page {page_number}")

                if not go_to_next_page(driver):
                    break

            logger.info(f"Total products scraped: {len(all_products)}")
            insert_data_to_mysql(all_products)
            break
        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt < retries:
                print("Retrying...")
            else:
                print("Max retries reached. Exiting.")
        finally:
            time.sleep(1)

    driver.quit()

def go_to_next_page(driver):
    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, "nav[data-testid='pagination'] a[aria-label='Next Page']")
        if next_page_link.get_attribute('aria-disabled') == "true":
            return False
        else:
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(3)
            return True
    except NoSuchElementException:
        return False

def grab_html_content(driver):
    try:
        wait = WebDriverWait(driver, 40)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-tile-skeleton']")))
        specific_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-grid']")))
        time.sleep(2)
        product_elements = specific_div.find_elements(By.CSS_SELECTOR, "div.product-tracking")
        
        products = []
        for product in product_elements:
            try:
                product_id = product.get_attribute('data-track-product-id')
                product_data = json.loads(product.get_attribute('data-track-products-array'))[0]
                product_name = product_data.get('productName', 'N/A')
                product_price = product_data.get('productPrice', 'N/A')

                if product_price != 'N/A':
                    product_price = float(product_price.replace('$', '').replace(',', ''))
                else:
                    continue

                generalized_name, category = find_generalized_name_and_category(product_name, categories)

                product_info = {
                    'name': product_name,
                    'price': product_price,
                    'category': category,
                    'generalized_name': generalized_name,
                    'source_collection': 'loblaws'
                }

                products.append(product_info)
            except Exception as e:
                logger.error(f"Error processing product data: {e}")
                continue
        
        return products
    except TimeoutException:
        print("Timeout while waiting for the product grid to load.")
        return None
    except Exception as e:
        print(f"An error occurred while grabbing HTML content: {e}")
        return None

def insert_data_to_mysql(products):
    db_items = [Loblaws(
        name=product['name'],
        price=product['price'],
        category=product['category'],
        generalized_name=product['generalized_name'],
        source_collection=product['source_collection']
    ) for product in products]

    if db_items:
        session.bulk_save_objects(db_items)
        session.commit()
        logger.info(f"Committed {len(db_items)} items to the database.")
    else:
        logger.info(f"No items to commit to the database.")

if __name__ == "__main__":
    base_link = "https://www.loblaws.ca/food/c/27985"  # Set your Loblaws base link
    retries = 3

    # Step 1: Create Table
    create_table()

    # Step 2: Scrape Data and Insert into MySQL
    scrape_loblaws(base_link, retries)
