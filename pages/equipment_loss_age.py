"""
Author: Jin Lin
Ported to Streamlit by Ze Hong Wu.
"""

# Import library
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load the CSV data
df_ru = pd.read_csv("data/oryx/ru_losses.csv")
df_ua = pd.read_csv("data/oryx/ua_losses.csv")

# Drop rows with null values
df_ru = df_ru.dropna()
df_ua = df_ua.dropna()

# Streamlit app
st.title("Military Vehicle Losses")


# Toggle buttons for displaying Russian and Ukrainian histograms
show_ru_histogram = st.checkbox('Show Russian Histogram', value=True)
show_ua_histogram = st.checkbox('Show Ukrainian Histogram', value=True)

# Combine histograms using Plotly
fig_combined = go.Figure()

# Add Russian histogram if the button is checked
if show_ru_histogram:
    fig_combined.add_trace(go.Histogram(x=df_ru["year_first_produced"], nbinsx=20, name="Russian"))

# Add Ukrainian histogram if the button is checked
if show_ua_histogram:
    fig_combined.add_trace(go.Histogram(x=df_ua["year_first_produced"], nbinsx=20, name="Ukrainian"))

# Update layout for the combined chart
fig_combined.update_layout(
    title_text="Combined Histogram of Production Year",
    xaxis_title="Production Year",
    yaxis_title="Count",
    barmode="overlay"
)

# Show combined chart
st.plotly_chart(fig_combined)


st.write("There are people saying that Russia is using older and older vehicles. This page is made\
         in response to those Unsubstantiated claims. Compared to the situation in Ukraine, there is no clear \
         evidence that Russia is using older vehicles.")

# below is the second chart

# reference https://www.nomidl.com/projects/russia-ukraine-war-data-analysis-project-using-python/#google_vignette

# Set Plotly template
pio.templates.default = 'plotly_dark'
color_theme = px.colors.qualitative.Antique

# Read data
df3 = pd.read_csv('data/russia_losses_equipment.csv')

# Drop unnecessary columns
df3.drop(columns=['mobile SRBM system', 'military auto', 'fuel tank', 'vehicles and fuel tanks'], inplace=True)


# Create Streamlit app
st.title('Russia Equipment Losses')

# Plotly figure
fig = go.Figure()

titles = ["Aircraft", "Helicopter", "Drone"]  
columns_to_plot = [2, 3, 8]

fig = make_subplots(rows=1, cols=3, subplot_titles=titles)

for i, col_index in enumerate(columns_to_plot, 1):
    fig.add_trace(go.Scatter(x=df3['date'], name=titles[i-1], y=df3.iloc[:, col_index]),
                  row=1, col=i)

fig.update_layout(showlegend=True)

# Update layout
fig.update_layout(title='Russia Equipment Losses', showlegend=False, height=350, width=250)

fig.update_xaxes(dtick='M5', tick0=df3['date'].iloc[0])

fig.update_layout(font_color='#11DEC6')

# Display the figure in Streamlit app
st.plotly_chart(fig, use_container_width=True)

st.write("At the beginning of the war, Russia suffered significant losses of aircraft and \
         helicopters. However, the rate of aircraft and helicopter losses for Russia quickly \
         decreased. This could be due to various reasons. One possibility is that Russia decided \
         to switch to drones. It can be observed that while the loss rate for aircraft and \
         helicopters is decreasing, the loss rate for drones is increasing. This may also be \
         one of the reasons why people think Russia is using increasingly older equipment.")