"""Fetch data from WolframAlpha."""
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_alt_texts(section):
    img_elements = section.find_elements(By.TAG_NAME, "img")
    return [img.get_attribute("alt") for img in img_elements if img.get_attribute("alt")]

def main(num_input):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.wolframalpha.com/input?i={num_input}")

    wait = WebDriverWait(driver, 10)
    closed_forms_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Possible closed forms']")))

    # Find the parent section of the "Possible closed forms" span.
    section = closed_forms_element.find_element(By.XPATH, "./ancestor::section")

    # Get initial alt-texts
    alt_texts = get_alt_texts(section)

    # Check for and click the "More" link if it exists
    try:
        more_link = section.find_element(By.XPATH, ".//a[contains(text(), 'More')]")
        driver.execute_script("arguments[0].click();", more_link)
        
        wait.until(EC.staleness_of(closed_forms_element))
        closed_forms_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Possible closed forms']")))
        section = closed_forms_element.find_element(By.XPATH, "./ancestor::section")
        
        # Get additional alt-texts
        alt_texts.extend(get_alt_texts(section))
    except (NoSuchElementException, TimeoutException):
        pass

    # Filter alt-texts to only include those with ≈ symbol
    filtered_alt_texts = [text for text in alt_texts if '≈' in text]

    for alt_text in filtered_alt_texts:
        print(alt_text)
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find possible closed forms for a given number using Wolfram Alpha.")
    parser.add_argument("number", type=str, help="The number to find possible closed forms for")
    args = parser.parse_args()

    print(f"Fetching for {args.number}...")
    main(args.number)
