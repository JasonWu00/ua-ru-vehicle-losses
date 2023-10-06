"""
This file contains Python code for a Dash dashboard.

Author: Ze Hong Wu

Anyone who edits this file and pushes their changes to master or Pull Requests their changes
should also add their name to this docstring.

This file was made with the reference of the Plotly Dash tutorial:
https://dash.plotly.com/tutorial
"""

from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
ru_df = pd.read_csv('data/losses_russia.csv')
ua_df = pd.read_csv('data/losses_ukraine.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Placeholder text'),
    dash_table.DataTable(data=ru_df.to_dict('records'), page_size=10)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)