from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_specific_div(Link, output_file):
    # Set up the WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        # Navigate directly to the page URL
        driver.get(Link)

        # Wait for the page to load completely
        time.sleep(5)

        # Find the specific div by data-testid attribute
        specific_div = driver.find_element("css selector", "div[data-testid='product-grid']")

        # Extract the HTML content from the specific div
        html_content = specific_div.get_attribute('outerHTML')

        # Save the HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print('HTML content of the specific div saved to', output_file)

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
scrape_specific_div('https://www.nofrills.ca/food/bakery/bagels-croissants-english-muffins/c/28149', 'C:/Users/User/OneDrive/Documents/GitHub/CP317-Project/API_Class/HTML_FILES/Bakery/Bagels, Croissants & English Muffins/HTML_Bagels, Croissants & English Muffins.txt')
