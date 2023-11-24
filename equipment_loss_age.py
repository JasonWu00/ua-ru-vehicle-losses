# import library
import pandas as pd
import streamlit as st
import altair as alt

# Load the CSV data
df = pd.read_csv("data/oryx/ru_losses.csv")
df2 = pd.read_csv("data/oryx/ua_losses.csv")

# Drop rows with null values
df = df.dropna()
df2 = df2.dropna()

# Combine the two DataFrames
combined_df = pd.concat([df.assign(dataset='ru'), df2.assign(dataset='ua')])

# Create a Streamlit Scatter Plot
st.title("Year First Produced vs Destroyed Date")

# Add a toggle button to show/hide 'ru' data for Scatter Plot
show_ru_scatter = st.checkbox('Show RU Data (Scatter)', value=True)

# Add a toggle button to show/hide 'ua' data for Scatter Plot
show_ua_scatter = st.checkbox('Show UA Data (Scatter)', value=True)

# Set the y-axis limits
y_min = 1940
y_max = 2030

# Filter the DataFrame based on user input for Scatter Plot
filtered_df_scatter = combined_df[((combined_df['dataset'] == 'ru') & show_ru_scatter) | ((combined_df['dataset'] == 'ua') & show_ua_scatter)]

scatter_chart = alt.Chart(filtered_df_scatter).mark_circle(size=60).encode(
    x='date_lost',
    y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max])),
    color=alt.Color('dataset:N', scale=alt.Scale(domain=['ru', 'ua'], range=['blue', 'red']))
).properties(width=600, height=400)

st.altair_chart(scatter_chart)

st.write("As time passes, both sides are using vehicles that are neither older nor newer.")

# Create a Streamlit Line Chart
st.title("Average Year First Produced vs Destroyed Date")

# Add a toggle button to show/hide 'ru' data for Line Chart
show_ru_line = st.checkbox('Show RU Data (Line)', value=True)

# Add a toggle button to show/hide 'ua' data for Line Chart
show_ua_line = st.checkbox('Show UA Data (Line)', value=True)

# Filter the DataFrame based on user input for Line Chart
filtered_df_line = combined_df[((combined_df['dataset'] == 'ru') & show_ru_line) | ((combined_df['dataset'] == 'ua') & show_ua_line)]

# Create a second chart to calculate the average "year_first_produced" for each "date_lost"
average_years = filtered_df_line.groupby(["dataset", "date_lost"])["year_first_produced"].mean().reset_index()
average_years_chart = alt.Chart(average_years).mark_line().encode(
    x='date_lost',
    y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max])),
    color=alt.Color('dataset:N', scale=alt.Scale(domain=['ru', 'ua'], range=['blue', 'red']))
).properties(width=600, height=400)

st.altair_chart(average_years_chart)

st.write("As time passes, both sides are using vehicles that are neither older nor newer.")
