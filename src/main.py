#!/usr/bin/python

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os
import lxml  # lol pd.read_tml


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
    savings_html_thing = pd.read_html("files/Savings/Savings.html")
    total_value_html_thing = pd.read_html("files/Total_Value/Total_Value.html")

    # Contracts: 4083 contract terminations totaling ~$15B in savings.
    # contracts_total_value
    # contracts_savings
    # Grants: 6289 grant terminations totaling ~$15B in savings. Descriptions are forthcoming.
    # grants_total_value
    # grants_savings
    # Real Estate: 747 lease terminations totaling 9,517,975 square feet and ~$468M in lease savings.
    # real_estate_total_value
    # real_estate_savings

    # go a little harder on the html files to extract the link here


if __name__ == "__main__":
    main()
