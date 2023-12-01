"""


Author: Alan Mackiewicz
Ported to Streamlit by Ze Hong Wu.

Had some trouble figuring out what to do with the donated vehicles csv but I made one nice presentation with the data so far

"""

from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import streamlit as st

file_path = 'data/oryx/donated_vehicles.csv'  
donated_vehicles_df = pd.read_csv(file_path)

# Grouping the data by supplier and sum the counts
supplier_vehicle_count = donated_vehicles_df.groupby('supplier')['count'].sum().reset_index()

# Sort from greatest to least
supplier_vehicle_count = supplier_vehicle_count.sort_values(by='count', ascending=False)


fig = px.bar(supplier_vehicle_count, y='supplier', x='count', 
             title='Total Number of Vehicles Donated to Ukraine by Supplier',
             labels={'count': 'Number of Vehicles', 'supplier': 'Supplier Country/Organization'},
             orientation='h', color='supplier')

#updated layout for better visuals
fig.update_layout(
    xaxis_title='Number of Vehicles',
    yaxis_title='Supplier Country/Organization',
    plot_bgcolor='white',
    yaxis=dict(categoryorder='total ascending'),
    height=600,  
    margin=dict(l=150) 
)

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
with st.sidebar:
    st.text("sidebar")

st.title("Vehicles Donated to Ukraine Visualization")
st.plotly_chart(fig)

# app = Dash(__name__)


# app.layout = html.Div([
#     html.H1("Vehicles Donated to Ukraine Visualization"),
#     dcc.Graph(figure=fig)
# ])


# if __name__ == '__main__':
#     app.run_server(debug=True)
