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

# Function to fetch today's electricity price
def fetch_todays_electricity_price():
    today = datetime.now().strftime('%Y-%m-%dT00:00:00')
    url = "https://api.esios.ree.es/indicators/1001"
    headers = {
        "Authorization": "Token token=your_ree_api_token",
        "Accept": "application/json; application/vnd.esios-api-v1+json"
    }
    params = {"start_date": today, "end_date": today}
    data = get_data_from_api(url, headers=headers, params=params)
    if "indicator" in data and "values" in data["indicator"]:
        return data["indicator"]["values"][0]["value"]
    return None

# Streamlit app
st.set_page_config(layout="wide")
st.title("Heater Dashboard")

# Fetch and display current temperature and electricity price
try:
    temperature = fetch_current_temperature()
    electricity_price = fetch_todays_electricity_price()

    with st.sidebar:
        st.header("Today's Info")
        st.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
        st.metric(label="Electricity Price (€/MWh)", value=f"{electricity_price} €/MWh" if electricity_price else "N/A")
except Exception as e:
    st.error(f"Error fetching data: {e}")




