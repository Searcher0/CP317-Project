import requests
from bs4 import BeautifulSoup
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class API:
    def __init__(self, url: str):
        self.url = url

    def get_html(self) -> str:
        """
        Fetches the HTML content of the main page URL.

        Returns:
            str: The HTML content of the page.
        """
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parses the HTML content using BeautifulSoup.

        Args:
            html (str): The HTML content to be parsed.

        Returns:
            BeautifulSoup: The parsed HTML content.
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_product_section(self, parsed_html: BeautifulSoup) -> BeautifulSoup:
        """
        Finds and returns the product section from the parsed HTML content.

        Args:
            parsed_html (BeautifulSoup): The parsed HTML content.

        Returns:
            BeautifulSoup: The product section of the HTML content.
        """
        raise NotImplementedError("This method should be implemented in a subclass.")

class HTMLFetcher(API):
    def fetch_html(self) -> str:
        logger.info(f"Fetching HTML content from URL: {self.url}")
        return self.get_html()

class HTMLParser(API):
    def parse_html_content(self, html: str) -> BeautifulSoup:
        logger.info("Parsing HTML content")
        return self.parse_html(html)

class ProductNavigator(API):
    def find_product_section(self, parsed_html: BeautifulSoup) -> BeautifulSoup:
        logger.info("Navigating to the product section")
        
        # Try to find the 'Shop By Activity' section
        product_section = parsed_html.find('div', class_='tile-container')
        if product_section:
            logger.info("Product section found under 'Shop By Activity'")
            return product_section

        # Try to find the 'Shop By Department' section
        product_section = parsed_html.find('div', class_='pod-container')
        if product_section:
            logger.info("Product section found under 'Shop By Department'")
            return product_section
        
        logger.warning("Product section not found")
        return None

class ProductDataScraper:
    def __init__(self, product_section: BeautifulSoup):
        self.product_section = product_section

    def scrape_products(self) -> list:
        logger.info("Scraping product data")
        products = []
        # Placeholder for product scraping logic
        # Assuming each product is within an element with class 'product'
        product_elements = self.product_section.find_all('a')
        for element in product_elements:
            # Extract product details, assuming each has name and price
            name = element.find('p', class_='tile-text').text.strip()
            # Placeholder price extraction logic (if price is available)
            price = None
            products.append({'name': name, 'price': price})
        return products

class SQLDatabaseHandler:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.products_table = Table('products', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String(255)),
                                    Column('price', Float, nullable=True))
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store_data(self, data: list):
        logger.info("Storing data in the database")
        session = self.Session()
        try:
            for item in data:
                ins = self.products_table.insert().values(name=item['name'], price=item['price'])
                session.execute(ins)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"An error occurred: {e}")
        finally:
            session.close()

# Example usage
if __name__ == "__main__":
    url = "https://www.dollarama.com"
    
    # Fetch HTML
    html_fetcher = HTMLFetcher(url)
    html_content = html_fetcher.fetch_html()
    
    # Parse HTML
    html_parser = HTMLParser(url)
    parsed_html = html_parser.parse_html_content(html_content)
    
    # Find Product Section
    product_navigator = ProductNavigator(url)
    product_section = product_navigator.find_product_section(parsed_html)
    
    # Scrape Product Data
    if product_section:
        product_scraper = ProductDataScraper(product_section)
        product_data = product_scraper.scrape_products()
        
        # Store Data in SQL Database
        db_url = "mysql+pymysql://root:Success786!!@localhost/dollarama_products"
        db_handler = SQLDatabaseHandler(db_url)
        db_handler.store_data(product_data)
    else:
        logger.error("Product section not found in the provided URL")
