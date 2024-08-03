import requests
from pymongo import MongoClient
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import json
import re

# Setup logging
logger = logging.getLogger('scraper.mongoDB_to_MySQL')
logging.basicConfig(level=logging.INFO)

# MongoDB connection
mongo_client = MongoClient("mongodb+srv://Muneeb:mzlaurier@groceryguru.qdx3gmj.mongodb.net/")
mongo_db = mongo_client['Nofrills_Directory']

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

# Define NoFrills table structure
class NoFrills(Base):
    __tablename__ = 'nofrills'
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

# Function to find the generalized name and category
def find_generalized_name_and_category(product_name, categories):
    for category, items in categories.items():
        for item in items:
            if item.lower() in product_name.lower():
                return item, category
    return 'unknown', 'unknown'

# Function to extract price
def extract_price(price_str):
    match = re.search(r'\$(\d+\.\d+)\$', price_str)
    if match:
        return float(match.group(1))
    return None

def create_table():
    # Create the table if it doesn't exist
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Created the nofrills table.")

def get_data_from_mongodb():
    # Get list of collections
    collections = mongo_db.list_collection_names()
    logger.info(f"MongoDB Collections: {collections}")

    all_products = []

    # Iterate over each collection
    for collection_name in collections:
        collection = mongo_db[collection_name]

        logger.info(f"Processing collection: {collection_name}")

        # Retrieve data from MongoDB
        documents = list(collection.find())
        logger.info(f"Retrieved {len(documents)} documents from collection: {collection_name}")

        if not documents:
            logger.warning(f"No documents found in collection: {collection_name}")
            continue

        # Log the structure of the documents
        logger.info(f"Structure of a sample document from collection {collection_name}: {documents[0] if documents else 'No documents to show'}")

        # Process data
        for document in documents:
            sub_category = document.get('sub_category', 'N/A')
            products = document.get('products', [])
            if not products or not isinstance(products[0], list):
                logger.warning(f"No products found or invalid format in document from collection: {collection_name}")
                continue

            logger.info(f"Products structure in document: {products[0]}")

            for product in products[0]:
                product_id = product.get('id', 'N/A')
                product_name = product.get('name', 'N/A')
                product_price_str = product.get('price_product_tile', 'N/A')
                generalized_name, category = find_generalized_name_and_category(product_name, categories)
                
                # Extract and handle different price formats
                product_price = extract_price(product_price_str)
                if product_price is None:
                    logger.error(f"Price extraction error for product {product_name}: {product_price_str}")
                    continue
                
                # Create product_info dictionary
                product_info = {
                    'name': product_name,
                    'price': product_price,
                    'category': category,
                    'generalized_name': generalized_name,
                    'source_collection': collection_name
                }

                logger.info(f"Processed product: {product_info}")
                all_products.append(product_info)

    return all_products

def insert_data_to_mysql(products):
    db_items = [NoFrills(
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

def migrate_data():
    # Step 1: Create Table
    create_table()

    # Step 2: Get Data from MongoDB
    products = get_data_from_mongodb()
    logger.info(f"Total products to insert: {len(products)}")

    # Step 3: Insert Data into MySQL
    insert_data_to_mysql(products)

    print("Data migration completed successfully!")

if __name__ == "__main__":
    migrate_data()
