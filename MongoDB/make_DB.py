import os
import json
from pymongo import MongoClient

# Connect to MongoDB
try:
    client = MongoClient("mongodb+srv://Muneeb:mzlaurier@groceryguru.qdx3gmj.mongodb.net/")
    db = client['Nofrills_Directory']
    print("Connected to MongoDB server successfully")
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    exit(1)

# Main folder path
main_folder = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\JSON_FILES'
empty_files = []

# Function to read JSON files and insert into MongoDB
def insert_data_from_json(sub_category_path, category_name, sub_category_name):
    products = []
    for json_file in os.listdir(sub_category_path):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(sub_category_path, json_file)
            try:
                with open(json_file_path, 'r') as file:
                    content = file.read()
                    if not content.strip():
                        print(f"JSON file is empty: {json_file_path}")
                        empty_files.append(json_file_path)
                        continue
                    data = json.loads(content)
                    products.append(data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {json_file_path}")
            except Exception as e:
                print(f"Error reading file {json_file_path}: {e}")

    if products:
        existing_sub_category = db[category_name].find_one({'sub_category': sub_category_name})
        if existing_sub_category:
            print(f"Sub-category '{sub_category_name}' already exists in collection '{category_name}'. Skipping...")
        else:
            db[category_name].insert_one({
                'sub_category': sub_category_name,
                'products': products
            })
            print(f"Inserted data from '{sub_category_name}' into collection '{category_name}'")
    else:
        print(f"Sub-category '{sub_category_name}' does not contain any JSON files.")

# Traverse the directory structure
for category in os.listdir(main_folder):
    category_path = os.path.join(main_folder, category)
    if os.path.isdir(category_path):
        for sub_category in os.listdir(category_path):
            sub_category_path = os.path.join(category_path, sub_category)
            if os.path.isdir(sub_category_path):
                insert_data_from_json(sub_category_path, category, sub_category)

print("Data transfer completed.")
if empty_files:
    print("The following JSON files were empty:")
    for file in empty_files:
        print(file)
