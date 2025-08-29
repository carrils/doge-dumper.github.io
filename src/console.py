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

contracts_meta = requests.get('https://api.doge.gov/savings/contracts?page=1&per_page=500').json()  # can also do .text and .content
cpage = 1
cbin = []  # bin of jsons. jsons, once existing, go into the bin.
while cpage <= contracts_meta['meta']['pages']:
    bin_json = requests.get(f"https://api.doge.gov/savings/contracts?&page={cpage}&per_page=500").json()
    cbin.append(pd.DataFrame.from_records(bin_json['result']['contracts']))
    cpage += 1

contract_bin_df = pd.concat(cbin)  # index starts at 0 goes to 500 then loops back to 0
contract_bin_df.reset_index(drop=True, inplace=True)
duplicate_rows = contract_bin_df[contract_bin_df.duplicated()]
contract = contract_bin_df.iloc[0]

agencies = pd.read_json('agencies.json')



# Open and read the JSON file
with open('agencies.json', 'r') as file:
    agencies_json = json.load(file)


for agency in agencies_json['agencies']:
    if len(agency['children']) > 0:
        print(f'{agency['name']} has {len(agency['children'])} children')
        for child in agency['children']:
            # check to see if children have children
            if 'children' in child.keys():
                print(child)

            # print child agency
            print(f'\t{child['name']}')

for agency in agencies_json['agencies']:
    if len(agency['children']) > 0:
        print(f'{agency['name']} has {len(agency['children'])} children')
        for child in agency['children']:
            # check to see if children have children
            if 'children' in child.keys():
                print(child)
            # print child agency
            # WE MAKE THE JSON BY HAND
            print(f'\t\t{{\n\t\t\t"name": "{child['name']}"\n\t\t}},')