#!/usr/local/bin/python

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os
import requests


def main():
    contracts_500 = requests.get("https://api.doge.gov/savings/contracts?page=1&per_page=500").json()  # can also do .text and .content
    # contracts_500['meta']  # {'total_results': 10248, 'pages': 22}
    # contracts_500['meta']['pages']  # 22

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
    gbin = []
    while gpage <= grants_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/grants?page={gpage}&per_page=500").json()
        gbin.append(pd.DataFrame.from_records(bin_json['result']['grants']))
        gpage += 1

    grant_bin_df = pd.concat(gbin)

    leases_500 = requests.get('https://api.doge.gov/savings/leases?page=1&per_page=500').json()
    lpage = 1
    lbin = []
    while lpage <= leases_500['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/leases?&page={lpage}&per_page=500").json()
        lbin.append(pd.DataFrame.from_records(bin_json['result']['leases']))
        lpage += 1

    lease_bin_df = pd.concat(lbin)
    # '05-27-2025'
    with pd.ExcelWriter(f'../files/doge_data_dump_{datetime.today().strftime('%m-%d-%Y')}.xlsx',
                        engine='xlsxwriter') as writer:
        contract_bin_df.to_excel(writer, sheet_name='Contracts', index=False)
        grant_bin_df.to_excel(writer, sheet_name=f'Grants', index=False)
        lease_bin_df.to_excel(writer, sheet_name=f'Leases', index=False)
        # column widths courtesy of xlsxwriter.autofit()
        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.autofit()


if __name__ == "__main__":
    main()
