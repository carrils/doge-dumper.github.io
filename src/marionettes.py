#!/usr/bin/python

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    driver = webdriver.Chrome()
    driver.get("https://doge.gov/savings")

    # [ --- BEGIN gather table data --- ]
    table = driver.find_element(By.TAG_NAME, "table")
    headers = [th.text for th in table.find_elements("xpath", ".//th")]  # vectorized

    rows = []
    for tr in table.find_elements("xpath", ".//tr")[1:]:  # Skip header row
        cells = [td.text for td in tr.find_elements("xpath", ".//td")]  # vectorized
        rows.append(cells)

    df = pd.DataFrame(rows, columns=headers)

    # df.to_csv("table_data.csv", index=False) #to save as CSV
    # [ --- END gather table data --- ]

    # [ --- BEGIN load next page --- ]
    # all buttons. includes switching values between total value and savings,
    # and then a confusing third button to sort the selected values (i.e. total value values) by date ascending and descending.
    # it could be they are just trying to confuse people, because that was not there before.
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.accessible_name == '2':
            button.click()

if __name__ == "__main__":
    main()
