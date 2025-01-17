import streamlit as st
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Streamlit app configuration
st.set_page_config(layout="wide", page_title="ThermoScope")

# Add custom styles for background
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #FF4500, #1E90FF);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Static data for 7th and 8th December 2024
data = {
    "2024-12-07": [
        ("0:00", 13.44), ("1:00", 12.97), ("2:00", 12.75), ("4:00", 12.75),
        ("5:00", 12.74), ("6:00", 13.23), ("7:00", 13.56), ("8:00", 13.6),
        ("9:00", 13.85), ("10:00", 14.66), ("11:00", 15.32), ("12:00", 16.68),
        ("13:00", 17.46), ("14:00", 18.09), ("15:00", 19.19), ("16:00", 18.04),
        ("17:00", 16.52), ("18:00", 14.74), ("19:00", 13.3), ("20:00", 12.19),
        ("21:00", 11.34), ("22:00", 10.45), ("23:00", 9.85)
    ],
    "2024-12-08": [
        ("0:00", 9.24), ("1:00", 8.84), ("2:00", 8.37), ("3:00", 8.13),
        ("4:00", 8.22), ("5:00", 7.86), ("6:00", 7.46), ("7:00", 7.45),
        ("8:00", 7.66), ("9:00", 8.21), ("10:00", 9.24), ("11:00", 10.6),
        ("12:00", 11.52), ("13:00", 12.33), ("14:00", 12.79), ("15:00", 12.63),
        ("16:00", 12.4), ("17:00", 11.74), ("18:00", 11), ("19:00", 10.5),
        ("20:00", 10.1), ("21:00", 9.27), ("22:00", 8.66), ("23:00", 8.37)
    ]
}

# Load data from Excel
file_path = '/mnt/data/DATA FOR MANUAL OPERATION HEATER.xlsx'
data_excel = pd.read_excel(file_path)

# Title
st.title("ThermoScope")

# Fetch electricity prices (placeholder function)
def fetch_electricity_price(date):
    return 0.15  # Placeholder value

# Fetch prices
price_7 = fetch_electricity_price("2024-12-07")
price_8 = fetch_electricity_price("2024-12-08")

today_date = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
today_price = fetch_electricity_price(today_date)

df_7 = pd.DataFrame(data["2024-12-07"], columns=["Hour", "Temperature"])
df_8 = pd.DataFrame(data["2024-12-08"], columns=["Hour", "Temperature"])

# Create two columns for December 7th and 8th
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.header("7th December 2024")
    fig, ax = plt.subplots()
    ax.plot(df_7["Hour"], df_7["Temperature"], label="Temperature", color="blue")
    ax.set_title("Hourly Temperature")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.metric("Electricity Price (€/kWh)", f"{price_7} €")

with graph_col2:
    st.header("8th December 2024")
    fig, ax = plt.subplots()
    ax.plot(df_8["Hour"], df_8["Temperature"], label="Temperature", color="orange")
    ax.set_title("Hourly Temperature")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.metric("Electricity Price (€/kWh)", f"{price_8} €")

# Add combined Excel data graph
st.header("Manual Heater Operation Data")
fig, ax = plt.subplots()

# Plot Temperature
ax.plot(data_excel['Time'], data_excel['Temperature'], label="Temperature (°C)", color="red")

# Plot Current
ax.plot(data_excel['Time'], data_excel['Current'], label="Current (A)", color="green")

# Plot Heater State
heater_state = data_excel['Heater state'].apply(lambda x: 1 if x == 'ON' else 0)
ax.step(data_excel['Time'], heater_state, label="Heater State (ON/OFF)", color="blue", where='post')

# Add labels and legend
ax.set_title("Heater Operation")
ax.set_xlabel("Time")
ax.set_ylabel("Values")
plt.xticks(rotation=45)
ax.legend()

st.pyplot(fig)


