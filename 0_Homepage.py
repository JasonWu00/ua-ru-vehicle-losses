"""
Copyright (C) 2023 Ze Hong Wu, Alan Mackiewicz

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

#import dash
#from dash import html, dcc
#from dash.dependencies import Input, Output
import pandas as pd
#import random
import streamlit as st



comments_df = pd.read_csv('data/comments_data.csv')

#app = dash.Dash(__name__, suppress_callback_exceptions=True)

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

st.markdown("<h1 style='text-align: center;'>\"Novorossiya\": Analysis on the War in Ukraine</h1>",
            unsafe_allow_html=True)
# Streamlit handles the nav menu in the left sidebar by default
# I am not recreating the Twitter box thing since class time is not far away.
st.text("Authors: Alan Mackiewitz, Jin Lin, Ze Hong Wu")

st.markdown(
"""
This project last collected data on 15 October 2023. \
Events and developments after that date (such as the Kursk offensive or the \
imminent arrival of North Korean troops, as of 26 October 2024) will not be shown.

When was the last time you thought about the war in Ukraine?

Have you, between 24 February 2022 and now, seen or heard any of these statements?
* The Kyiv offensive is a feint
* The Kharkiv / Kherson battles are futile gestures, Russia has lost nothing at all
* Russia has destroyed 60 HIMARS (or some other large number of Western equipment)

If you have heard or seen one or more of these statements, or other similar statements, \
and want to know if any of them are legitimate, the pages listed on the left sidebar \
might provide some useful context.
""")

# There used to be Dash code here. It's been nuked.
# Check the GitHub repo history for a version of this file when it used to exist.
