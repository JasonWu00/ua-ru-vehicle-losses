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
    # reference: https://plotly.com/python/horizontal-vertical-shapes/
    # Adding mostly transparent colored bars to denote major conflict moments
    figure.add_vrect(x0="2022-02-24", x1="2022-04-01", 
                    annotation_text="Kyiv", annotation_position="top left",
                    fillcolor="red", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2022-05-05", x1="2022-05-13", 
                    annotation_text="Siverskiy Donets", annotation_position="top left",
                    fillcolor="red", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2022-09-06", x1="2022-10-12", 
                    annotation_text="Kharkiv", annotation_position="top left",
                    fillcolor="blue", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2022-08-29", x1="2022-11-11", 
                    annotation_text="Kherson", annotation_position="outside top right",
                    fillcolor="blue", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2023-01-07", x1="2023-04-01", 
                    annotation_text="Bakhmut", annotation_position="outside top right",
                    fillcolor="red", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2023-01-24", x1="2023-02-15", 
                    annotation_text="Vuhledar", annotation_position="top left",
                    fillcolor="red", opacity=0.25, line_width=0)
    figure.add_vrect(x0="2023-06-04", x1="2023-10-17", 
                    annotation_text="Zaporizhzhia", annotation_position="top left",
                    fillcolor="blue", opacity=0.25, line_width=0)
    
    # the last cleaned data doesn't go up to the failed Russian offensive against
    # the Avdiivka slag heap mountain, so I will exclude this for the time being.
    # figure.add_vrect(x0="2023-10-18", x1="2023-11-01", 
    #                 annotation_text="Avdiivka", annotation_position="top left",
    #                 fillcolor="red", opacity=0.25, line_width=0)
    return figure

# Initialize the app
app = Dash(__name__)

# To do:
# Make names readable (written horizontally)
# Sort the graph bars
# Provide better x-axis, y-axis, and title descriptions
# Display RU/UA values side by side for a better comparison

app.layout = html.Div([
    html.Div(children=[
        'Data Science Project: Analysis on the War in Ukraine',
        html.Br(),
        'On the distribution of losses over time',
        html.Br(),
        'Author: Ze Hong Wu',
    ]),
    html.Hr(),
    html.H4(children="Introduction"),
    html.Div(children=[
        "For the purposes of this project, we will be analyzing data sets on known vehicle losses \
        in Russia's invasion of Ukraine.",
        html.Br(),
        "Our analysis is based on data scraped from the [Oryx blog]\
        (https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html).",
    ]),
    html.Hr(),
    html.H4(children="Visualizations"),
    html.Span(children='Vehicle losses over time for Russia and Ukraine, per day,\
              from 24 February 2022 to 18 October 2023:'),
    #dcc.RadioItems(options=['Russia', 'Ukraine'], value='Russia', id='country-radioitem'),
    dcc.Graph(figure=update_loss_time_graph(), id='time-loss-graph'),
    html.Hr(),
    html.H6(children="Disclaimer:"),
    html.Span(children=[
        "Due to limitations in our data acquisition and cleaning process, \
        namely poorly formatted source data, the losses shown in this visualization represent \
        only a subset of the whole Oryx blog data set. Many of the entries only contain \
        loss dates as text in images, and wrangling a neural network to carry out OCR \
        analysis on the data set is beyond the current scope of this project. Because of this, \
        the graph above represents only part of all confirmed losses.",
        html.Br(),
        "The data set we used was last updated on 18 October 2023. Any events that occurred \
        after this date, such as the ongoing Russian offensive in the Avdiivka direction, \
        are not reflected in this analysis."
    ]),
    html.H6(children="Analysis:"),
    html.Div(children=[
        "This graph displays the number of dated losses, per day, from the start of the war \
        to the current time.",
        html.Br(),
        "Parts of the graph, corresponding to periods of intense battle, are marked \
        with semi-transparent bars with the names of the battles at the top. These periods are \
        color-coded to denote the country starting them, red for Russia and blue for Ukraine.",
        html.Br(),
        "Notice that, during offensives launched by both sides, Ukraine consistently destroys more \
        enemy vehicles compared to Russia. For a country who is supposedly on the verge of collapsing \
        against a much more powerful enemy, they sure are doing a lot better than expected.",
        html.Br(),
        "Pay special attention to the Kharkiv counter-offensive portions of the graph \
        and notice the large spike of Russian vehicle losses. Some people claim that this offensive \
        was an abject failure and was the equivalent of the Battle of tbe Bulge. How did a \
        so-called 'inconsequential' skirmish lead to such significant Russian losses? \
        We will leave that as an exercise to the reader.",
        html.Br(),
        "",
    ]),
])

#https://www.nomidl.com/projects/russia-ukraine-war-data-analysis-project-using-python/#google_vignette
#https://github.com/dimitryzub/russo-ukraine-war-prediction-losses

# Run the app
if __name__ == '__main__':
    app.run(debug=True)