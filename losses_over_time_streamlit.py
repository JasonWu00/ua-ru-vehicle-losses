"""
This file contains Python code for a Streamlit app.

Author: Ze Hong Wu

Anyone who edits this file and pushes their changes to master or Pull Requests their changes
should also add their name to this docstring.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
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
    A failed attempt to create a Plotly subplot using figure objects.
    Traces were too confusing for me and there seems to be no good way
    to fit figure objects into subplots.

    https://stackoverflow.com/questions/71623896/create-a-histogram-with-plotly-graph-objs-like-in-plotly-express
    """
    #go.Figure(data=[go.Histogram(ru_ua_concat, x="date_lost", y="user", histfunc="count")])
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.00)
    fig1 = go.Histogram( 
                    x=ru_ua_concat[ru_ua_concat["user"] == "Russia"]["date_lost"], 
                    y=ru_ua_concat[ru_ua_concat["user"] == "Russia"]["user"], 
                    histfunc="count", nbinsx=500,
                    name="Russia",
                    marker=dict(color="red"))
    fig.append_trace(fig1, row=2, col=1)
    fig2 = go.Histogram(
                    x=ru_ua_concat[ru_ua_concat["user"] == "Ukraine"]["date_lost"], 
                    y=ru_ua_concat[ru_ua_concat["user"] == "Ukraine"]["user"], 
                    histfunc="count", nbinsx=500,
                    name="Ukraine",
                    marker=dict(color="blue"),
                    )
    #fig2.update(yaxis_range=[0,50]) #also broken and useless
    fig.append_trace(fig2, row=1, col=1)
    fig.update_layout(height=700, width=1000, title_text="RU/UA Losses")
    fig.update_yaxes(autorange="reversed", row=2, col=1)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(range=[0,45], row=1, col=1) # completely broken and useless
    return fig

def update_loss_time_graph():
    """
    Generates an overlaid vehicle losses histogram.
    """
    # reference: https://stackoverflow.com/questions/65856933/plotly-how-to-plot-histogram-with-x-hour
    #print(ru_ua_dates.reset_index())
    figure = px.histogram(ru_ua_concat, x="date_lost", y="user", histfunc="count",
                          color="user",
                          color_discrete_map={"Russia": "red", "Ukraine": "blue"},
                          nbins=500,
                          labels={
                              "date_lost": "Date",
                              "user": "Vehicles lost",
                              "count": "Vehicles lost"
                          },
                          barmode="overlay",
                          width=1000, height=500, opacity=0.75
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
    figure.update_yaxes(
        range=(0, 50),
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

with st.sidebar:
    st.text("sidebar text")

st.text("Hello, world")
st.dataframe(ru_ua_dates)
st.write("#### Vehicle losses over time for Russia and Ukraine, \
         per day, from 24 February 2022 to 18 October 2023:")
st.plotly_chart(update_loss_time_graph())
st.plotly_chart(stacked_loss_graph())