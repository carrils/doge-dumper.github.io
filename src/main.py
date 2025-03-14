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

def integerizer(soup):
    soup = soup.strip('$')
    return int(soup.replace(',', ''))


def main():
    # # savings_df.loc[4] == total_df.loc[4]
    # savings_df = pd.read_table("../files/contracts_savings.txt")
    # total_df = pd.read_table("../files/contracts_total_value.txt")
    #
    # # integerize THIS!
    # total_df["Value"] = total_df["Value"].apply(integerizer)
    # savings_df["Saved"] = savings_df["Saved"].apply(integerizer)
    #
    # # Total Value: The potential expenditure (with options).
    # # Savings: Total value - current obligation
    # obbies = total_df["Value"] - savings_df["Saved"]
    #
    # # so hows about we actually read this data
    # super_df = pd.concat([total_df, savings_df["Saved"]], axis=1)
    # super_df = pd.concat([super_df, obbies], axis=1)
    # super_df.rename(columns={0: 'Obligations'}, inplace=True)
    # super_df.to_csv("../files/super_doge.csv", index=False)
    # print("Savings: Total value - current obligation")
    # print("Total Value: The potential expenditure (with options).")
    # To get these html files go to doge.gov and expand all 3 tables, then save as.
    # flip the little thing at the top to the other thing and then repeat
    # thing == list of dataframes.
    savings_html_thing = pd.read_html("files/Savings/Savings.html")  # 3.13.25
    total_value_html_thing = pd.read_html("files/Total_Value/Total_Value.html")  # 3.13.25

    # Contracts: 4083 contract terminations totaling ~$15B in savings.
    contracts_total_value = total_value_html_thing[0]
    contracts_savings = savings_html_thing[0]
    # Grants: 6289 grant terminations totaling ~$15B in savings. Descriptions are forthcoming.
    grants_total_value = total_value_html_thing[1]
    grants_savings = savings_html_thing[1]
    # Real Estate: 747 lease terminations totaling 9,517,975 square feet and ~$468M in lease savings.
    real_estate_total_value = total_value_html_thing[2]
    real_estate_savings = savings_html_thing[2]

    # go a little harder on the html files to extract the link here
    with open('files/Savings/Savings.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    savings_soup = BeautifulSoup(html_content, 'html.parser')

    with open('files/Total_Value/Total_Value.html', 'r', encoding='utf-8') as file:
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

if __name__ == "__main__":
    main()
