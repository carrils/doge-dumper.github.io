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

agencies = pd.read_json('agencies.json')
hierarchy = pd.read_json('hierarchy.json')
contracts = pd.read_json('contracts_08-27-25.json')
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
for contract in contracts.itertuples():
    for nerd_group in hierarchy.itertuples():
        if contract.agency == nerd_group.name:
            print(contract.agency)
            break
        for child in nerd_group.children:
            if contract.agency == child:
                print(contract.agency)
                break

# this piece of code is SO FUCKING CLEAN because literally each part of it is a symbol/code.
# this MAY be the best piece of code i've written so far.
savings = {}
value = {}
for contract in contracts.itertuples():
    if contract.agency not in savings:
        savings[contract.agency] = contract.savings
    else:
        savings[contract.agency] += contract.savings