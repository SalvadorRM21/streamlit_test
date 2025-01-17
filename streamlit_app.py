import streamlit as st
from datetime import datetime, timedelta, timezone
import pytz
import matplotlib.pyplot as plt
import pandas as pd
import requests


# Add custom styles for background
# Add custom styles for background and overall design
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #FF4500, #1E90FF); /* Sunset gradient */
        color: white; /* Ensure text is visible */
    }
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.5); /* Transparent sidebar for better contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered title
st.markdown(
    """
    <h1 style="text-align: center; color: white;">ThermoScope</h1>
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



# Fetch electricity prices for 7th, 8th December, and today
price_7 = fetch_electricity_price("2024-12-07")
price_8 = fetch_electricity_price("2024-12-08")
today_date = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
today_price = fetch_electricity_price(today_date)
today_time = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%H:%M")

# Prepare data for plotting
hourly_temp_7 = data["2024-12-07"]
hourly_temp_8 = data["2024-12-08"]
df_7 = pd.DataFrame(hourly_temp_7, columns=["Hour", "Temperature"])
df_8 = pd.DataFrame(hourly_temp_8, columns=["Hour", "Temperature"])

# Create two side-by-side columns for the temperature plots
col1, col2 = st.columns(2)

with col1:
    st.header("December 7th 2024")
    fig_7, ax_7 = plt.subplots(figsize=(6, 3))  # Adjust height
    fig_7.patch.set_facecolor('none')  # Transparent background for the figure
    ax_7.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
    ax_7.plot(df_7["Hour"], df_7["Temperature"], label="7th December", color="blue")
    ax_7.set_xlabel("Hour")
    ax_7.set_ylabel("Temperature (°C)")
    ax_7.set_title("Outside Temperature")
    plt.xticks(rotation=45)
    st.pyplot(fig_7)
    st.metric(label="Electricity Price (€/kWh) for December 7th 2024", value=f"{price_7} €")

with col2:
    st.header("December 8th 2024")
    fig_8, ax_8 = plt.subplots(figsize=(6, 3))  # Adjust height
    fig_8.patch.set_facecolor('none')  # Transparent background for the figure
    ax_8.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
    ax_8.plot(df_8["Hour"], df_8["Temperature"], label="8th December", color="orange")
    ax_8.set_xlabel("Hour")
    ax_8.set_ylabel("Temperature (°C)")
    ax_8.set_title("Outside Temperature")
    plt.xticks(rotation=45)
    st.pyplot(fig_8)
    st.metric(label="Electricity Price (€/kWh) for December 8th 2024", value=f"{price_8} €")

# Display current temperature, today's electricity price, and time
st.sidebar.image("Logo.png", width=75)  # Add your logo here
st.sidebar.header("Today's Info")
st.sidebar.markdown("*Barcelona, Spain*", unsafe_allow_html=True)
st.sidebar.metric(label="Temperature (°C)", value="N/A")  # Replace with real temperature if available
st.sidebar.metric(label="Today's Electricity Price (€/kWh)", value=f"{today_price} €")
st.sidebar.metric(label="Time", value=today_time)

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Static data for plotting
data = {
    "2024-12-09": [
        ("18:00", 17.2, 5.5), ("18:00:45", 17.6, 5.5), ("18:01:30", 18.1, 5.5), ("18:02:15", 18.5, 5.5),
        ("18:03:00", 18.9, 5.5), ("18:03:45", 19.3, 0), ("18:04:30", 19.5, 0), ("18:05:15", 19.4, 0),
        ("18:06:00", 19.2, 0), ("18:06:45", 18.9, 0), ("18:07:30", 18.5, 5.5), ("18:08:15", 18.9, 5.5),
        ("18:09:00", 19.3, 5.5), ("18:09:45", 19.5, 0), ("18:10:30", 19.6, 0), ("18:11:15", 19.4, 0),
        ("18:12:00", 19.1, 0), ("18:12:45", 18.8, 0), ("18:13:30", 18.5, 5.5), ("18:14:15", 18.9, 5.5),
        ("18:15:00", 19.3, 5.5), ("18:15:45", 19.5, 0), ("18:16:30", 19.4, 0), ("18:17:15", 19.2, 0),
        ("18:18:00", 18.9, 0), ("18:18:45", 18.5, 5.5), ("18:19:30", 18.9, 5.5), ("18:20:15", 19.3, 5.5),
        ("18:21:00", 19.5, 0)
    ],
    "2024-12-10": [
        ("18:00", 18.0, 5.5), ("18:00:45", 18.4, 5.5), ("18:01:30", 18.8, 5.5), ("18:02:15", 19.2, 5.5),
        ("18:03:00", 19.5, 0), ("18:03:45", 19.6, 0), ("18:04:30", 19.3, 0), ("18:05:15", 19.0, 0),
        ("18:06:00", 18.7, 0), ("18:06:45", 18.5, 5.5), ("18:07:30", 18.9, 5.5), ("18:08:15", 19.4, 5.5),
        ("18:09:00", 19.5, 0), ("18:09:45", 19.3, 0), ("18:10:30", 19.0, 0), ("18:11:15", 18.7, 0),
        ("18:12:00", 18.5, 5.5), ("18:12:45", 18.9, 5.5), ("18:13:30", 19.3, 5.5), ("18:14:15", 19.5, 0),
        ("18:15:00", 19.4, 0), ("18:15:45", 19.2, 0), ("18:16:30", 18.9, 0), ("18:17:15", 18.5, 5.5),
        ("18:18:00", 18.9, 5.5), ("18:18:45", 19.3, 5.5), ("18:19:30", 19.5, 0), ("18:20:15", 19.4, 0),
        ("18:21:00", 19.2, 0)
    ]
}

# Prepare data for plotting
hourly_temp_9 = data["2024-12-09"]
hourly_temp_10 = data["2024-12-10"]

df_9 = pd.DataFrame(hourly_temp_9, columns=["Hour", "Temperature", "Current"])
df_10 = pd.DataFrame(hourly_temp_10, columns=["Hour", "Temperature", "Current"])

# Create two side-by-side columns for the temperature and current plots
col1, col2 = st.columns(2)

with col1:
    st.header("December 9th 2024 - Turning ON/OFF remotely")
    fig_9, ax_9 = plt.subplots(figsize=(6, 3))  # Adjust height
    fig_9.patch.set_facecolor('none')  # Transparent background for the figure
    ax_9.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
    ax_9.plot(df_9["Hour"], df_9["Temperature"], label="Temperature", color="blue")
    ax_9.set_xlabel("Hour")
    ax_9.set_ylabel("Temperature (°C)", color="blue")
    ax_9.tick_params(axis='y', labelcolor="blue")

    # Add current to the same plot with a secondary axis
    ax9_current = ax_9.twinx()
    ax9_current.plot(df_9["Hour"], df_9["Current"], label="Current", color="orange")
    ax9_current.set_ylabel("Current (A)", color="orange")
    ax9_current.tick_params(axis='y', labelcolor="orange")

    ax_9.set_title("Room Temperature and Current")
    ax_9.set_xticks(range(0, len(df_9["Hour"]), 2))  # Add spacing to the x-axis ticks
    ax_9.set_xticklabels(df_9["Hour"].iloc[::2], rotation=45)  # Better x-axis labels
    st.pyplot(fig_9)

with col2:
    st.header("December 10th 2024 - Turning ON/OFF remotely")
    fig_10, ax_10 = plt.subplots(figsize=(6, 3))  # Adjust height
    fig_10.patch.set_facecolor('none')  # Transparent background for the figure
    ax_10.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
    ax_10.plot(df_10["Hour"], df_10["Temperature"], label="Temperature", color="blue")
    ax_10.set_xlabel("Hour")
    ax_10.set_ylabel("Temperature (°C)", color="blue")
    ax_10.tick_params(axis='y', labelcolor="blue")

    # Add current to the same plot with a secondary axis
    ax10_current = ax_10.twinx()
    ax10_current.plot(df_10["Hour"], df_10["Current"], label="Current", color="orange")
    ax10_current.set_ylabel("Current (A)", color="orange")
    ax10_current.tick_params(axis='y', labelcolor="orange")

    ax_10.set_title("Room Temperature and Current")
    ax_10.set_xticks(range(0, len(df_10["Hour"]), 2))  # Add spacing to the x-axis ticks
    ax_10.set_xticklabels(df_10["Hour"].iloc[::2], rotation=45)  # Better x-axis labels
    st.pyplot(fig_10)




