import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from NoFrills import Branded_products, Unbranded_products


def Accordion_Scraper(base_link, accordion_title, output_file, json_output_file, retries):

    # Set up the WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    attempt = 0
    page_number = 1
    all_html_content = ""

    while attempt < retries:
        try:
            # Navigate to the base page URL
            driver.get(base_link)

            # Wait for the accordion with the specific title to be present
            wait = WebDriverWait(driver, 30)  # Adjust timeout as needed
            accordion_xpath = f"//p[text()='{accordion_title}']/ancestor::div[@data-testid='accordion-item']"
            accordion = wait.until(
                EC.presence_of_element_located((By.XPATH, accordion_xpath))
            )

            # Print the outer HTML of the located accordion for debugging
            print("Located accordion outer HTML:")
            print(accordion.get_attribute('outerHTML'))

            # Click the accordion button to expand it using JavaScript to avoid interception issues
            accordion_button = accordion.find_element(By.CSS_SELECTOR, "button.chakra-accordion__button")
            driver.execute_script("arguments[0].click();", accordion_button)

            # Wait for the 'See All' link to be present and clickable
            see_all_link_xpath = f"{accordion_xpath}//a[text()='See All']"
            see_all_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, see_all_link_xpath))
            )

            # Get the href attribute to navigate to the new page
            href = see_all_link.get_attribute('href')
            new_page_link = urljoin(base_link, href)

            # Navigate to the new page URL
            driver.get(new_page_link)

            while True:
                html_content = grab_html_content(driver)
                if html_content:
                    # Append the HTML content to all_html_content
                    all_html_content += html_content
                    print(f'HTML content of page {page_number} saved.')
                    page_number += 1
                else:
                    print(f"Failed to grab HTML content for page {page_number}")

                if not go_to_next_page(driver):
                    break

            # Process all collected HTML with Branded_products after pagination ends
            Branded_products(all_html_content, json_output_file)
            break
        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt < retries:
                print("Retrying...")
            else:
                print("Max retries reached. Exiting.")
        finally:
            time.sleep(1)  # Adding a slight delay before retries

    # Close the WebDriver
    driver.quit()

def go_to_next_page(driver):
    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, "nav[data-testid='pagination'] a[aria-label='Next Page']")
        if next_page_link.get_attribute('aria-disabled') == "true":
            return False  # No more pages
        else:
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(2)  # Small delay to ensure the next page loads properly
            return True
    except NoSuchElementException:
        return False  # No 'Next Page' link found

def grab_html_content(driver):
    try:
        wait = WebDriverWait(driver, 30)  # Adjust timeout as needed
        specific_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-grid']")))
        html_content = specific_div.get_attribute('outerHTML')
        return html_content
    except Exception as e:
        print(f"An error occurred while grabbing HTML content: {e}")
        return None
