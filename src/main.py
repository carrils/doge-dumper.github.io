#!/usr/local/bin/python3

import csv
import json
from datetime import datetime
import pandas as pd
import math
import glob
import os
import requests
import xlsxwriter
import numpy as np

from src.scrap import hierarchy


# TODO
# Make script runnable from any directory
# need to add up:
# 	contract
# 	lease
# 	grant
# 	payment

def soupcans():
    df = pd.DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.randn(8),
            "D": np.random.randn(8),
        }
    )
    # Grouping by a column label, selecting column labels,
    # and then applying the 'DataFrameGroupBy.sum()' function to the resulting groups.
    # experimental code to sum totals for an agency or contract or whatever.
    df.groupby("agency/contract/identifying info/ID")[["C", "D"]].sum()


def main():
    start_time = datetime.now()
    print("Beginning doge data dump...")
    contracts_meta = requests.get('https://api.doge.gov/savings/contracts?page=1&per_page=500').json()  # can also do .text and .content
    # contracts_meta['meta']  # {'total_results': 10248, 'pages': 22}
    # contracts_meta['meta']['pages']  # 22

    # grants: https://api.doge.gov/savings/grants?page=1&per_page=500
    # leases: https://api.doge.gov/savings/leases?page=1&per_page=500
    # payments: https://api.doge.gov/payments?page=1&per_page=500
    # payment statistics: https://api.doge.gov/payments/statistics

    grants_meta = requests.get('https://api.doge.gov/savings/grants?page=1&per_page=500').json()
    leases_meta = requests.get('https://api.doge.gov/savings/leases?page=1&per_page=500').json()
    payments_meta = requests.get('https://api.doge.gov/payments?page=1&per_page=500').json()
    # no params, just returns number of payments made by agency
    pmt_stats = requests.get('https://api.doge.gov/payments/statistics').json()

    cpage = 1
    cbin = []  # bin of jsons. jsons, once existing, go into the bin.
    while cpage <= contracts_meta['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/contracts?&page={cpage}&per_page=500").json()
        cbin.append(pd.DataFrame.from_records(bin_json['result']['contracts']))
        cpage += 1

    contract_bin_df = pd.concat(cbin)  # index starts at 0, goes to 500 then loops back to 0 for all rows
    contract_bin_df.reset_index(drop=True, inplace=True)
    # [ ---- visualization ---- ]
    duplicate_rows_contracts = contract_bin_df[contract_bin_df.duplicated()]  # all USAID contracts.
    # group by agency name and perform agg functions on savings and value columns
    contracts_by_agency = contract_bin_df.groupby("agency").agg({'savings': 'sum', 'value': 'sum'})

    # [ --- 09.02.25 --- ]
    hierarchy = pd.read_json('hierarchy.json')
    for agency in hierarchy.itertuples():
        # check for parent agency contracts
        for t_agency in contracts_by_agency.itertuples():
            # Pandas(Index=63, agency='United States Trade and Development Agency', savings=415391.0, value=1813720.34)
            if t_agency.agency == agency.name:
                print(f'big dawg {agency.name}: \t{t_agency.savings}')
        # for child in agency.children:
        #     print(f'\t{child['name']}')
        # check for child agency contracts and add them to parent contracts. a "sort".










    # [ --- 09.02.25 --- ]
    gpage = 1
    gbin = []
    while gpage <= grants_meta['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/grants?page={gpage}&per_page=500").json()
        gbin.append(pd.DataFrame.from_records(bin_json['result']['grants']))
        gpage += 1

    grant_bin_df = pd.concat(gbin)
    grant_bin_df.reset_index(drop=True, inplace=True)

    lpage = 1
    lbin = []
    while lpage <= leases_meta['meta']['pages']:
        bin_json = requests.get(f"https://api.doge.gov/savings/leases?&page={lpage}&per_page=500").json()
        lbin.append(pd.DataFrame.from_records(bin_json['result']['leases']))
        lpage += 1

    lease_bin_df = pd.concat(lbin)
    lease_bin_df.reset_index(drop=True, inplace=True)

    ppage = 1
    pbin = []
    pmt_processing_start_time = datetime.now()
    print("Beginning to process payments. This may take a while...")
    while ppage <= payments_meta['meta']['pages']:  # 215 pages
        res = requests.get(f"https://api.doge.gov/payments?page={ppage}&per_page=500").json()
        # res_json = res['result']['payments'].json()
        for payment in res['result']['payments']:
            # because not passing an index it breaks so we wrap the dict in a list and call it like an idiot
            df = pd.DataFrame([payment])
            pbin.append(df)
        ppage += 1

    payments_bin_df = pd.concat(pbin)
    payments_bin_df.reset_index(drop=True, inplace=True)

    pmt_result = pmt_stats['result']
    lob = []  # list of dfs its a list with df's in it its name is LOB
    for res in pmt_result:
        res_df = pd.DataFrame.from_records(pmt_result[f'{res}'])
        lob.append(res_df)

    # just putting the random shit they compiled onto one df
    squab = pd.concat(lob, axis=1)
    squab.insert(2, '', '')
    squab.insert(5, 'blank', '')
    squab.columns = ['agency_name', 'count', '', 'date', 'count', '', 'orgn_name', 'count']
    print(f"Payment processing time: {datetime.now() - pmt_processing_start_time}")

    # '05-27-2025'
    with pd.ExcelWriter(f'files/doge_data_dump_{datetime.today().strftime('%m-%d-%Y')}.xlsx',
                        engine='xlsxwriter') as writer:
        contract_bin_df.to_excel(writer, sheet_name='Contracts', index=False)
        grant_bin_df.to_excel(writer, sheet_name=f'Grants', index=False)
        lease_bin_df.to_excel(writer, sheet_name=f'Leases', index=False)
        payments_bin_df.to_excel(writer, sheet_name=f'Payments', index=False)
        squab.to_excel(writer, sheet_name=f'Payment Statistics', index=False)

        # column widths courtesy of xlsxwriter.autofit()
        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.autofit()

    print(f'Total Execution Time: {datetime.now() - start_time}')

    def has_children(row):
        if row:
            # return any(row.values())


if __name__ == "__main__":
    main()
