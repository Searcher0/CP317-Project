from pymongo import MongoClient
from tabulate import tabulate
import re

# Connect to MongoDB
try:
    client = MongoClient("mongodb+srv://Muneeb:mzlaurier@groceryguru.qdx3gmj.mongodb.net/?retryWrites=true&w=majority")
    db = client['Nofrills_Directory']
    print("Connected to MongoDB server successfully")
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    exit(1)

# Function to extract numerical price from a price string
def extract_price(price_string):
    match = re.search(r"\$([0-9]+(\.[0-9]+)?)", price_string)
    if match:
        return float(match.group(1))
    return float('inf')  # Return a large number if no price is found

# Function to search for items based on a search string
def search_products(search_string):
    collections = db.list_collection_names()  # Get all collection names
    search_results = []

    for collection_name in collections:
        print(f"Searching in collection: {collection_name}")
        collection = db[collection_name]
        sub_categories = collection.find()

        for sub_category in sub_categories:
            if 'products' in sub_category and isinstance(sub_category['products'], list):
                for product_list in sub_category['products']:
                    for product in product_list:
                        if isinstance(product, dict) and search_string.lower() in product.get('name', '').lower():
                            search_results.append({
                                'Collection': collection_name,
                                'ID': product.get('id'),
                                'Name': product.get('name'),
                                'Price': product.get('price'),
                                'Image URL': product.get('image_url'),
                                'Image Alt': product.get('image_alt'),
                                'Price Value': extract_price(product.get('price'))
                            })
    
    # Sort the results by price (least to greatest)
    search_results.sort(key=lambda x: x['Price Value'])
    
    return search_results

# Main execution
if __name__ == "__main__":
    # Example usage of search function
    search_string = "cream"
    results = search_products(search_string)
    if not results:
        print("No results found.")
    else:
        # Print the results in a table format
        headers = ["Collection", "ID", "Name", "Price", "Image URL", "Image Alt"]
        table = [result.values() for result in results]
        print(tabulate(table, headers=headers, tablefmt="grid"))
