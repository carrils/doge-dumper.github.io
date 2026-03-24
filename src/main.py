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

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_ag_grid as dag  # idk if i need this beyond the example

# TODO
# Make script runnable from any directory
# need to add up:
# 	contract
# 	lease
# 	grant
# 	payment


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

    # [ ---- visualization ---- ]
    duplicate_rows_contracts = contract_bin_df[contract_bin_df.duplicated()]  # all USAID contracts.
    # group by agency name and perform agg functions on savings and value columns
    # aka sum the contract savings and value for each agency
    contracts_by_agency = contract_bin_df.groupby("agency").agg({'savings': 'sum', 'value': 'sum'})
    # find the fattest of cats and sum savings and value of their contracts
    contracting_fatcats = contract_bin_df.groupby("vendor").agg({'savings': 'sum', 'value': 'sum'})
    contract_bin_df['savings'].agg('sum')  # 58354585573.83
    grant_bin_df['savings'].agg('sum')  # 43775935185
    lease_bin_df['savings'].agg('sum')  # 139708550

    # [Printing] Format: '05-27-2025'
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

    # Initialize the app
    app = Dash()
    # App layout
    app.layout = [
        html.Div(children='My First App with Data, Graph, and Controls'),
        html.Hr(),
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-final-radio-item-example'),
        dag.AgGrid(
            rowData=df.to_dict('records'),
            columnDefs=[{"field": i} for i in df.columns]
        ),
        dcc.Graph(figure={}, id='my-final-graph-example')
    ]

    # Add controls to build the interaction
    @callback(
        Output(component_id='my-final-graph-example', component_property='figure'),
        Input(component_id='my-final-radio-item-example', component_property='value')
    )
    def update_graph(col_chosen):
        fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
        return fig

    # Run the app
    app.run(debug=True)


if __name__ == "__main__":
    main()
