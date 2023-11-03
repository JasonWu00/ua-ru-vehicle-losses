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
ru_losses = pd.read_csv('data/oryx/ru_losses.csv')
ua_losses = pd.read_csv('data/oryx/ua_losses.csv')
ru_losses = ru_losses[pd.notna(ru_losses["date_lost"])]
ua_losses = ua_losses[pd.notna(ua_losses["date_lost"])]

ru_losses_trunc = ru_losses[["type", "date_lost", "user"]]
ua_losses_trunc = ua_losses[["type", "date_lost", "user"]]

#ru_losses_dated = ru_losses[pd.notna(ru_losses["day"])]
#print(ru_losses_dated[["id", "day", "month", "year", "status", "proof"]])
# dated RU losses come in at 3012 rows; around 25% of all losses (12450)
# this should be enough

#ua_losses_dated = ua_losses[pd.notna(ua_losses["day"])]
#print(ua_losses_dated[["id", "day", "month", "year", "status", "proof"]])
# dated UA losses come in at 1450 rows, around 33% of all losses (4608)
# should also be enough.

def update_loss_time_graph():
    # reference: https://stackoverflow.com/questions/65856933/plotly-how-to-plot-histogram-with-x-hour
    ru_ua_concat = pd.concat([ru_losses_trunc, ua_losses_trunc])
    ru_ua_dates = ru_ua_concat.groupby(["date_lost", "user"]).count()
    #print(ru_ua_dates.reset_index())
    figure = px.histogram(ru_ua_concat, x="date_lost", y="user", histfunc="count",
                          color="user",
                          color_discrete_map={"Russia": "red", "Ukraine": "blue"},
                          nbins=500,
                          title="Vehicle losses with confirmed dates, 24 Feb 2022 to Present Day",
                          labels={
                              "date_lost": "Date",
                              "user": "Number of vehicles lost",
                              "count": "Number of vehicles lost"
                          }
                          )
    # if col_chosen == "Russia":
    #     figure=px.histogram(ru_df, x='manufacturer', y='losses_total', histfunc='sum')
    # elif col_chosen == "Ukraine":
    #     figure=px.histogram(ua_df, x='manufacturer', y='losses_total', histfunc='sum')
    return figure

# Initialize the app
app = Dash(__name__)

# To do:
# Make names readable (written horizontally)
# Sort the graph bars
# Provide better x-axis, y-axis, and title descriptions
# Display RU/UA values side by side for a better comparison

app.layout = html.Div([
    html.Div(children='Data Science Project: Analysis on the War in Ukraine'),
    html.Div(children='On the distribution of losses over time'),
    html.Div(children='Author: Ze Hong Wu'),
    html.Div(children='View vehicle losses over time for Russia and Ukraine, per week:'),
    #dcc.RadioItems(options=['Russia', 'Ukraine'], value='Russia', id='country-radioitem'),
    dcc.Graph(figure=update_loss_time_graph(), id='time-loss-graph'),
])

#https://www.nomidl.com/projects/russia-ukraine-war-data-analysis-project-using-python/#google_vignette
#https://github.com/dimitryzub/russo-ukraine-war-prediction-losses

# Run the app
if __name__ == '__main__':
    app.run(debug=True)