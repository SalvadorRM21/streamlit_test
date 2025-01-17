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

# Function to fetch electricity price for a specific range of dates
def fetch_electricity_price(start_date, end_date):
    url = "https://api.esios.ree.es/indicators/1001"
    headers = {
        "Authorization": "Token token=your_ree_api_token",
        "Accept": "application/json; application/vnd.esios-api-v1+json"
    }
    params = {"start_date": start_date, "end_date": end_date}
    try:
        data = get_data_from_api(url, headers=headers, params=params)
        if "indicator" in data and "values" in data["indicator"]:
            return [(entry["datetime"], entry["value"]) for entry in data["indicator"]["values"]]
    except Exception as e:
        if "403" in str(e):
            raise Exception("Access to the REE API is forbidden. Check your token or permissions.")
        else:
            raise e
    return []

# Streamlit app
st.set_page_config(layout="wide")
st.title("Heater Dashboard")

try:
    # Fetch current temperature
    temperature = fetch_current_temperature()

    # Fetch electricity prices for specific dates
    electricity_prices = fetch_electricity_price("2022-12-07T00:00:00", "2022-12-09T23:59:59")
    today = datetime.now().strftime('%Y-%m-%dT00:00:00')
    today_price = fetch_electricity_price(today, today)

    # Sidebar with today's info
    with st.sidebar:
        st.header("Today's Info")
        st.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
        if today_price:
            st.metric(label="Electricity Price (€/MWh)", value=f"{today_price[0][1]} €/MWh")

    # Display historical prices
    st.header("Electricity Prices (7-8 December 2022)")
    if electricity_prices:
        for date, price in electricity_prices:
            st.write(f"{date}: {price} €/MWh")
    else:
        st.write("No data available for the selected dates.")

except Exception as e:
    st.error(f"Error fetching data: {e}")




