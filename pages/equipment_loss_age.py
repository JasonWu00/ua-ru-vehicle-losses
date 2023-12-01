"""
Author: Jin Lin
Ported to Streamlit by Ze Hong Wu.
"""

# import library
import pandas as pd
import streamlit as st
import altair as alt
from sklearn.linear_model import LinearRegression

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

st.write("There are rumors that the reason why the war between Russia and Ukraine is prolonged is because Russia does not take the war seriously. They are using older and older vehicles.")



# Below is the Second Chart

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

st.write("This chart displays the average age of vehicles that were destroyed on a specified date. However, it is not very clear whether each side is using newer or older vehicles.")




# Below is the Third Chart

# Create a Streamlit Line Chart
st.title("Regression Lines for Age of Vehicles That Were Destroyed")

combined_df['date_lost'] = pd.to_datetime(combined_df['date_lost']).dt.year

# Add a toggle button to show/hide 'ru' data for Line Chart
show_ru_reg_line = st.checkbox('Show RU Data (Reg_Line)', value=True)

# Add a toggle button to show/hide 'ua' data for Line Chart
show_ua_reg_line = st.checkbox('Show UA Data (Reg_Line)', value=True)

# Filter the DataFrame based on user input for Line Chart
filtered_df_ru = combined_df[(combined_df['dataset'] == 'ru') & show_ru_reg_line]
filtered_df_ua = combined_df[(combined_df['dataset'] == 'ua') & show_ua_reg_line]

# Check if either dataset is selected
if not filtered_df_ru.empty or not filtered_df_ua.empty:
    # Create a Linear Regression model for RU data if 'ru' data is selected
    if not filtered_df_ru.empty:
        regression_model_ru = LinearRegression()
        regression_model_ru.fit(filtered_df_ru[['date_lost']], filtered_df_ru['year_first_produced'])
        line_of_best_fit_ru = pd.DataFrame({
            'date_lost': filtered_df_ru['date_lost'],
            'year_first_produced': regression_model_ru.predict(filtered_df_ru[['date_lost']])
        })
        chart_ru = alt.Chart(line_of_best_fit_ru).mark_line(color='red').encode(
            x='date_lost',
            y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max]))
        )
    else:
        chart_ru = alt.Chart().mark_point()

    # Create a Linear Regression model for UA data if 'ua' data is selected
    if not filtered_df_ua.empty:
        regression_model_ua = LinearRegression()
        regression_model_ua.fit(filtered_df_ua[['date_lost']], filtered_df_ua['year_first_produced'])
        line_of_best_fit_ua = pd.DataFrame({
            'date_lost': filtered_df_ua['date_lost'],
            'year_first_produced': regression_model_ua.predict(filtered_df_ua[['date_lost']])
        })
        chart_ua = alt.Chart(line_of_best_fit_ua).mark_line(color='blue').encode(
            x='date_lost',
            y=alt.Y('year_first_produced', scale=alt.Scale(domain=[y_min, y_max]))
        )
    else:
        chart_ua = alt.Chart().mark_point()

    # Combine both charts
    line_chart = chart_ru + chart_ua

    st.altair_chart(line_chart)
else:
    st.warning("Please select at least one dataset to display.")    
    
st.write("As time passes, Ukraine tends to deploy newer vehicles, reflecting potential efforts to modernize its military capabilities. In contrast, Russia appears to rely on a mix of older and not necessarily newer equipment. The age and condition of lost equipment vary by type on both sides. This disparity might suggest that Ukraine is actively investing in modernization and maintaining a higher readiness level, while Russia is not inclined to escalate the conflict into a larger war.")