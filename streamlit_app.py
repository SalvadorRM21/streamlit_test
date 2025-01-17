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

# Function to fetch hourly temperature from AEMET OpenData
def fetch_hourly_temperature(date, station_id="0076"):
    url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{date}T00:00:00UTC/fechafin/{date}T23:59:59UTC/estacion/{station_id}"
    headers = {
        "Accept": "application/json",
        "api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYWx2YWRvcnJtMjEwN0BnbWFpbC5jb20iLCJqdGkiOiI3ZmZkNDMzZC1iMzM3LTQ1YjktOGNiMy0yNjZjMWM1ZTY1MmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTczNzEzOTgxOCwidXNlcklkIjoiN2ZmZDQzM2QtYjMzNy00NWI5LThjYjMtMjY2YzFjNWU2NTJiIiwicm9sZSI6IiJ9.xzboGn3oPvjyr6tHmbm4LuVg3F7Baxo2lrfo-WssZTo"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if "datos" in data:
        datos_response = requests.get(data["datos"])
        datos_response.raise_for_status()
        hourly_data = datos_response.json()
        return [(obs["hora"], obs["tmed"]) for obs in hourly_data if "hora" in obs and "tmed" in obs]
    return []

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


# Plot temperature, state, and current
def plot_temp_state_current(df, title):
    fig, ax1 = plt.subplots(figsize=(6, 3))

    ax1.set_title(title)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (°C)", color="blue")
    ax1.plot(df["Time"], df["Temperature"], color="blue", label="Temperature")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("State / Current", color="green")
    ax2.plot(df["Time"], df["State"], color="green", linestyle="--", label="State")
    ax2.plot(df["Time"], df["Current"], color="orange", label="Current")
    ax2.tick_params(axis="y", labelcolor="green")

    fig.tight_layout()
    return fig

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

   

    


    

    # Display current temperature, today's electricity price, and time
    st.sidebar.header("Today's Info")
    st.sidebar.markdown("*Barcelona, Spain*", unsafe_allow_html=True)
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
    st.sidebar.metric(label="Today's Electricity Price (€/kWh)", value=f"{today_price} €")
    st.sidebar.metric(label="Time", value=today_time)

except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")






