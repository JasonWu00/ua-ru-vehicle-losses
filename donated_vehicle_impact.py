"""
Author: Alan Mackiewicz

Had some trouble figuring out what to do with the donated vehicles csv but I made one nice presentation with the data so far

"""

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load the data for donated vehicles
file_path_vehicles = 'data/oryx/donated_vehicles.csv'
donated_vehicles_df = pd.read_csv(file_path_vehicles)

# Grouping the data by supplier and sum the counts (removing duplicates)
supplier_vehicle_count = donated_vehicles_df.groupby('supplier')['count'].sum().reset_index()

# Sort from greatest to least
supplier_vehicle_count = supplier_vehicle_count.sort_values(by='count', ascending=False)

# Load the humanitarian aid data
file_path_aid = 'data/ukraine-ps-contributions.csv'
ukraine_aid_data = pd.read_csv(file_path_aid)

# Standardize the 'Business sector' column (remove leading/trailing spaces, convert to a consistent case)
ukraine_aid_data['Business sector'] = ukraine_aid_data['Business sector'].str.strip().str.lower()

# Grouping the data by business sector and sum the estimated USD value (removing duplicates)
sector_donation_value = ukraine_aid_data.groupby('Business sector')['Est USD value'].sum().reset_index()

# Grouping the data by business sector and count the number of donations (removing duplicates)
sector_donation_count = ukraine_aid_data.groupby('Business sector').size().reset_index(name='Donation Count')

# Sort from greatest to least by donation value
sector_donation_value = sector_donation_value.sort_values(by='Est USD value', ascending=False)

# Sort from greatest to least by donation count
sector_donation_count = sector_donation_count.sort_values(by='Donation Count', ascending=False)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Ukraine Support Visualization"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Vehicles Donated by Supplier', 'value': 'VEH'},
            {'label': 'Total Value of Donations by Business Sector', 'value': 'VAL'},
            {'label': 'Number of Donations by Business Sector', 'value': 'CNT'}
        ],
        value='VEH',
        clearable=False
    ),
    dcc.Graph(id='main-graph')
])

@app.callback(
    Output('main-graph', 'figure'),
    [Input('graph-type', 'value')]
)
def update_graph(graph_type):
    if graph_type == 'VEH':
        fig = px.bar(supplier_vehicle_count, y='supplier', x='count', 
                     title='Total Number of Vehicles Donated to Ukraine by Supplier',
                     labels={'count': 'Number of Vehicles', 'supplier': 'Supplier Country/Organization'},
                     orientation='h', color='supplier')
        fig.update_layout(yaxis=dict(categoryorder='total ascending'))
    elif graph_type == 'VAL':
        fig = px.bar(sector_donation_value, x='Business sector', y='Est USD value', 
                     title='Total Value of Donations by Business Sector',
                     labels={'Est USD value': 'Estimated USD Value', 'Business sector': 'Business Sector'})
        fig.update_layout(
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Roboto"
            )
        )
    else:  
        fig = px.bar(sector_donation_count, x='Business sector', y='Donation Count', 
                     title='Number of Donations by Business Sector',
                     labels={'Donation Count': 'Number of Donations', 'Business sector': 'Business Sector'},
                     color='Business sector')
    
    fig.update_layout(plot_bgcolor='white', height=600, margin=dict(l=150))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


