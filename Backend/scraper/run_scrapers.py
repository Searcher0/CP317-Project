import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from api.app import app, db
from scraper.walmart_scraper import scrape_walmart
from scraper.loblaws_scraper import scrape_loblaws
from scraper.superstore_scraper import scrape_superstore
from scraper.metro_scraper import scrape_metro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_all_scrapers():
    with app.app_context():
        logger.info("Starting to create all tables if they don't exist.")
        db.create_all()  # Ensure all tables are created
        logger.info("Finished creating tables.")
        
        logger.info("Starting Walmart scraper.")
        scrape_walmart()
        logger.info("Finished Walmart scraper.")
        

        # logger.info("Starting Loblaws scraper.")
        # scrape_loblaws()
        # logger.info("Finished Loblaws scraper.")
        
        # logger.info("Starting Superstore scraper.")
        # scrape_superstore()
        # logger.info("Finished Superstore scraper.")
        
        # logger.info("Starting Metro scraper.")
        # scrape_metro()
        # logger.info("Finished Metro scraper.")

if __name__ == '__main__':
    run_all_scrapers()