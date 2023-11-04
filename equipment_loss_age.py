# Step 1: import library
import pandas as pd
import streamlit as st
import altair as alt

# Step 2: Load the CSV data
df = pd.read_csv("data/oryx/ru_losses.csv")

# Step 3: Drop rows with null values
df = df.dropna()

# Step 6: Create a Streamlit Scatter Plot
st.title("Year First Produced vs Destroyed Date")
st.write("Scatter plot to compare 'year_first_produced' and 'date_lost")

# Set the y-axis limits
y_min = 1930
y_max = 2030

scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
    x='date_lost',
    y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max]))
).properties(width=600, height=400)

st.altair_chart(scatter_chart)

# Step 7: Create a second chart to calculate the average "year_first_produced" for each "date_lost"
average_years = df.groupby("date_lost")["year_first_produced"].mean().reset_index()
average_years_chart = alt.Chart(average_years).mark_line().encode(
    x='date_lost',
    y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max]))
).properties(width=600, height=400)

st.title("Average Year First Produced vs Destroyed Date")
st.write("Line chart to show the average 'year_first_produced' for each 'date_lost'")
st.altair_chart(average_years_chart)
