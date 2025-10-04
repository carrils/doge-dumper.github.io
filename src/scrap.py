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

agencies = pd.read_json('tmp/data/agencies.json')
hierarchy = pd.read_json('tmp/data/hierarchy.json')
contracts = pd.read_json('tmp/data/contracts_08-27-25.json')
# hierarchy = hierarchy.set_index('name')



# group_count = {}
# for idx, children in hierarchy.itertuples():
#     # idx == str, children == []
#     group = []
#     group.append(idx)
#     for child_agency in children:
#         group.append(child_agency['name'])
#     for contract in contracts.itertuples():
#         if contract.agency not in group:
#             print("what")
#         else:
#             group_count[idx] += contract.savings

# we make-a da jay-son by hand yeh?
# for agency in hierarchy.itertuples():
#     print(f'name: \"{agency.name}\", children: [')
#     for child in agency.children:
#         print(f'\"{child['name']}\",')
#     print(']')

# this will iterate through contracts and match against groups of gov idiots
# for contract in contracts.itertuples():
#     for nerd_group in hierarchy.itertuples():
#         if contract.agency == nerd_group.name:
#             print(contract.agency)
#             break
#         for child in nerd_group.children:
#             if contract.agency == child:
#                 print(contract.agency)
#                 break

# this piece of code is SO FUCKING CLEAN because literally each part of it is a symbol/code.
# this MAY be the best piece of code i've written so far.
# savings = {}
# value = {}
# for contract in contracts.itertuples():
#     if contract.agency not in savings:
#         savings[contract.agency] = contract.savings
#     else:
#         savings[contract.agency] += contract.savings


savings = {}
value = {}
contractor_fatcats = {}
for contract in contracts.itertuples():
    if contract.agency not in savings:
        savings[contract.agency] = contract.savings
    else:
        savings[contract.agency] += contract.savings

    if contract.agency not in value:
        value[contract.agency] = contract.value
    else:
        value[contract.agency] += contract.value

    if contract.vendor not in contractor_fatcats:
        contractor_fatcats[contract.vendor] = contract.value
    else:
        contractor_fatcats[contract.vendor] += contract.value



# lmao its a collectionnnnn > TypeError: Index(...) must be called with a collection of some kind, 64 was passed
fat_cats_df = pd.DataFrame(contractor_fatcats,index={0:len(contractor_fatcats)})
fat_cats_df = fat_cats_df.T

agency_savings = pd.DataFrame(savings,index={0:len(savings)})
agency_savings = agency_savings.T

agency_value = pd.DataFrame(value, index={0:len(value)})
agency_value = agency_value.T

agency_savings.sort_values(by=[0], inplace=True, ascending=False)
agency_value.sort_values(by=[0], inplace=True, ascending=False)

#  most of these are weird. most are for news subscriptions?
for contract in contracts.itertuples():
    if 'Micro' in contract.fpds_status and contract.value > 25000:
        print(f'Agency: {contract.agency}, Vendor: {contract.vendor} \nValue: {contract.value} \nSavings: {contract.savings}')
