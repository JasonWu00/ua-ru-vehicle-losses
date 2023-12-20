"""
This page discusses the distributions of lost vehicles by date lost.

Copyright (C) 2023 Ze Hong Wu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>

Anyone who edits this file and pushes their changes to master or Pull Requests their changes
should also add their name to this docstring.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
#import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

ru_losses = pd.read_csv('data/oryx/ru_losses.csv')
ua_losses = pd.read_csv('data/oryx/ua_losses.csv')
ru_losses_trunc = ru_losses[["type", "date_lost", "user"]]
ua_losses_trunc = ua_losses[["type", "date_lost", "user"]]
ru_ua_concat = pd.concat([ru_losses_trunc, ua_losses_trunc])
ru_ua_dates = ru_ua_concat.groupby(["date_lost", "user"]).count()
ru_ua_dates.rename(columns={"type": "count"})

def stacked_loss_graph():
    """
    An attempt to create a Plotly subplot using figure objects.
    Traces were too confusing for me and there seems to be no good way
    to fit figure objects into subplots.

    https://stackoverflow.com/questions/71623896/create-a-histogram-with-plotly-graph-objs-like-in-plotly-express
    """
    #go.Figure(data=[go.Histogram(ru_ua_concat, x="date_lost", y="user", histfunc="count")])
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.00)
    fig1 = go.Histogram(
                    x=ru_ua_concat[ru_ua_concat["user"] == "Russia"]["date_lost"],
                    y=ru_ua_concat[ru_ua_concat["user"] == "Russia"]["user"],
                    histfunc="count", nbinsx=655,
                    name="Russia",
                    marker={"color": "red"})
    fig.append_trace(fig1, row=2, col=1)
    fig2 = go.Histogram(
                    x=ru_ua_concat[ru_ua_concat["user"] == "Ukraine"]["date_lost"],
                    y=ru_ua_concat[ru_ua_concat["user"] == "Ukraine"]["user"],
                    histfunc="count", nbinsx=655,
                    name="Ukraine",
                    marker={"color": "#4444FF"},
                    )
    #fig2.update(yaxis_range=[0,50]) #also broken and useless
    fig.append_trace(fig2, row=1, col=1)
    fig.update_layout(height=700, width=1000, title_text="RU/UA Losses, above and below")
    fig.update_yaxes(autorange="reversed", row=2, col=1)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(range=[0,80], row=1, col=1) # completely broken and useless
    return fig

def update_loss_time_graph(show_rects = True) -> px.histogram:
    """
    Generates an overlaid vehicle losses histogram.
    """
    # reference: 
    # https://stackoverflow.com/questions/65856933/plotly-how-to-plot-histogram-with-x-hour
    #print(ru_ua_dates.reset_index())
    figure = px.histogram(ru_ua_concat, x="date_lost", y="user", histfunc="count",
                          color="user",
                          color_discrete_map={"Russia": "red", "Ukraine": "#4444FF"},
                          nbins=655,
                          labels={
                              "date_lost": "Date",
                              "user": "Vehicles lost",
                              "count": "Vehicles lost"
                          },
                          barmode="overlay",
                          width=1000, height=500, opacity=0.75,
                          title="RU/UA losses, overlaid"
                          )
    # reference: https://plotly.com/python/horizontal-vertical-shapes/
    # Adding mostly transparent colored bars to denote major conflict moments
    if show_rects:
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
    figure.update_yaxes(
        range=(0, 80),
        constrain='domain'
    )
    # the last cleaned data doesn't go up to the failed Russian offensive against
    # the Avdiivka slag heap mountain, so I will exclude this for the time being.
    # figure.add_vrect(x0="2023-10-18", x1="2023-11-01", 
    #                 annotation_text="Avdiivka", annotation_position="top left",
    #                 fillcolor="red", opacity=0.25, line_width=0)
    return figure

# ======================
# streamlit stuff

st.set_page_config(layout="wide")

# This markdown line was based on this:
# https://discuss.streamlit.io/t/cover-entire-page/26345
st.markdown(
    """
    <style>
        .main > div {
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#st.text("Hello, world")
st.title('Iron Harvest: Vehicles lost in Ukraine')
st.text('Author: Ze Hong Wu')
st.markdown(
"""
#### Introduction
For the purposes of this project, we will be analyzing data sets on known vehicle losses \
in Russia's invasion of Ukraine.

The analysis in this page is based on data scraped from the \
[Oryx blog](https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html), \
which contains individual confirmed vehicles lost in Ukraine as well as \
image proof of their loss and (sometimes) dates when they were lost.

#### Visualizations
""")

st.plotly_chart(update_loss_time_graph())
st.markdown(
"""
#### Explanation

The histogram shown above displays some of the losses sustained by Russia and Ukraine, \
sorted by date, stacked on top of each other. Semi-transparent blue and red bars denote periods of \
intense conflict or major battle, with red bars identifying Russian battles and blue bars \
identifying Ukrainian battles.

The histogram below shows the same data, but with the data split into two mirroring sections \
to allow for a better display of the loss differences.
""")
st.plotly_chart(stacked_loss_graph())

st.markdown(
"""
#### Disclaimers
Due to limitations in our data acquisition and cleaning process, \
namely poorly formatted source data, the losses shown in this visualization represent \
only the subset of the whole Oryx blog data set that has well formatted datetime data. \
Because of this, the graph above represents only part of all confirmed losses.

The data set we used was last updated on 18 October 2023. Any events that occurred \
after this date, such as the ongoing Russian offensive in the Avdiivka direction, \
are not reflected in this analysis.

#### Analysis
The two graphs above displays the number of dated losses, per day, from the start of the war \
to the current time. The first one shows them overlaid on each other, with important periods \
of battle highlighted with bars colored by starting country \
(red for Russia and blue for Ukraine).

Parts of the graph, corresponding to periods of intense battle, are marked \
with semi-transparent bars with the names of the battles at the top. These periods are \
color-coded to denote the country starting them, red for Russia and blue for Ukraine.

Notice that, during offensives launched by both sides, Ukraine consistently destroys more \
enemy vehicles compared to Russia. For a country who is supposedly on the verge of collapsing \
against a much more powerful enemy, they sure are doing a lot better than expected.

Pay special attention to the \
[Kharkiv counter-offensive](https://en.wikipedia.org/wiki/2022_Kharkiv_counteroffensive) \
portions of the graph:
""")

losses_kharkiv = update_loss_time_graph(show_rects=False)
losses_kharkiv.update_xaxes(
    range=("2022-09-06", "2022-10-12"),
    constrain='domain'
)
losses_kharkiv.update_yaxes(
    range=(0, 65),
    constrain='domain'
)
losses_kharkiv.update_layout(
    width=500,
    title="RU/UA losses, Kharkiv Campaign"
)

st.plotly_chart(losses_kharkiv)

st.markdown(
"""
#### Focusing on Kharkiv
Notice the large spike of Russian vehicle losses.

This large spike seems to go against institutional knowledge that an attacking force \
oftentimes need a three to one force ratio and often suffers more losses than the defender \
at some points of the battle.

Some people claim that this offensive was an abject failure and was \
the equivalent of the Battle of tbe Bulge. How did a so-called 'inconsequential' skirmish \
lead to such significant Russian losses and the reclamation of formerly occupied territory? \
We will leave that as an exercise to the reader.
""")
