"""
This file contains Python code for a Streamlit page.
This page discusses the sources of the data used for this project.

Author: Ze Hong Wu

Anyone who edits this file and pushes their changes to master or Pull Requests their changes
should also add their name to this docstring.
"""

import streamlit as st

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

st.title('Attributions: Sources for our data')
st.text('Author: Ze Hong Wu')
st.markdown(
    """
    Our primary source of data is the \
    [Oryx blog](https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html), \
    which contains individual confirmed vehicles lost in Ukraine as well as \
    image proof of their loss and (sometimes) dates when they were lost.

    We chose this source of data for the following reasons:
    - the people maintaining the blog inspects each new entry to ensure that it is:
      - it is real
      - it is not a duplicate of a previous entry
      - it pertains to the conflict in Ukraine
    - every entry has an image proof attached
    """
)