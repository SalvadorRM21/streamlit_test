import streamlit as st
from datetime import datetime
from api_connection import get_data_from_api

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

# Streamlit app
st.set_page_config(layout="wide")
st.title("Heater Dashboard")

try:
    # Fetch data
    temperature = fetch_current_temperature()

    # Display data
    st.sidebar.header("Today's Info")
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")




