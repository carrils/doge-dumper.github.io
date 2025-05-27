#!/usr/bin/python

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os
import requests

# Plan:
# read first page then determine how many times to do the curl
# then consume that json into a df and then you have the contracts.
# now do the same for grants
# and now do the same for leases.
# then you have a days complete data set.
# doge set.
def integerizer(soup):
    soup = soup.strip('$')
    return int(soup.replace(',', ''))


def main():
    contracts_500 = requests.get("https://api.doge.gov/savings/contracts?page=1&per_page=500").json()  # can also do .text and .content
    contracts_500_json_meta = contracts_500['meta']  # {'total_results': 10248, 'pages': 22}
    contracts_500['meta']['pages']  # 22

    page = 0
    bin = []  # bin of jsons
    while page <= contracts_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/contracts?&page={page}&per_page=500").json()
        if bin_json['success']:  # for some reason only the first try returns a schema validation error who cares fuck elon musk
            bin.append(bin_json['result']['contracts'])
        page += 1

    bin_df = pd.DataFrame.from_records(bin)

if __name__ == "__main__":
    main()
