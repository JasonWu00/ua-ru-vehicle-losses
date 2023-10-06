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

# In-place data modifying

losses_types = [
    "abandoned",
    "captured",
    "damaged",
    "destroyed",
    "sunk"
]
ru_df[losses_types] = ru_df[losses_types].fillna(0)
ua_df[losses_types] = ua_df[losses_types].fillna(0)

ru_losses_sum = pd.DataFrame(columns=losses_types)
ua_losses_sum = pd.DataFrame(columns=losses_types)
ru_losses_sum.loc[0] = [0,0,0,0,0]
ua_losses_sum.loc[0] = [0,0,0,0,0]
for type in losses_types:
    ru_losses_sum[type].loc[0] = ru_df[type].sum()
    ua_losses_sum[type].loc[0] = ua_df[type].sum()

ru_losses_sum = ru_losses_sum.transpose()
ua_losses_sum = ua_losses_sum.transpose()
ru_losses_sum = ru_losses_sum.reset_index()
ua_losses_sum = ua_losses_sum.reset_index()
ru_losses_sum.rename(columns={0: "count"}, inplace=True)
ua_losses_sum.rename(columns={0: "count"}, inplace=True)
print(ru_losses_sum)
print(ua_losses_sum)

# Initialize the app
app = Dash(__name__)

# Long paragraphs that will appear in the app

# App layout
app.layout = html.Div([
    html.Div(children='Data Science: Week 5 exercise:'),
    html.Div(children='Exploratory charts using vehicle loss data from the War in Ukraine'),
    html.Hr(),
    html.Div(children='View vehicle manufacturer distribution for:'),
    dcc.RadioItems(options=['Russia', 'Ukraine'], value='Ukraine', id='country-radioitem'),
    dcc.Graph(figure={}, id='manufacturer-graph'),
    html.Span(children=[
        "Russia is almost entirely dependent on its own material and old Soviet stock.",
        html.Br(),
        "While Ukraine also relies heavily on old Soviet equipment,\
        it is also receiving support from a number of countries aligned with its goals and values.",
        html.Br(),
        "The disparity of foreign supplied vehicles to the two countries reveal\
        a similar disparity in political support to the two countries.",
    ]),
    html.Hr(),
    html.Div(children='View vehicle loss distribution for:'),
    dcc.RadioItems(options=['Russia', 'Ukraine'], value='Ukraine', id='country-losses-radioitem'),
    dcc.Graph(figure={}, id='loss-graph'),
    html.Span(children=[
        "Both sides have similar abandoned/captured/destroyed proportions.",
        html.Br(),
        "This indicates that both sides are experiencing similar conditions on the front lines.",
    ])
])

# Add controls to build the interaction
@callback(
    Output(component_id='manufacturer-graph', component_property='figure'),
    Input(component_id='country-radioitem', component_property='value')
)
def update_manufacturers_graph(col_chosen):
    if col_chosen == "Russia":
        figure=px.histogram(ru_df, x='manufacturer', y='losses_total', histfunc='sum')
    elif col_chosen == "Ukraine":
        figure=px.histogram(ua_df, x='manufacturer', y='losses_total', histfunc='sum')
    return figure

@callback(
    Output(component_id='loss-graph', component_property='figure'),
    Input(component_id='country-losses-radioitem', component_property='value')
)
def update_loss_graph(col_chosen):
    if col_chosen == "Russia":
        figure=px.histogram(ru_losses_sum, x="index", y="count", histfunc='sum')
    elif col_chosen == "Ukraine":
        figure=px.histogram(ua_losses_sum, x="index", y="count", histfunc='sum')
    return figure

# Run the app
if __name__ == '__main__':
    app.run(debug=True)