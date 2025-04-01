
# prompt:
# selenium script to cycle through paginated table elements and save to a dataframe python pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

def extract_table_data(driver, table_xpath):
    """Extracts table data from the current page."""
    table = driver.find_element(By.XPATH, table_xpath)
    rows = table.find_elements(By.TAG_NAME, 'tr')
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        cols = [col.text for col in cols]
        data.append(cols)
    return data

def navigate_to_next_page(driver, next_button_xpath):
    """Navigates to the next page if available."""
    try:
        next_button = driver.find_element(By.XPATH, next_button_xpath)
        next_button.click()
        time.sleep(2)  # Wait for the page to load
        return True
    except NoSuchElementException:
        return False

def scrape_paginated_table(url, table_xpath, next_button_xpath):
    """Scrapes data from a paginated table and returns a Pandas DataFrame."""
    driver = webdriver.Chrome()  # Or any other browser driver
    driver.get(url)
    all_data = []

    while True:
        table_data = extract_table_data(driver, table_xpath)
        all_data.extend(table_data)
        if not navigate_to_next_page(driver, next_button_xpath):
            break

    driver.quit()
    df = pd.DataFrame(all_data)
    return df

if __name__ == '__main__':
    url = 'YOUR_URL_HERE'
    table_xpath = 'YOUR_TABLE_XPATH_HERE'
    next_button_xpath = 'YOUR_NEXT_BUTTON_XPATH_HERE'

    df = scrape_paginated_table(url, table_xpath, next_button_xpath)
    print(df)
    # df.to_csv('table_data.csv', index=False) # Save to CSV if needed