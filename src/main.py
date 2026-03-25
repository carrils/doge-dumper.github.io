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
# plotly dash reqs
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_ag_grid as dag


# ToDo:
# add grants, leases, and payments tables to dash dashboard (hehe xd)
# graphs for contracts, grants, leases, and payments (temporal?)
# callback controls that make sense and are useful
# reduce compilation time. maybe switch to docker? 

def main():
    start_time = datetime.now()
    print("Beginning doge data dump...")
    contracts_meta = requests.get('https://api.doge.gov/savings/contracts?page=1&per_page=500').json()  # can also do .text and .content
    # contracts_meta['meta']  # {'total_results': 10248, 'pages': 22}
    # contracts_meta['meta']['pages']  # 22


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

    contract_bin_df = pd.concat(cbin)
    contract_bin_df.reset_index(drop=True, inplace=True) # index starts at 0, goes to 500 then loops back to 0 for all rows

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

    # Initialize the app
    app = Dash()
    # App layout
    app.layout = [
        html.Div(children='contracts_bin_df'),
        html.Hr(),
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-final-radio-item-example'),
        dcc.Graph(figure=px.histogram(contract_bin_df, x='agency', y='value', histfunc='avg')),
        dag.AgGrid(
            rowData=contract_bin_df.to_dict('records'),
            columnDefs=[{"field": i} for i in contract_bin_df.columns]
        )
    ]

    # Add controls to build the interaction
    @callback(
        Output(component_id='my-final-graph-example', component_property='figure'),
        Input(component_id='my-final-radio-item-example', component_property='value')
    )
    def update_graph(col_chosen):
        fig = px.histogram(contract_bin_df, x='agency_name', y=col_chosen, histfunc='avg')
        return fig

    # Run the app
    app.run(debug=True)


if __name__ == "__main__":
    main()
