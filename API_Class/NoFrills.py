from bs4 import BeautifulSoup
import json

def Branded_products(html_file_path, output_file):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    product_divs = soup.find_all('div', class_='css-0')
    product_id = 1
    unique_products = set()

    for product_div in product_divs:
        name_tag = product_div.find('h3', {'data-testid': 'product-title'})
        price_tag = product_div.find('p', {'data-testid': 'product-package-size'})
        brand_tag = product_div.find('p', {'data-testid': 'product-brand'})
        image_tag = product_div.find('div', {'data-testid': 'product-image'}).find('img') if product_div.find('div', {'data-testid': 'product-image'}) else None

        if name_tag and price_tag and image_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            brand = brand_tag.get_text(strip=True) if brand_tag else "No brand"
            image_url = image_tag['src']

            if (name, price) not in unique_products:
                unique_products.add((name, price, brand))
                products.append({
                    'id': product_id,
                    'name': name,
                    'price': price,
                    'brand': brand,
                    'image_url': image_url
                })
                product_id += 1
    
    with open(output_file, 'w') as json_file:
        json.dump(products, json_file, indent=4)

    print("Products have been written to JSON file.")




def Unbranded_products(html_file_path, output_file):
# The following Code for Products that don't have Brands
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

# # Extract product information
    products = []
    product_divs = soup.find_all('div', class_='css-0')
    product_id = 1
    unique_products = set()

    for product_div in product_divs:
        name_tag = product_div.find('h3', {'data-testid': 'product-title'})
        price_tag = product_div.find('p', {'data-testid': 'product-package-size'})
        image_tag = product_div.find('div', {'data-testid': 'product-image'}).find('img') if product_div.find('div', {'data-testid': 'product-image'}) else None

        if name_tag and price_tag and image_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            image_url = image_tag['src']

            
            if (name, price) not in unique_products:
                unique_products.add((name, price))
                products.append({
                    'id': product_id,
                    'name': name,
                    'price': price,
                    'image_url': image_url
                })
                product_id += 1

    # Write the extracted product details to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(products, json_file, indent=4)

    print("Products have been written to JSON file.")