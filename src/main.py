#!/usr/bin/python

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os
import lxml  # lol pd.read_tml
from pandas import ExcelWriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def integerizer(soup):
    soup = soup.strip('$')
    return int(soup.replace(',', ''))


def main():
    savings_thing = pd.read_html("files/Savings/Savings.html")
    total_value_thing = pd.read_html("files/Total_Value/Total_Value.html")

    # Contracts: 4083 contract terminations totaling ~$15B in savings.
    contracts_total_value = total_value_thing[0]
    contracts_savings = savings_thing[0]
    # Grants: 6289 grant terminations totaling ~$15B in savings. Descriptions are forthcoming.
    grants_total_value = total_value_thing[1]
    grants_savings = savings_thing[1]
    # Real Estate: 747 lease terminations totaling 9,517,975 square feet and ~$468M in lease savings.
    real_estate_total_value = total_value_thing[2]
    real_estate_savings = savings_thing[2]

    # go a little harder on the html files to extract the link here
    with open('files/Savings/Savings_3-13-25.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    savings_soup = BeautifulSoup(html_content, 'html.parser')

    with open('files/Total_Value/Total_Value_3-13-25.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    value_soup = BeautifulSoup(html_content, 'html.parser')

    savings_contract_table = savings_soup.find('table')
    value_contract_table = value_soup.find('table')

    value_links = []
    for link in value_contract_table.find_all('a'):
        value_links.append(link.get('href'))

    value_links_series = pd.Series(value_links)
    contracts_total_value["Link"] = value_links_series
    # [print?]
    # with ExcelWriter(os.path.join("files/Savings/Savings.xlsx")) as writer:

    # with ExcelWriter(os.path.join("files/Total_Value/Total_Value.xlsx")) as writer:

    old_savings_thing = pd.read_html("files/Savings/archive/Savings_3-13-25.html")
    old_total_value_thing = pd.read_html("files/Total_Value/archive/Total_Value_3-13-25.html")
    savings_html_thing = pd.read_html("files/Savings/Savings.html")
    total_value_thing = pd.read_html("files/Total_Value/Total_Value.html")

    old_savings = old_savings_thing[0]
    savings = savings_html_thing[0]
    with pd.ExcelWriter("banana_pie.xlsx") as filewriter:
        old_savings.to_excel(filewriter, sheet_name="old savings", )
        savings.to_excel(filewriter, sheet_name="new savings")


if __name__ == "__main__":
    main()
