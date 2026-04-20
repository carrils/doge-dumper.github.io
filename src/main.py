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
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_ag_grid as dag


# ToDo:
# graphs for contracts, grants, leases, and payments (temporal?)
# callback controls for import export
# reduce compilation time. maybe switch to docker?
# preserve api dump functionality somewhere.


def main():
    contract_bin_df = pd.read_json('tmp/data/contracts-3-30-26.json')
    grant_bin_df = pd.read_json('tmp/data/grants-3-30-26.json')
    lease_bin_df = pd.read_json('tmp/data/leases-3-30-26.json')
    squab = pd.read_json('tmp/data/payments-3-30-26.json')
    print('[ ---- AUTOBOT FUCKMODE ENGAGED (json loaded) ---- ]')

    def generate_table(dataframe, max_rows=10):
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ])


    app = Dash()

    app.layout = [
        # generate_table(contract_bin_df),
        html.H1(children='Contracts'),
        # html.Hr(),
        # dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-final-radio-item-example'),
        # https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html
        dcc.Graph(figure=px.histogram(contract_bin_df, x='agency', y='value', histfunc='sum')),
        dag.AgGrid(
            id="contracts-grid",
            rowData=contract_bin_df.to_dict('records'),
            columnDefs=[{"field": i, 'filter': True} for i in contract_bin_df.columns], # the {} parts in the next line make a dict, the rest of a list composition.
            dashGridOptions={'pagination': True, 'theme': 'themeBalham'},
            csvExportParams={
                "fileName": f"doge_contracts_export_{datetime.today().strftime('%m-%d-%Y')}.csv",
            }
        ),
        html.Button("Download CSV", id="csv-button", n_clicks=0),
        html.H1(children='Grants'),
        dag.AgGrid(
            rowData=grant_bin_df.to_dict('records'),
            columnDefs=[{"field": i, 'filter': True} for i in grant_bin_df.columns],
            dashGridOptions={'pagination': True, 'theme': 'themeBalham'}
        ),
        html.H1(children='Leases'),
        dag.AgGrid(
            rowData=lease_bin_df.to_dict('records'),
            columnDefs=[{"field": i, 'filter': True} for i in lease_bin_df.columns],
            dashGridOptions={'pagination': True, 'theme': 'themeBalham'}
        ),
        html.H1(children='payments'),
        dag.AgGrid(
            rowData=squab.to_dict('records'),
            columnDefs=[{"field": i, 'filter': True} for i in squab.columns],
            dashGridOptions={'pagination': True, 'theme': 'themeBalham'}
        )
    ]

    @callback(
        Output("contracts-grid", "exportDataAsCsv"),
        Input("csv-button", "n_clicks"),
    )
    def export_data_as_csv(n_clicks):
        if n_clicks:
            return True
        return False

    # Run the app
    app.run(debug=True)


if __name__ == "__main__":
    main()
