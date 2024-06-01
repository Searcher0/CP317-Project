from bs4 import BeautifulSoup
import json

# Read HTML content from a file
html_file_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FRESHVEG.txt'  # Update the path to your HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract product information
products = []
product_divs = soup.find_all('div', class_='css-0')
product_id = 1
unique_products = set()

for product_div in product_divs:
    name_tag = product_div.find('h3', {'data-testid': 'product-title'})
    price_tag = product_div.find('p', {'data-testid': 'product-package-size'})

    if name_tag and price_tag:
        name = name_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        
        if (name, price) not in unique_products:
            unique_products.add((name, price))
            products.append({
                'id': product_id,
                'name': name,
                'price': price
            })
            product_id += 1

# Write the extracted product details to a JSON file
output_file = 'C:\\CP317 Project\\CP317-Project\\products.json' # CHANGE THIS TO THE PATH YOU WANT. 
with open(output_file, 'w') as json_file:
    json.dump(products, json_file, indent=4)

print("Products have been written to JSON file.")