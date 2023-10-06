"""
This file contains Python code for a Dash dashboard.

Author: Ze Hong Wu

Anyone who edits this file and pushes their changes to master or Pull Requests their changes
should also add their name to this docstring.

This file was made with the reference of the Plotly Dash tutorial:
https://dash.plotly.com/tutorial
"""

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
ru_df = pd.read_csv('data/losses_russia.csv')
ua_df = pd.read_csv('data/losses_ukraine.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Data Science: Week 5 exercise:'),
    html.Div(children='Exploratory charts using vehicle loss data from the War in Ukraine'),
    html.Hr(),
    html.Div(children='View vehicle manufacturer distribution for:'),
    dcc.RadioItems(options=['Russia', 'Ukraine'], value='Ukraine', id='country-radioitem'),
    dcc.Graph(figure={}, id='manufacturer-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='manufacturer-graph', component_property='figure'),
    Input(component_id='country-radioitem', component_property='value')
)
def update_graph(col_chosen):
    if col_chosen == "Russia":
        figure=px.histogram(ru_df, x='manufacturer', y='losses_total', histfunc='sum')
    elif col_chosen == "Ukraine":
        figure=px.histogram(ua_df, x='manufacturer', y='losses_total', histfunc='sum')
    return figure

# Run the app
if __name__ == '__main__':
    app.run(debug=True)