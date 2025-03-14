#!/usr/bin/python

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os


def integerizer(soup):
    soup = soup.strip('$')
    return int(soup.replace(',', ''))


def main():
    # savings_df.loc[4] == total_df.loc[4]
    savings_df = pd.read_table("../files/contracts_savings.txt")
    total_df = pd.read_table("../files/contracts_total_value.txt")

    # integerize THIS!
    total_df["Value"] = total_df["Value"].apply(integerizer)
    savings_df["Saved"] = savings_df["Saved"].apply(integerizer)

    # Total Value: The potential expenditure (with options).
    # Savings: Total value - current obligation
    obbies = total_df["Value"] - savings_df["Saved"]
    
    # so hows about we actually read this data
    super_df = pd.concat([total_df, savings_df["Saved"]], axis=1)
    super_df = pd.concat([super_df, obbies], axis=1)
    super_df.to_csv("../files/super_doge.csv", index=False)
    print("Savings: Total value - current obligation")
    print("Total Value: The potential expenditure (with options).")


if __name__ == "__main__":
    main()
