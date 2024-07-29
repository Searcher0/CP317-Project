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

from TestNew_Automation import Accordion_Scraper


# CHANGE PATHS TO SUIT THE NEEDS.

Link = "https://www.nofrills.ca/food/drinks/c/28004"
Section_Title="Water"
Html_file_path=r"C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FILES\Drinks\Water\HTML_Water.txt"
Json_file_path=r"C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\JSON_FILES\Drinks\Water\JSON_Water.json"
retries = 3

# Accordion_Scraper(Link, Section_Title, Html_file_path, retries)
Accordion_Scraper(Link, Section_Title, Html_file_path, Json_file_path, retries)