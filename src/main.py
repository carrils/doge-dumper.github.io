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
    contracts_500 = requests.get(
        "https://api.doge.gov/savings/contracts?page=1&per_page=500").json()  # can also do .text and .content
    contracts_500['meta']  # {'total_results': 10248, 'pages': 22}
    contracts_500['meta']['pages']  # 22

    # grants: https://api.doge.gov/savings/grants?page=1&per_page=500
    # leases: https://api.doge.gov/savings/leases?page=1&per_page=500

    grants_500 = requests.get('https://api.doge.gov/savings/grants?page=1&per_page=500').json()

    cpage = 1
    cbin = []  # bin of jsons. jsons, once existing, go into the bin.
    while cpage <= contracts_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/contracts?&page={cpage}&per_page=500").json()
        cbin.append(pd.DataFrame.from_records(bin_json['result']['contracts']))
        cpage += 1

    contract_bin_df = pd.concat(cbin)

    gpage = 1
    gbin = []  # bin of jsons. jsons, once existing, go into the bin.
    while gpage <= grants_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/grants?page={gpage}&per_page=500").json()
        gbin.append(pd.DataFrame.from_records(bin_json['result']['grants']))
        gpage += 1

    grant_bin_df = pd.concat(gbin)

    leases_500 = requests.get('https://api.doge.gov/savings/leases?page=1&per_page=500').json()
    leases_500_df = pd.DataFrame.from_records(leases_500['result']['leases'])
    lpage = 1
    lbin = []  # bin of jsons. jsons, once existing, go into the bin.
    while lpage <= leases_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/leases?&page={lpage}&per_page=500").json()
        lbin.append(pd.DataFrame.from_records(bin_json['result']['leases']))
        lpage += 1

    lease_bin_df = pd.concat(lbin)

    print(len(contract_bin_df))
    print(len(grant_bin_df))
    print(len(lease_bin_df))


if __name__ == "__main__":
    main()
