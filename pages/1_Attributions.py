"""
This page discusses the sources of the data used for this project.

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
    along with this program.  If not, see <https://www.gnu.org/licenses/>

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

While the data quality has room for improvement, its status as a verified minimum baseline \
made the Oryx blog our primary data source.
""")
