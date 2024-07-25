import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from NoFrills import Branded_products, Unbranded_products


def Accordion_Scraper(base_link, accordion_title, output_file, json_output_file, retries):
    # Set up the WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    attempt = 0
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

            # Wait for the new page to load completely by checking for the presence of the body element
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Additional wait to ensure all dynamic elements are loaded
            time.sleep(5)

            # Extract the live HTML content from the specific div (product grid)
            specific_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='product-grid']")
            html_content = specific_div.get_attribute('outerHTML')

            # Save the HTML content to a file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(html_content)

            print('HTML content of the specific div saved to', output_file)

            Branded_products(output_file, json_output_file)
            break  # Exit the loop if successful

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

# Accordion_Scraper(
#     base_link="https://www.nofrills.ca/food/bakery/c/28002",
#     accordion_title="Cakes",
#     output_file=r"C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\HTML_FILES\Bakery\Cakes\HTML_Cakes.txt",
#     json_output_file=r"C:\Users\User\OneDrive\Documents\GitHub\CP317-Project\API_Class\JSON_FILES\Bakery\Cakes\JSON_Cakes.json"
# )
