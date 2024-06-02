"""
Author: Muneeb Zaidi
ID:     169044446
Date:   2024-06-01

Webscraper only for the use on NOfrills.ca
Built completely in python Using beautifulsoup4 webscraping library.
Provides results in a JSON file.
If the Items you want to retreive have a brand associated with them then use the Branded_Products Function.
If the Items you want to retreive DO NOT have a brand associated with them then use the Unbranded_Products Function.
"""


from NoFrills import Branded_products, Unbranded_products

# CHANGE PATHS TO SUIT THE NEEDS.

output_file = r'C:\\CP317 Project\\CP317-Project\\B&S.json'
html_file_path = r'C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FILES\HTML_Butters & Spreads.txt'

# Branded_products(html_file_path, output_file)
# Unbranded_products(html_file_path, output_file)