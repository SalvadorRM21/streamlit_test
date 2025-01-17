import streamlit as st
from datetime import datetime, timedelta, timezone
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

# Hardcoded data from the user
heater_data = {
    "Time": [
        "6:25:00", "6:25:45", "6:26:30", "6:27:15", "6:28:00", "6:28:45", "6:29:30", "6:30:15",
        "6:31:00", "6:31:45", "6:32:30", "6:33:15", "6:34:00", "6:34:45", "6:35:30", "6:36:15",
        "6:37:00", "6:37:45", "6:38:30", "6:39:15", "6:40:00", "6:40:45", "6:41:30", "6:42:15",
        "6:43:00", "6:43:45", "6:44:30", "6:45:15", "6:46:00", "6:46:45", "6:47:30", "6:48:15",
        "6:49:00", "6:49:45", "6:50:30", "6:51:15", "6:52:00", "6:52:45", "6:53:30", "6:54:15"
    ],
    "Temperature": [
        17.00, 17.16, 16.59, 17.08, 17.16, 17.08, 17.16, 16.91, 17.48, 18.20, 17.88,
        17.64, 17.56, 17.96, 18.20, 18.04, 18.04, 18.20, 17.96, 17.96, 18.45, 18.45,
        18.45, 18.45, 19.01, 18.69, 19.25, 19.33, 19.49, 19.17, 19.81, 19.33, 19.41,
        19.73, 19.65, 19.65, 19.65, 19.57, 20.22, 19.81
    ],
    "Current": [
        0.00, 0.00, 0.00, 5.58, 5.53, 5.50, 5.54, 5.49, 5.49, 5.46, 5.45, 5.46, 5.45,
        5.46, 5.44, 5.43, 5.41, 5.43, 5.42, 5.41, 5.40, 5.40, 5.40, 5.39, 5.38, 5.38,
        5.37, 5.37, 5.38, 5.38, 5.36, 5.37, 5.37, 5.37, 5.37, 5.36, 5.36, 5.35, 5.36
    ],
    "Heater State": [
        "OFF", "OFF", "OFF", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON",
        "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON",
        "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON", "ON"
    ]
}

# Function to fetch electricity price for a specific date from REE API
def fetch_electricity_price(date):
    endpoint = 'https://apidatos.ree.es'
    get_archives = '/en/datos/mercados/precios-mercados-tiempo-real'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Host': 'apidatos.ree.es'
    }
    params = {
        'start_date': f'{date}T00:00',
        'end_date': f'{date}T23:59',
        'time_trunc': 'hour'
    }
    response = requests.get(endpoint + get_archives, headers=headers, params=params)
    response.raise_for_status()
    data_json = response.json()
    if "included" in data_json:
        pvpc = data_json["included"][0]["attributes"]["values"][0]["value"] / 1000  # Convert €/MWh to €/kWh
        return round(pvpc, 4)
    return "N/A"

# Title
st.title("ThermoScope")

# Plot Heater Operation Data
st.header("Manual Heater Operation Data")
fig, ax = plt.subplots()

# Plot Temperature
ax.plot(heater_data["Time"], heater_data["Temperature"], label="Temperature (°C)", color="red")

# Plot Current
ax.plot(heater_data["Time"], heater_data["Current"], label="Current (A)", color="green")

# Plot Heater State
heater_state = [1 if state == "ON" else 0 for state in heater_data["Heater State"]]
ax.step(heater_data["Time"], heater_state, label="Heater State (ON/OFF)", color="blue", where='post')

# Add labels and legend
ax.set_title("Heater Operation")
ax.set_xlabel("Time")
ax.set_ylabel("Values")
plt.xticks(rotation=45)
ax.legend()

st.pyplot(fig)

# Fetch electricity prices for 7th, 8th December, and today
price_7 = fetch_electricity_price("2024-12-07")
price_8 = fetch_electricity_price("2024-12-08")
today_date = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
today_price = fetch_electricity_price(today_date)

# Plot data for December 7th
st.header("7th December 2024")
df_7 = pd.DataFrame(data["2024-12-07"], columns=["Hour", "Temperature"])
fig_7, ax_7 = plt.subplots()
ax_7.plot(df_7["Hour"], df_7["Temperature"], label="Temperature", color="orange")
ax_7.set_title("Hourly Temperature on 7th December 2024")
ax_7.set_xlabel("Hour")
ax_7.set_ylabel("Temperature (°C)")
plt.xticks(rotation=45)
ax_7.legend()
st.pyplot(fig_7)

# Plot data for December 8th
st.header("8th December 2024")
df_8 = pd.DataFrame(data["2024-12-08"], columns=["Hour", "Temperature"])
fig_8, ax_8 = plt.subplots()
ax_8.plot(df_8["Hour"], df_8["Temperature"], label="Temperature", color="purple")
ax_8.set_title("Hourly Temperature on 8th December 2024")
ax_8.set_xlabel("Hour")
ax_8.set_ylabel("Temperature (°C)")
plt.xticks(rotation=45)
ax_8.legend()
st.pyplot(fig_8)

# Display current temperature, today's electricity price, and time
st.sidebar.header("Today's Info")
st.sidebar.markdown("*Barcelona, Spain*", unsafe_allow_html=True)
st.sidebar.metric(label="Temperature (°C)", value="N/A")  # Replace with real temperature if available
st.sidebar.metric(label="Today's Electricity Price (€/kWh)", value=f"{today_price} €")



