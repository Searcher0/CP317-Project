from bs4 import BeautifulSoup
import json
import os

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
        img_tag = product_div.find('img')

        if name_tag and price_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

            if (name, price) not in unique_products:
                unique_products.add((name, price))
                products.append({
                    'id': product_id,
                    'name': name,
                    'price': price,
                    'image_url': img_url
                })
                product_id += 1

    # Write the extracted product details to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(products, json_file, indent=4)

    print("Products have been written to JSON file.")

def create_base_and_sub_folders(list_file_path):
    # Read the list file
    with open(list_file_path, 'r') as file:
        lines = [line.strip() for line in file]
    
    # Get the base folder name from the first line
    base_folder_name = lines[0]
    base_path = os.path.join(r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\JSON_FILES', base_folder_name)
    
    # Create the base folder
    os.makedirs(base_path, exist_ok=True)
    
    # Create subfolders and files from the remaining lines
    for folder_name in lines[1:]:
        folder_name = folder_name.strip()  # Strip leading and trailing spaces
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create the file within the folder
        file_name = f'JSON_{folder_name}.json'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write('')  # Create an empty file

def create_folders_and_files(base_path, list_file_path):
    with open(list_file_path, 'r') as file:
        folder_names = [line.strip() for line in file]

    for folder_name in folder_names:
        # Strip leading and trailing spaces from folder names
        folder_name = folder_name.strip()
        
        # Create the folder
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create the file within the folder
        file_name = f'HTML_{folder_name}.txt'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write('')  # Create an empty file


