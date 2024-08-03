import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
import os
from bs4 import BeautifulSoup
import json
import re

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

def create_table():
    # Create the table if it doesn't exist
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Created the loblaws table.")

def Loblaws_Scraper():
    base_link = "https://www.loblaws.ca/food/c/27985"  # Hard-coded base link
    retries = 3  # Hard-coded retries

    # Path to the ChromeDriver
    chrome_driver_path = r"C:\Users\User\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe" # update this if you want to run the scraper
    
    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path))
    file_path = r"Backend\scraper\loblaws.txt"
    attempt = 0
    page_number = 1
    all_html_content = []

    while attempt < retries:
        try:
            logger.info(f"Attempting to access {base_link}")
            driver.get(base_link)
            time.sleep(10)  # Delay to allow the page to load fully
            logger.info(f"Successfully accessed {base_link}")

            while True:
                logger.info(f"Scraping page {page_number}")
                html_content = grab_html_content(driver)
                if html_content:
                    all_html_content.append(html_content)
                    logger.info(f"Scraped HTML content from page {page_number}")
                    page_number += 1
                    with open(file_path, 'w', encoding='utf-8') as file:
                        for content in all_html_content:
                            file.write(content + '\n')
                    print(f"HTML content saved to {file_path}")
                else:
                    logger.info(f"Failed to grab HTML content for page {page_number}")

                if not go_to_next_page(driver):
                    break

            break
        except Exception as e:
            logger.error(f"An error occurred on attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt < retries:
                logger.info("Retrying...")
            else:
                logger.info("Max retries reached. Exiting.")
        finally:
            time.sleep(1)

    driver.quit()
    parse_and_insert_data_from_file()

def go_to_next_page(driver):
    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, "nav[data-testid='pagination'] a[aria-label='Next Page']")
        if next_page_link.get_attribute('aria-disabled') == "true":
            logger.info("No more pages to navigate.")
            return False
        else:
            logger.info("Navigating to next page.")
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(5)  # Increased wait time for next page to load
            return True
    except NoSuchElementException:
        logger.info("Next page link not found.")
        return False

def grab_html_content(driver):
    try:
        wait = WebDriverWait(driver, 40)
        logger.info("Waiting for product grid to load.")
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-tile-skeleton']")))
        product_grid = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-grid']")))
        time.sleep(2)  # Additional wait to ensure the content has loaded
        html_content = product_grid.get_attribute('outerHTML')
        return html_content
    except TimeoutException:
        logger.error("Timeout while waiting for the product grid to load.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while grabbing HTML content: {e}")
        return None

def parse_and_insert_data_from_file():
    try:
        file_path = r"Backend\scraper\loblaws.txt"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        products = extract_product_info_from_html(content)
        insert_data_to_mysql(products)
    except Exception as e:
        logger.error(f"An error occurred while parsing and inserting data from file: {e}")

def extract_product_info_from_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        product_elements = soup.select("div.chakra-linkbox")
        file_path = r'Backend\categories.json'
        # Load categories.json
        with open(file_path) as f:
            categories = json.load(f)

        products = []
        for product in product_elements:
            try:
                product_name = product.select_one("h3[data-testid='product-title']").get_text(strip=True)
                price_element = product.select_one("div[data-testid='price-product-tile'] span[data-testid='regular-price']")
                product_price = price_element.get_text(strip=True) if price_element else 'N/A'
                
                if product_price != 'N/A':
                    # Extract only the first valid float number from the string
                    price_match = re.search(r'\d+(\.\d{1,2})?', product_price)
                    if price_match:
                        product_price = float(price_match.group(0).replace('\n', ''))
                    else:
                        continue

                # Find the generalized name and category
                generalized_name, category = find_generalized_name_and_category(product_name, categories)
                
                # Create product_info dictionary
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
    except Exception as e:
        logger.error(f"An error occurred while extracting product info from HTML: {e}")
        return []

def find_generalized_name_and_category(product_name, categories):
    for category, items in categories.items():
        for item in items:
            if item.lower() in product_name.lower():
                return item, category
    return 'unknown', 'unknown'

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
    # Step 1: Create Table
    # create_table()

    # Step 2: Scrape Data and Insert into MySQL
    Loblaws_Scraper()
