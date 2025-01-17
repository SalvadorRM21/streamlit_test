import streamlit as st
from datetime import datetime
from api_connection import get_data_from_api
import matplotlib.pyplot as plt
import pandas as pd

# Function to fetch current temperature
def fetch_current_temperature(location="Barcelona"):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "9cd7ba775cmsha41eeb17ec7c48ap1a3d57jsnb01278a07b82",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": location}
    data = get_data_from_api(url, headers=headers, params=params)
    return data["current"]["temp_c"] if "current" in data else None

# Function to fetch hourly temperature for a specific date
def fetch_hourly_temperature(date, location="Barcelona"):
    url = "https://weatherapi-com.p.rapidapi.com/history.json"
    headers = {
        "X-RapidAPI-Key": "9cd7ba775cmsha41eeb17ec7c48ap1a3d57jsnb01278a07b82",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": location, "dt": date}
    data = get_data_from_api(url, headers=headers, params=params)
    if "forecast" in data and "forecastday" in data["forecast"]:
        hourly_data = data["forecast"]["forecastday"][0]["hour"]
        return [(hour["time"].split(" ")[1], hour["temp_c"]) for hour in hourly_data]  # Extract only the hour
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
    df_7 = pd.DataFrame(hourly_temp_7, columns=["Hour", "Temperature"])
    df_8 = pd.DataFrame(hourly_temp_8, columns=["Hour", "Temperature"])

    # Create two side-by-side columns for the plots
    col1, col2 = st.columns(2)

    with col1:
        st.header("7th December")
        fig_7, ax_7 = plt.subplots(figsize=(6, 3))  # Adjust height
        ax_7.plot(df_7["Hour"], df_7["Temperature"], label="7th December", color="blue")
        ax_7.set_xlabel("Hour")
        ax_7.set_ylabel("Temperature (°C)")
        ax_7.set_title("Hourly Temperatures")
        plt.xticks(rotation=45)
        st.pyplot(fig_7)

    with col2:
        st.header("8th December")
        fig_8, ax_8 = plt.subplots(figsize=(6, 3))  # Adjust height
        ax_8.plot(df_8["Hour"], df_8["Temperature"], label="8th December", color="orange")
        ax_8.set_xlabel("Hour")
        ax_8.set_ylabel("Temperature (°C)")
        ax_8.set_title("Hourly Temperatures")
        plt.xticks(rotation=45)
        st.pyplot(fig_8)

    # Display current temperature
    st.sidebar.header("Today's Info")
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")





