import requests

# URL to scrape
url = "https://www.nofrills.ca/food/fruits-vegetables/fresh-vegetables/c/28195?navid=flyout-L3-Fresh-Vegetables"

# Fetch HTML content
response = requests.get(url)
html_content = response.text

# Save HTML content to a file
file_path = "C:/CP317 Project/CP317-Project/test_1.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"HTML content saved to {file_path}")
