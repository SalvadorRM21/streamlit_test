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

# Function to fetch current temperature
def fetch_current_temperature(location="Barcelona"):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "9cd7ba775cmsha41eeb17ec7c48ap1a3d57jsnb01278a07b82", 
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": location}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["current"]["temp_c"] if "current" in data else None

# Function to fetch hourly temperature (using provided static data for 7th and 8th December 2024)
def fetch_hourly_temperature(date, station_id="0076"):
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
    # Return the data for the specified date
    return data.get(date, [])


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

st.title("ThermoScope")

try:
    # Fetch current temperature
    temperature = fetch_current_temperature()

    # Fetch hourly temperatures for 7th and 8th December
    hourly_temp_7 = fetch_hourly_temperature("2024-12-07")
    hourly_temp_8 = fetch_hourly_temperature("2024-12-08")

    # Fetch electricity prices for 7th, 8th December, and today
    price_7 = fetch_electricity_price("2024-12-07")
    price_8 = fetch_electricity_price("2024-12-08")
    today_date = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
    today_price = fetch_electricity_price(today_date)
    today_time = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%H:%M")

    # Prepare data for plotting
    df_7 = pd.DataFrame(hourly_temp_7, columns=["Hour", "Temperature"])
    df_8 = pd.DataFrame(hourly_temp_8, columns=["Hour", "Temperature"])

    # Create two side-by-side columns for the temperature plots
    col1, col2 = st.columns(2)

    with col1:
        st.header("7th December 2024")
        fig_7, ax_7 = plt.subplots(figsize=(6, 3))  # Adjust height
        fig_7.patch.set_facecolor('none')  # Transparent background for the figure
        ax_7.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
        ax_7.plot(df_7["Hour"], df_7["Temperature"], label="7th December", color="blue")
        ax_7.set_xlabel("Hour")
        ax_7.set_ylabel("Temperature (°C")
        ax_7.set_title("Hourly Temperatures")
        plt.xticks(rotation=45)
        st.pyplot(fig_7)
        st.metric(label="Electricity Price (€/kWh)", value=f"{price_7} €")

    with col2:
        st.header("8th December 2024")
        fig_8, ax_8 = plt.subplots(figsize=(6, 3))  # Adjust height
        fig_8.patch.set_facecolor('none')  # Transparent background for the figure
        ax_8.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
        ax_8.plot(df_8["Hour"], df_8["Temperature"], label="8th December", color="orange")
        ax_8.set_xlabel("Hour")
        ax_8.set_ylabel("Temperature (°C")
        ax_8.set_title("Hourly Temperatures")
        plt.xticks(rotation=45)
        st.pyplot(fig_8)
        st.metric(label="Electricity Price (€/kWh)", value=f"{price_8} €")

    # Display current temperature, today's electricity price, and time
    st.sidebar.header("Today's Info")
    st.sidebar.markdown("*Barcelona, Spain*", unsafe_allow_html=True)
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
    st.sidebar.metric(label="Today's Electricity Price (€/kWh)", value=f"{today_price} €")
    st.sidebar.metric(label="Time", value=today_time)

except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")

# Load the cleaned datasets
file_manual = "/mnt/data/Befre algrtihme - Manual regulation.xlsx"
file_auto = "/mnt/data/test with automatic heater regulation.xlsx"
data_manual = pd.read_excel(file_manual)
data_auto = pd.read_excel(file_auto)

# Cleaning the manual regulation data
data_manual_cleaned = data_manual[["Day", "Time", "Temperature of the room", "Current", "HEATER STATE"]]
data_manual_cleaned["Time"] = pd.to_datetime(data_manual_cleaned["Time"], format="%H:%M:%S").dt.time

# Cleaning the automatic regulation data
data_auto_cleaned = data_auto[["Day", "Time (min:sec)", "Temperature of the room", "Current", "Heater State"]]
data_auto_cleaned.rename(columns={"Time (min:sec)": "Time"}, inplace=True)
data_auto_cleaned["Time"] = pd.to_datetime(data_auto_cleaned["Time"], errors="coerce", format="%H:%M:%S").dt.time
data_auto_cleaned["Time"].fillna(method="ffill", inplace=True)

# Streamlit layout
st.header("Comparison of Heater Regulation Modes")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Manual Heater Regulation")
    fig_manual, ax_manual = plt.subplots(figsize=(6, 3))
    ax_manual.plot(data_manual_cleaned["Time"], data_manual_cleaned["Temperature of the room"], label="Temperature", color="blue")
    ax_manual.plot(data_manual_cleaned["Time"], data_manual_cleaned["Current"], label="Current", color="orange")
    ax_manual.set_xlabel("Time")
    ax_manual.set_ylabel("Temperature (°C) / Current (A)")
    ax_manual.set_title("Manual Heater Regulation")
    ax_manual.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig_manual)

with col4:
    st.subheader("Automatic Heater Regulation")
    fig_auto, ax_auto = plt.subplots(figsize=(6, 3))
    ax_auto.plot(data_auto_cleaned["Time"], data_auto_cleaned["Temperature of the room"], label="Temperature", color="blue")
    ax_auto.plot(data_auto_cleaned["Time"], data_auto_cleaned["Current"], label="Current", color="orange")
    ax_auto.set_xlabel("Time")
    ax_auto.set_ylabel("Temperature (°C) / Current (A)")
    ax_auto.set_title("Automatic Heater Regulation")
    ax_auto.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig_auto)








