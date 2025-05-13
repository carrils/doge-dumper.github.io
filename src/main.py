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
    # for now just exploring the response
    req = requests.get("https://api.doge.gov/savings/contracts?page=1&per_page=500")  # 500 contracts, page 1
    req_json = req.json()  # can also do .text and .content
    req_json['meta']  # {'total_results': 10248, 'pages': 21}
    


if __name__ == "__main__":
    main()
