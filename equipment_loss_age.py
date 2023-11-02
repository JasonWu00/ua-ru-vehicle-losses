# Step 1: import library
import pandas as pd
import streamlit as st

# Step 2: Load the CSV data
data = pd.read_csv("data/oryx/ru_losses.csv")

# Step 3: Create the "destroyed_date" column
def combine_date(row):
    try:
        day = int(row['day'])
        month = int(row['month'])
        year = int(row['year'])
        return pd.to_datetime(f'{day}/{month}/{year}', format='%d/%m/%y')
    except (ValueError, TypeError):
        return pd.NaT  # Set to NaN for non-finite or missing values

# Step 4 Apply the custom function to create the "Date" column
data["destroyed_date"] = data.apply(combine_date, axis=1)
data["destroyed_date"] = data["destroyed_date"].dt.strftime('%Y-%m-%d')
# Step 5: Filter out rows with null values in "destroyed_date"
data = data.dropna(subset=["destroyed_date"])

# Step 6: Create a Streamlit Scatter Plot
st.title("Year First Produced vs Destroyed Date")
st.write("Scatter plot to compare 'year_first_produced' and 'destroyed_date'")

st.write(data[['year_first_produced', 'destroyed_date']])
st.scatter_chart(data=data, x="destroyed_date", y="year_first_produced")

# Step 7: Create a second chart to calculate the average "year_first_produced" for each "destroyed_date"
average_years = data.groupby("destroyed_date")["year_first_produced"].mean()
st.title("Average Year First Produced vs Destroyed Date")
st.write("Line chart to show the average 'year_first_produced' for each 'destroyed_date'")

st.line_chart(average_years)