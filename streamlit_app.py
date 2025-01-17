import streamlit as st
from datetime import datetime
from api_connection import get_data_from_api
import matplotlib.pyplot as plt
import pandas as pd

# Function to fetch current temperature
def fetch_current_temperature(location="Barcelona"):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "6a425b2a7bmshc1f059e65b98fb7p1cdd78jsn184965114ca2",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": location}
    data = get_data_from_api(url, headers=headers, params=params)
    return data["current"]["temp_c"] if "current" in data else None

# Function to fetch hourly temperature for a specific date
def fetch_hourly_temperature(date, location="Barcelona"):
    url = "https://weatherapi-com.p.rapidapi.com/history.json"
    headers = {
        "X-RapidAPI-Key": "6a425b2a7bmshc1f059e65b98fb7p1cdd78jsn184965114ca2",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": location, "dt": date}
    data = get_data_from_api(url, headers=headers, params=params)
    if "forecast" in data and "forecastday" in data["forecast"]:
        hourly_data = data["forecast"]["forecastday"][0]["hour"]
        return [(hour["time"], hour["temp_c"]) for hour in hourly_data]
    return []

# Streamlit app
st.set_page_config(layout="wide")
st.title("Heater Dashboard")

try:
    # Fetch current temperature
    temperature = fetch_current_temperature()

    # Fetch hourly temperatures for 7th and 8th December
    hourly_temp_7 = fetch_hourly_temperature("2022-12-07")
    hourly_temp_8 = fetch_hourly_temperature("2022-12-08")

    # Prepare data for plotting
    df_7 = pd.DataFrame(hourly_temp_7, columns=["Time", "Temperature"])
    df_8 = pd.DataFrame(hourly_temp_8, columns=["Time", "Temperature"])

    # Plot temperatures
    st.header("Hourly Temperatures for 7th and 8th December")
    fig, ax = plt.subplots()
    ax.plot(df_7["Time"], df_7["Temperature"], label="7th December")
    ax.plot(df_8["Time"], df_8["Temperature"], label="8th December")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Hourly Temperatures")
    ax.legend()
    plt.xticks(rotation=45)

    # Display plot in Streamlit
    st.pyplot(fig)

    # Display current temperature
    st.sidebar.header("Today's Info")
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")





