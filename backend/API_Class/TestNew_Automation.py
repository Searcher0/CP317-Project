import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from NoFrills import Branded_products

def Accordion_Scraper(base_link, accordion_title, output_file, json_output_file, retries):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    attempt = 0
    page_number = 1
    all_html_content = ""

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("")

        # Clear the content of the JSON file before starting
    with open(json_output_file, 'w', encoding='utf-8') as file:
        file.write("[]")

    while attempt < retries:
        try:
            driver.get(base_link)

            wait = WebDriverWait(driver, 40)
            accordion_xpath = f"//p[text()='{accordion_title}']/ancestor::div[@data-testid='accordion-item']"
            accordion = wait.until(
                EC.presence_of_element_located((By.XPATH, accordion_xpath))
            )

            print("Located accordion outer HTML:")
            print(accordion.get_attribute('outerHTML'))

            accordion_button = accordion.find_element(By.CSS_SELECTOR, "button.chakra-accordion__button")
            driver.execute_script("arguments[0].click();", accordion_button)

            see_all_link_xpath = f"{accordion_xpath}//a[text()='See All']"
            see_all_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, see_all_link_xpath))
            )

            href = see_all_link.get_attribute('href')
            new_page_link = urljoin(base_link, href)

            driver.get(new_page_link)
            time.sleep(10)  # Increased delay for the first page
            while True:
                html_content = grab_html_content(driver)
                if html_content:
                    all_html_content += html_content
                    print(f'HTML content of page {page_number} saved.')
                    page_number += 1
                else:
                    print(f"Failed to grab HTML content for page {page_number}")

                if not go_to_next_page(driver):
                    break

            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(all_html_content)
            print(f"HTML content saved to {output_file}")
            Branded_products(output_file, json_output_file)
            break
        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt < retries:
                print("Retrying...")
            else:
                print("Max retries reached. Exiting.")
        finally:
            time.sleep(1)

    driver.quit()

def go_to_next_page(driver):
    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, "nav[data-testid='pagination'] a[aria-label='Next Page']")
        if next_page_link.get_attribute('aria-disabled') == "true":
            return False
        else:
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(3)
            return True
    except NoSuchElementException:
        return False

def grab_html_content(driver):
    try:
        wait = WebDriverWait(driver, 40)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-tile-skeleton']")))
        specific_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='product-grid']")))
        time.sleep(2)  # Additional wait to ensure the content has loaded
        html_content = specific_div.get_attribute('outerHTML')
        return html_content
    except TimeoutException:
        print("Timeout while waiting for the product grid to load.")
        return None
    except Exception as e:
        print(f"An error occurred while grabbing HTML content: {e}")
        return None

