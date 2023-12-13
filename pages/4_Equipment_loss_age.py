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
st.title("Deep Soviet Stocks: Vehicle Losses by Age")

st.text('Author: Jin Lin')
# Toggle buttons for displaying Russian and Ukrainian histograms
show_ru_histogram = st.checkbox('Show Russian Histogram', value=True)
show_ua_histogram = st.checkbox('Show Ukrainian Histogram', value=True)

# Combine histograms using Plotly
fig_combined = go.Figure()

# Add Russian histogram if the button is checked
if show_ru_histogram:
    fig_combined.add_trace(go.Histogram(x=df_ru["year_first_produced"],
                                        nbinsx=50, name="Russia", marker={"color": "#FF4444"}))

# Add Ukrainian histogram if the button is checked
if show_ua_histogram:
    fig_combined.add_trace(go.Histogram(x=df_ua["year_first_produced"],
                                        nbinsx=50, name="Ukraine", marker={"color": "#4444FF"}))
    fig_combined.update_yaxes(
        range=(0, 360), # to really get across just how big the difference is
        constrain='domain' # also because people often times do not read y axis labels
    )

# Update layout for the combined chart
fig_combined.update_layout(
    title_text="Combined Histogram of Production Year",
    xaxis_title="Production Year",
    yaxis_title="Count",
    barmode="overlay",
)

# Show combined chart
st.plotly_chart(fig_combined)

st.markdown(
"""
Russia's lost vehicles fall in two distinct ranges: 1970-1990 and 2010-2017.

The first year range correspond to the peak of Soviet military power, which Russia \
inherited a large amount of after the collapse of the Soviet Union. 

The second year range corresponds to the construction of all of \
Russia's most advanced and rarest vehicles, such as the \
[T-90M](https://en.wikipedia.org/wiki/T-90) (first produced in 2016) and the \
[BMPT Terminator](https://en.wikipedia.org/wiki/BMPT_Terminator) (first produced in 2011).
"""
)

# below is the second chart

# reference: 
# https://www.nomidl.com/projects/russia-ukraine-war-data-analysis-project-using-python/

# Set Plotly template
pio.templates.default = 'plotly_dark'
color_theme = px.colors.qualitative.Antique

# Read data
df3 = pd.read_csv('data/russia_losses_equipment.csv')

# Drop unnecessary columns
df3.drop(columns=
         ['mobile SRBM system', 'military auto', 'fuel tank', 'vehicles and fuel tanks'],
         inplace=True)


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

st.markdown(
"""
At the beginning of the war, Russia suffered a significant loss of aircraft and \
helicopters (as seen in the initial spike in the loss line). \
However, the rate of Russian aircraft and helicopter losses slowed down. \
The drop in helicopter loss rates occurred at around the start of April 2022, \
when Russia abandoned its northern attack. The drop in aircraft loss rates occurred \
in May 2022, a month or so after that.

One possible explanation is that changing battlefield conditions no longer required \
the heavy frontline presence of these helicopters. Recall that during the early days of the war, \
such as during the \
[Hostomel Airport battle](https://en.wikipedia.org/wiki/Battle_of_Antonov_Airport), \
there was a heavy involvement (and thus loss) of helicopters. With that part of the war \
concluding, they are no longer flying out to their deaths.

Also take note of the slight uptick of aircraft losses during September 2022, which correlates \
with the occurrence of Ukraine's counteroffensive in the direction of Kharkiv.\

With the battle growing more static and both sides relying more on drones in their battles, \
the surge in drone losses over time makes more sense.
""")

