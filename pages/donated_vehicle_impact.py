"""


Author: Alan Mackiewicz
Ported to Streamlit by Ze Hong Wu.

Had some trouble figuring out what to do with the donated vehicles csv but I made one nice presentation with the data so far

"""

from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import streamlit as st

file_path_donations = 'data/ukraine-ps-contributions.csv'
ps_donations_df = pd.read_csv(file_path_donations)


ps_donations_df['Business sector'] = ps_donations_df['Business sector'].str.strip().str.lower().replace(['communications services'], 'communication services')

# Remove the row with 'Business sector' as '0'
ps_donations_df = ps_donations_df[ps_donations_df['Business sector'] != '0']

# Aggregate the data to get the sum of 'Est USD value' and list of distinct 'Private sector donors'
sector_aggregated = ps_donations_df.groupby('Business sector').agg({
    'Est USD value': 'sum',
    'Private sector donor': lambda x: ', '.join(x.unique())
}).reset_index()

file_path = 'data/oryx/donated_vehicles.csv'  
donated_vehicles_df = pd.read_csv(file_path)

# Group the data by supplier and sum the counts
supplier_vehicle_count = donated_vehicles_df.groupby('supplier')['count'].sum().reset_index()

supplier_vehicle_count = supplier_vehicle_count.sort_values(by='count', ascending=False)


fig = px.bar(supplier_vehicle_count, y='supplier', x='count', 
             title='Total Number of Vehicles Donated to Ukraine by Supplier',
             labels={'count': 'Number of Vehicles', 'supplier': 'Supplier Country/Organization'},
             orientation='h', color='supplier')


fig.update_layout(
    xaxis_title='Number of Vehicles',
    yaxis_title='Supplier Country/Organization',
    plot_bgcolor='rgba(0, 0, 0, 0)',  
    bargap=0.10, 
    yaxis=dict(categoryorder='total ascending'),
    width=1000, 
    height=650,
    margin=dict(l=50, r=50) 
)


#fig2 total money donated
sector_donation_sum = ps_donations_df.groupby('Business sector')['Est USD value'].sum().reset_index()

sector_donation_sum = sector_donation_sum.sort_values(by='Est USD value', ascending=False)

fig2 = px.bar(sector_donation_sum, x='Business sector', y='Est USD value', 
              title='Total Donation Amount by Business Sector',
              labels={'Est USD value': 'Total Estimated Value (USD)', 'Business sector': 'Business Sector'})
fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', bargap=0.15, width=1000, height=600)


#fig3 company donations
sector_donation_count = ps_donations_df.groupby('Business sector').size().reset_index(name='Donations Count')

sector_donation_count = sector_donation_count.sort_values(by='Donations Count', ascending=False)

fig3 = px.bar(sector_donation_count, x='Business sector', y='Donations Count', 
              title='Number of Donations by Business Sector',
              labels={'Donations Count': 'Number of Donations', 'Business sector': 'Business Sector'})
fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', bargap=0.15, width=1000, height=600)

#fig4 Pie Chart

donation_status_count = ps_donations_df.groupby('Donation status').size().reset_index(name='Count')

fig4 = px.pie(donation_status_count, names='Donation status', values='Count', 
              title='Distribution of Donation Status (Paid vs Pledged)')
fig4.update_traces(textposition='inside', textinfo='percent+label')
fig4.update_layout(width=1000, height=600)

#fig5 actual companies who donated
top_donors = ps_donations_df.groupby('Private sector donor')['Est USD value'].sum().reset_index()
top_donors = top_donors.sort_values(by='Est USD value', ascending=False).head(10)
fig5 = px.bar(top_donors, x='Private sector donor', y='Est USD value', 
              title='Top 10 Donors by Total Donation Amount',
              labels={'Est USD value': 'Total Estimated Value (USD)', 'Private sector donor': 'Donor'})
fig5.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', bargap=0.15, width=1000, height=600)

#fig6 world map 
country_donation_sum = ps_donations_df.groupby('Donor country of registration')['Est USD value'].sum().reset_index()
fig6 = px.choropleth(country_donation_sum, locations='Donor country of registration',
                     color='Est USD value', 
                     locationmode='country names',
                     title='Geographical Distribution of Donors by Total Donation Amount')
fig6.update_geos(projection_type="natural earth")
fig6.update_layout( width=1000, height=600)





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

st.title("Ukraine Donation Visualizer")
st.plotly_chart(fig)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
st.plotly_chart(fig5)
st.plotly_chart(fig6)


# app = Dash(__name__)


# app.layout = html.Div([
#     html.H1("Vehicles Donated to Ukraine Visualization"),
#     dcc.Graph(figure=fig)
# ])


# if __name__ == '__main__':
#     app.run_server(debug=True)
