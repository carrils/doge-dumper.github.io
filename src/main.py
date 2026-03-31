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
# graphs for contracts, grants, leases, and payments (temporal?)
# callback controls that make sense and are useful
# reduce compilation time. maybe switch to docker?
# now that api dump is gone here we need to preserve that functionality somewhere.

def main():
    contract_bin_df = pd.read_json('tmp/data/contracts-3-30-26.json')
    grant_bin_df = pd.read_json('tmp/data/grants-3-30-26.json')
    lease_bin_df = pd.read_json('tmp/data/leases-3-30-26.json')
    squab = pd.read_json('tmp/data/payments-3-30-26.json')
    print('[ ---- AUTOBOT FUCKMODE ENGAGED (json loaded) ---- ]')

    app = Dash()

    app.layout = [
        html.Div(children='Contracts'),
        # html.Hr(),
        # dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-final-radio-item-example'),
        # dcc.Graph(figure=px.histogram(contract_bin_df, x='agency', y='value', histfunc='avg')),
        dag.AgGrid(
            rowData=contract_bin_df.to_dict('records'),
            columnDefs=[{"field": i} for i in contract_bin_df.columns],  # single line fors because we wanna bully anyone bothering to read this
            dashGridOptions={'pagination': True}
        ),
        html.Div(children='Grants'),
        dag.AgGrid(
            rowData=grant_bin_df.to_dict('records'),
            columnDefs=[{"field": i} for i in grant_bin_df.columns],
            dashGridOptions={'pagination': True}
        ),
        html.Div(children='Leases'),
        dag.AgGrid(
            rowData=lease_bin_df.to_dict('records'),
            columnDefs=[{"field": i} for i in lease_bin_df.columns],
            dashGridOptions={'pagination': True}
        ),
        html.Div(children='payments'),
        dag.AgGrid(
            rowData=squab.to_dict('records'),
            columnDefs=[{"field": i} for i in squab.columns],
            dashGridOptions={'pagination': True}
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
