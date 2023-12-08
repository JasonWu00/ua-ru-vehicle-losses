import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Set Plotly template
pio.templates.default = 'plotly_dark'
color_theme = px.colors.qualitative.Antique

# Read data
df3 = pd.read_csv('data/russia_losses_equipment.csv')

# Drop unnecessary columns
df3.drop(columns=['mobile SRBM system', 'military auto', 'fuel tank', 'vehicles and fuel tanks'], inplace=True)


# Create Streamlit app
st.title('Equipment Losses')

# Plotly figure
fig = go.Figure()
titles = []

for i in list(df3.columns[2:]):
    title = i
    if i[0].isupper() == False:
        title = i.title()
    titles += [title]

fig = make_subplots(rows=3, cols=3, subplot_titles=titles)

for i in range(3):
    for j in range(3):
        index = 2 + (j + i * 3)
        if index < len(titles):
            fig.add_trace(go.Scatter(x=df3['date'], name=titles[index], y=df3.iloc[:, index]),
                          row=i + 1, col=j + 1)

# Update layout
fig.update_layout(title='Equipment Losses', showlegend=False, height=850, width=750)

fig.update_xaxes(dtick='M6', tick0=df3['date'].iloc[0])

fig.update_layout(font_color='#11DEC6')

# Display the figure in Streamlit app
st.plotly_chart(fig, use_container_width=True)
