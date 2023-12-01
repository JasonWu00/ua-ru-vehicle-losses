import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('data/russia_losses_equipment.csv')

# Create a Streamlit app
st.title('Russia Losses of Equipment')

# Create a line chart for aircraft losses
st.subheader('Aircraft Losses Over Time')
fig, ax = plt.subplots()
ax.plot(data['date'], data['aircraft'], label='Aircraft', marker='o')
ax.set_xlabel('Date')
ax.set_ylabel('Aircraft Losses')
ax.legend()
st.pyplot(fig)




# You can add more charts for other categories as needed

