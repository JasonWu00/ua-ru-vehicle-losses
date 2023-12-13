"""
Copyright (C) 2023 Alan Mackiewicz, Ze Hong Wu

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

Presented are three visuals regarding civilian impact in the war. 
No insight is given however but will be added shortly.
- Alan Mackiewicz

Updated analyses with additional context and cut out some problematic statements.
- Ze Hong Wu

"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from dash import Dash, html, dcc, Input, Output
import streamlit as st

# Load and preprocess the datasets
file_path_civilian_harm = 'data/civilianHarm.csv'
file_path_missile_attacks = 'data/missile_attacks_daily.csv'
ukr_refugee_data_path = 'data/UKR_refugee_by_countries.csv'

civilian_harm_df_provided = pd.read_csv(file_path_civilian_harm)
missile_attacks_df = pd.read_csv(file_path_missile_attacks)
ukr_refugee_data = pd.read_csv(ukr_refugee_data_path)

# parsing for time in missile attacks
def parse_datetime(dt):
    """
    See func name.
    """
    try:
        return pd.to_datetime(dt, format='%Y-%m-%d %H:%M', errors='coerce')
    except ValueError:
        return pd.to_datetime(dt, format='%Y-%m-%d', errors='coerce')

missile_attacks_df['time_start'] = missile_attacks_df['time_start'].apply(parse_datetime)

# Preprocess and aggregate data for timeline (grouped by month)
civilian_harm_df_provided['date'] = pd.to_datetime(civilian_harm_df_provided['date'])
civilian_timeline_provided = civilian_harm_df_provided.groupby(
                            civilian_harm_df_provided['date'].dt.to_period('M')
                            ).size().reset_index(name='counts')
civilian_timeline_provided['date'] = civilian_timeline_provided['date'].dt.to_timestamp()

missile_timeline = missile_attacks_df.groupby(
                                    missile_attacks_df['time_start'].dt.to_period('M')
                                    ).size().reset_index(name='counts')
missile_timeline['time_start'] = missile_timeline['time_start'].dt.to_timestamp()

# Timeline Visualization 
fig_timeline = go.Figure()
fig_timeline.add_trace(
    go.Scatter(x=civilian_timeline_provided['date'],
               y=civilian_timeline_provided['counts'],
               mode='lines', name='Civilian Casualties'))
fig_timeline.add_trace(
    go.Scatter(x=missile_timeline['time_start'],
               y=missile_timeline['counts'],
               mode='lines', name='Missile Attacks',
               line={"color": "red"}))
fig_timeline.update_layout(
    title='Missile Attacks in Relation to Civilian Casualties', 
    xaxis_title='Date', yaxis_title='Number of Events',width=1000, height=400)

# Geographical Heatmap with hover effect
fig_map = px.scatter_geo(civilian_harm_df_provided, lat='latitude', lon='longitude',
                         hover_name='description',
                         title='Geographical Distribution of Civilian Casualties',
                         scope='europe')

fig_map.update_traces(marker={"opacity": 0.4, "size": 7,})
fig_map.update_geos(center={"lat": 48.3794, "lon": 31.1656}, projection_scale=5)
fig_map.update_layout(
    width=1000,
    height=800,
    geo={"bgcolor": "black"}
)

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
    labels={'individuals': 'Number of Individuals', 'country': 'Country'},
)

#fig_refugee_bar_latest.update_traces(marker_color='#FFA500')


fig_refugee_bar_latest.update_layout(
    title='Most Recent Number of Ukrainian Refugees by Country',
    width=1000, height=400)


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

st.title("No Innocents in Hell: The War's Impact on Civilians")
st.text('Author: Alan Mackiewicz')
st.plotly_chart(fig_timeline)
st.markdown(
"""
Disclaimer: Missile data is not available for the initial months of the conflict.

The data shows that civilian casualties correlate with occurrences of Russian missile strikes. \
While this data alone is insufficient in determining malicious intent from Russia, it does suggest \
that their missile strikes lead to civilian deaths.
""")
st.plotly_chart(fig_map)
st.markdown(
"""
The distribution of civilian deaths contain several notable details:

1. There is a great band of recorded deaths along the eastern frontlines from Kharkiv, \
southeast to Bakhmut, then south-southwest through Zaporizhzhia and into Kherson. This \
is to be expected, since the primary front lines after the failed Kyiv Offensive \
occurs in this direction.
2. There are four lesser but still distinct blobs of civilian deaths not on the frontlines, \
centered around the cities:
    - Kyiv (north of center)
    - Lviv (west)
    - Mariupol (south of the eastern portion of the front lines)
    - Mykolaiv (south-west of the southern portion of the front lines)

The losses in Lviv + Mykolaiv can be explained as the results of Russian missile strikes \
against Ukrainina infrastructure, while those in Kyiv + Mykolaiv and Mariupol correspond \
to the failed and successful Russian attacks in those directions respectively.

3. There is a lone dot on the Ukraine-Poland border, corresponding to the stray missile that \
landed in Poland in November 2022.
""")
st.plotly_chart(fig_refugee_bar_latest)
st.markdown(
"""
The data here describes the movement of Ukrainian refugees.

The largest number of them moved to Poland, which is to be expected as they border Ukraine \
in the direction opposite of Russia.

The second largest number of them moved to Russia. Why an invaded population might choose to move \
to the invader nation can be explained by a few possible reasons, primarily:
- Forced deportation by Russian invasion forces
- Ukrainians in the Donbas and Crimea identifying with and moving into Russia

Unfortunately, due to limitations in our data, it is not possible to determine the proportion of \
willing and deported refugees from our data alone.

The next several categories all consist of friendly European countries bordering Ukraine or \
bordering one of these aforementioned border countries. Since most refugees likely do not have \
the capacity or reason to go far, this is to be expected.
""")

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
