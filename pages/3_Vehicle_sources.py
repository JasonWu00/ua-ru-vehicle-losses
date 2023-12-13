"""
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

Last minute addition.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

# Copied from a deprecated dashboard.

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

# create new dfs to store the sum of each type of loss.
ru_losses_sum = pd.DataFrame(columns=losses_types)
ua_losses_sum = pd.DataFrame(columns=losses_types)
ru_losses_sum.loc[0] = [0,0,0,0,0]
ua_losses_sum.loc[0] = [0,0,0,0,0]
for my_type in losses_types:
    ru_losses_sum[my_type].loc[0] = ru_df[my_type].sum()
    ua_losses_sum[my_type].loc[0] = ua_df[my_type].sum()

# rotate, turn index into entries, and rename columns
# to make the dfs fit px histograms
ru_losses_sum = ru_losses_sum.transpose()
ua_losses_sum = ua_losses_sum.transpose()
ru_losses_sum = ru_losses_sum.reset_index()
ua_losses_sum = ua_losses_sum.reset_index()
ru_losses_sum.rename(columns={0: "count"}, inplace=True)
ua_losses_sum.rename(columns={0: "count"}, inplace=True)

def update_manufacturers_graph(col_chosen):
    """
    Histogram of manufacturers.
    """
    if col_chosen == "Russia":
        figure=px.histogram(ru_df,
                            title="Russia's lost vehicles by country of origin",
                            y='manufacturer',
                            x='losses_total',
                            histfunc='sum',
                            # color="manufacturer",
                            # color_discrete_map = {"Soviet Union": "red"},
                            #orientation='h'
                            )
        figure.update_layout(
            xaxis_title='Total vehicles lost',
            yaxis_title='Manufacturer country',
            yaxis={"categoryorder": 'total ascending'},
            width=800,
            height=400,
        )
    elif col_chosen == "Ukraine":
        figure=px.histogram(ua_df,
                            title="Ukraine's lost vehicles by country of origin",
                            y='manufacturer',
                            x='losses_total',
                            histfunc='sum',
                            # color="manufacturer",
                            # color_discrete_map = {"Soviet Union": "red"},
                            #orientation='h'
                            )
        figure.update_layout(
            xaxis_title='Total vehicles lost',
            yaxis_title='Manufacturer country',
            yaxis={"categoryorder": 'total ascending'},
            width=800,
            height=650,
        )
    return figure

# Copied over from the corresponding Streamlit page for vehicles lost by date.
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

st.title("Rallying to War: Sources of Vehicles")
st.text('Author: Ze Hong Wu')
st.markdown(
"""
#### Introduction

This page will discuss the sources of vehicles used and lost by Russia and Ukraine.

#### Visualizations
""")

st.plotly_chart(update_manufacturers_graph("Russia"))
st.markdown(
"""
The two graphs above and below shows the distributions of vehicles lost by Russia and Ukraine, \
distinguished by the country those vehicles are made at. 

Note that the Soviet Union and Yugoslavia \
no longer exist and their bars represent old stock inherited from them after their dissolutions.
""")
st.plotly_chart(update_manufacturers_graph("Ukraine"))

st.markdown(
"""
#### Analysis
Russia relies extremely heavily on a combination of inherited Soviet stock and self produced gear, \
with very little in terms of foreign sourced equipment. Notice that China, despite being in a \
strategic alliance with Russia, has provided little of note. There are various possible reasons \
for this, ranging from avoiding sanctions to opportunistic back-stabbing, but the data alone \
cannot definitely identify any one of them as the true reason.

While Ukraine also relies on Soviet inherited stock and self produced gear, they also have access \
to donated and supplied material from a number of countries such as the United States and various \
European countries. The disjunction between Russia's few sources and Ukraine's many sources \
indicate very directly that the major governments of the world are aligned with Ukraine and \
against Russia. Of the countries aligned with Russia, they have provided Russia with either \
nothing, materials too small in number to be recorded as lost, or non-vehicle support.
"""
)

