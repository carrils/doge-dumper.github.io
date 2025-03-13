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
    savings_df = pd.read_table("files/contracts_savings.txt")
    total_df = pd.read_table("files/contracts_total_value.txt")

    # integerize THIS!
    total_df["Value"] = total_df["Value"].apply(integerizer)
    savings_df["Saved"] = savings_df["Saved"].apply(integerizer)
    total_values = total_df["Value"]
    savings_saved = savings_df["Saved"]


if __name__ == "__main__":
    main()
