import json
from collections import defaultdict

# Path to the JSON file with products
input_file = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\Butters & Spreads.json'
# Path to the JSON file to save duplicates
output_file = r'C:\CP317 Project\CP317-Project\duplicates_1.json'

# Read the products from the JSON file
with open(input_file, 'r') as json_file:
    products = json.load(json_file)

# Find duplicates
seen_products = set()
duplicates = []

for product in products:
    product_key = (product['name'], product['price'])
    if product_key in seen_products:
        duplicates.append(product)
        print(product_key)
    else:
        seen_products.add(product_key)

with open(output_file, 'w') as json_file:
    json.dump(duplicates, json_file, indent=4)

print("Duplicates have been written to JSON file.")
