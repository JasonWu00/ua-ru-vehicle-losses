"""


Author: Alan Mackiewicz
Ported to Streamlit by Ze Hong Wu.

presented are three visuals regarding civilian impact in the war. No insight is given however but will be added shortly.

"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import streamlit as st

# Load and preprocess the datasets
file_path_civilian_harm = 'data/civilianHarm.csv'
file_path_missile_attacks = 'data/missile_attacks_daily.csv'
ukr_refugee_data_path = 'data/UKR_refugee_by_countries.csv' 

civilian_harm_df_provided = pd.read_csv(file_path_civilian_harm)
missile_attacks_df = pd.read_csv(file_path_missile_attacks)
ukr_refugee_data = pd.read_csv(ukr_refugee_data_path)  

#parsing for time in missile attacks
def parse_datetime(dt):
    try:
        return pd.to_datetime(dt, format='%Y-%m-%d %H:%M', errors='coerce')
    except ValueError:
        return pd.to_datetime(dt, format='%Y-%m-%d', errors='coerce')

missile_attacks_df['time_start'] = missile_attacks_df['time_start'].apply(parse_datetime)

# Preprocess and aggregate data for timeline (grouped by month)
civilian_harm_df_provided['date'] = pd.to_datetime(civilian_harm_df_provided['date'])
civilian_timeline_provided = civilian_harm_df_provided.groupby(civilian_harm_df_provided['date'].dt.to_period('M')).size().reset_index(name='counts')
civilian_timeline_provided['date'] = civilian_timeline_provided['date'].dt.to_timestamp()

missile_timeline = missile_attacks_df.groupby(missile_attacks_df['time_start'].dt.to_period('M')).size().reset_index(name='counts')
missile_timeline['time_start'] = missile_timeline['time_start'].dt.to_timestamp()

# Timeline Visualization 
fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(x=civilian_timeline_provided['date'], y=civilian_timeline_provided['counts'], mode='lines', name='Civilian Casualties'))
fig_timeline.add_trace(go.Scatter(x=missile_timeline['time_start'], y=missile_timeline['counts'], mode='lines', name='Missile Attacks'))
fig_timeline.update_layout(title='Timeline of Events', xaxis_title='Date', yaxis_title='Number of Events')

# Geographical Heatmap with hover effect
fig_map = px.scatter_geo(civilian_harm_df_provided, lat='latitude', lon='longitude', hover_name='description', title='Geographical Distribution of Civilian Casualties', scope='europe')
fig_map.update_geos(center=dict(lat=48.3794, lon=31.1656), projection_scale=5)

# get only recent data from the immigration csv
ukr_refugee_data['date'] = pd.to_datetime(ukr_refugee_data['date'])
latest_refugee_data = ukr_refugee_data.sort_values('date').groupby('country').tail(1)

# Sort the data
latest_refugee_data_sorted = latest_refugee_data.sort_values('individuals', ascending=True)

fig_refugee_bar_latest = px.bar(
    latest_refugee_data_sorted, 
    x='individuals', 
    y='country', 
    orientation='h', 
    labels={'individuals': 'Number of Individuals', 'country': 'Country'}
)
fig_refugee_bar_latest.update_layout(title='Most Recent Number of Ukrainian Refugees by Country')

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

st.title("Analysis of Ukraine Conflict Data")
st.text("Placeholder text.")
st.plotly_chart(fig_timeline)
st.plotly_chart(fig_map)
st.plotly_chart(fig_refugee_bar_latest)

# app = Dash(__name__)


# app.layout = html.Div([
#     html.H1("Analysis of Ukraine Conflict Data"),
#     dcc.Graph(figure=fig_timeline),
#     dcc.Graph(id='map', figure=fig_map),
#     dcc.Graph(figure=fig_refugee_bar_latest),  
#     html.Div(id='detail-visualization', children=[
#         html.H3("Detail Visualization"),
        
#     ])
# ])

# # Callback for the interactive map
# @app.callback(
#     Output('detail-visualization', 'children'),
#     Input('map', 'hoverData')
# )
# def update_detail_visualization(hoverData):
#     if hoverData is not None and 'points' in hoverData:

#         # Extract hovered point's latitude and longitude
#         lat = hoverData['points'][0]['lat']
#         lon = hoverData['points'][0]['lon']
        

# if __name__ == '__main__':
#     app.run_server(debug=True)