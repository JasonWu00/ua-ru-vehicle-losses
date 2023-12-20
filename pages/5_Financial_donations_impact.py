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

Had some trouble figuring out what to do with the donated vehicles ccsv, 
but I made one nice presentation with the data so far.
- Alan Mackiewicz

"""

#from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import streamlit as st

file_path_donations = 'data/ukraine-ps-contributions.csv'
ps_donations_df = pd.read_csv(file_path_donations)


ps_donations_df['Business sector'] = ps_donations_df['Business sector']\
            .str.strip().str.lower().\
                replace(['communications services'], 'communication services')

# Remove the row with 'Business sector' as '0'
ps_donations_df = ps_donations_df[ps_donations_df['Business sector'] != '0']

# Aggregate the data to get the sum of 'Est USD value' and list of distinct 'Private sector donors'
sector_aggregated = ps_donations_df.groupby('Business sector').agg({
    'Est USD value': 'sum',
    'Private sector donor': lambda x: ', '.join(x.unique())
}).reset_index()

file_path = 'data/oryx/donated_vehicles.csv'
donated_vehicles_df = pd.read_csv(file_path)

# NONE isn't a country or group.
donated_vehicles_df = donated_vehicles_df[\
    donated_vehicles_df["supplier"] != "NONE"]
# This is about Ukraine, not Russia.
donated_vehicles_df = donated_vehicles_df[\
    donated_vehicles_df["recipient"] == "Ukraine"]

# Group the data by supplier and sum the counts
supplier_vehicle_count = donated_vehicles_df.groupby('supplier')['count'].sum().reset_index()

supplier_vehicle_count = supplier_vehicle_count.sort_values(by='count', ascending=False)


fig = px.bar(supplier_vehicle_count, y='supplier', x='count',
             title='Total Number of Vehicles Donated to Ukraine by Different Suppliers',
             labels={'count': 'Number of Vehicles', 'supplier': 'Supplier Country/Organization'},
             orientation='h', color='supplier')


fig.update_layout(
    xaxis_title='Number of Vehicles',
    yaxis_title='Supplier Country/Organization',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    bargap=0.10,
    yaxis={"categoryorder": 'total ascending'},
    width=1000,
    height=800,
    margin={"l": 50, "r": 50}
)


#fig2 total money donated
sector_donation_sum = ps_donations_df.groupby(
    'Business sector')['Est USD value'].sum().reset_index()

sector_donation_sum = sector_donation_sum.sort_values(by='Est USD value', ascending=False)

fig2 = px.bar(sector_donation_sum, x='Business sector', y='Est USD value',
              title='Total Donation Amount by Different Business Sectors',
              labels={'Est USD value': 'Total Estimated Value (USD)',
                      'Business sector': 'Business Sector'},
              color='Est USD value')
fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', bargap=0.15, width=1000, height=600)


#fig3 company donations
sector_donation_count = ps_donations_df.groupby('Business sector').size()\
                                        .reset_index(name='Donations Count')

sector_donation_count = sector_donation_count.sort_values(by='Donations Count', ascending=False)

fig3 = px.bar(sector_donation_count, y='Business sector', x='Donations Count',
              title='Number of Donations by Different Business Sectors',
              labels={'Donations Count': 'Number of Donations',
                      'Business sector': 'Business Sector'},
              orientation='h', color='Donations Count')
fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', bargap=0.15, width=1000, height=600)

#fig4 Pie Chart

donation_status_count = ps_donations_df.groupby('Donation status').size().reset_index(name='Count')

fig4 = px.pie(donation_status_count, names='Donation status', values='Count', 
              title='Distribution of Donation Status From Donors(Paid vs Pledged)', hole=0.3)
fig4.update_traces(textposition='inside', textinfo='percent+label')
fig4.update_layout(width=1000, height=600)

#fig5 actual companies who donated
top_donors = ps_donations_df.groupby('Private sector donor')['Est USD value'].sum().reset_index()
top_donors = top_donors.sort_values(by='Est USD value', ascending=False).head(20)
fig5 = px.treemap(
    top_donors,
    path=['Private sector donor'],
    values='Est USD value',
    title='Tree Map of Top 20 Donors by Total Donation Amount'
)

fig5.update_traces(
    textinfo='label+value',
    textfont={"size": 20, "color": "black"}
)

fig5.update_layout(width=1000, height=600)


#fig6 world map

# US of A is severely skewing the data. Removed them. They will be discussed in the analysis.
ps_donations_df = ps_donations_df[\
    ps_donations_df['Donor country of registration'] != 'United States of America']

country_donation_sum = ps_donations_df.groupby(
    'Donor country of registration')['Est USD value'].sum().reset_index()
fig6 = px.choropleth(country_donation_sum, locations='Donor country of registration',
                     color='Est USD value',
                     locationmode='country names',
                     color_continuous_scale='blues',
                     title='Geographical Distribution of Donors by Total Donation Amount',
                     hover_name='Donor country of registration', hover_data=['Est USD value'])

fig6.update_geos(
    projection_type="natural earth",
    landcolor='gray',
    oceancolor='black',
    showcountries=False,
)

fig6.update_layout(
    width=1000,
    height=600,
    paper_bgcolor='black',
    geo_bgcolor='black',
    title_font_color='white',
    font_color='white',
    margin={"l": 0, "r": 0, "t": 50, "b": 0},
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

st.title("Soft Factors: Monetary Donations to Ukraine")
st.text('Author: Alan Mackiewicz')

st.markdown(
"""
This page focuses mostly on monetary donations made to Ukraine.
"""
)

st.plotly_chart(fig)
st.markdown(
"""
As displayed, the United States donated the most vehicles to the war effort by a significant degree.

Possible reasons for this include:
- Providing aid to a country in need, much like the Lend-Lease Act of World War II
- "Bleeding Russia dry" by indirectly aiding in their military humiliation and bruising
- Live testing of equipment
- Disposing of older equipment by sending them to be used instead of paying for decommissioning
""")

st.plotly_chart(fig5)
st.markdown(
"""
Above are the top 20 leading companies who donated to Ukraine. \
As this data does not inform us of their exact intentions, we will refrain from speculating.
""")

st.plotly_chart(fig2)
st.markdown(
"""
Here we see total monetary donations to Ukraine, in United States Dollars, from different sectors.
""")
st.plotly_chart(fig3)
st.markdown(
"""
Total donations, by business sector.
""")

st.plotly_chart(fig4)
st.markdown(
"""
The pie chart above shows the ratio of pledged to committed donations. \
Whether the pledged donations are undergoing bureaucracy or exist solely for publicity \
will be left as an exercise to the reader.
""")

st.plotly_chart(fig6)
st.markdown(
"""
The heatmap displays regions of the world distinguished by monetary donations to Ukraine.

The United States is not shown on this heat map due to their total private monetary donations \
of 933 million USD massively skewing the heat map scale. The next runner up is Germany with \
123 million USD equivalent of donations.

The United States stand at the front of the pack, which is to be expected given the military \
and civilian aid they have provided already. China's relative lack of donations, despite having a \
similarly sized economy, can be explained by their political alliance with Russia.
""")


# app = Dash(__name__)


# app.layout = html.Div([
#     html.H1("Vehicles Donated to Ukraine Visualization"),
#     dcc.Graph(figure=fig)
# ])


# if __name__ == '__main__':
#     app.run_server(debug=True)
