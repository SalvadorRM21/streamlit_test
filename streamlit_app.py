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
    url = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    headers = {
        "api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYWx2YWRvcnJtMjEwN0BnbWFpbC5jb20iLCJqdGkiOiI3ZmZkNDMzZC1iMzM3LTQ1YjktOGNiMy0yNjZjMWM1ZTY1MmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTczNzEzOTgxOCwidXNlcklkIjoiN2ZmZDQzM2QtYjMzNy00NWI5LThjYjMtMjY2YzFjNWU2NTJiIiwicm9sZSI6IiJ9.xzboGn3oPvjyr6tHmbm4LuVg3F7Baxo2lrfo-WssZTo"
    }
    params = {"q": location}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["current"]["temp_c"] if "current" in data else None

# Function to fetch hourly temperature for a specific date from AEMET API
def fetch_hourly_temperature_aemet(date, location="Barcelona"):
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYWx2YWRvcnJtMjEwN0BnbWFpbC5jb20iLCJqdGkiOiI3ZmZkNDMzZC1iMzM3LTQ1YjktOGNiMy0yNjZjMWM1ZTY1MmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTczNzEzOTgxOCwidXNlcklkIjoiN2ZmZDQzM2QtYjMzNy00NWI5LThjYjMtMjY2YzFjNWU2NTJiIiwicm9sZSI6IiJ9.xzboGn3oPvjyr6tHmbm4LuVg3F7Baxo2lrfo-WssZTo"
    base_url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/"
    location_code = "08019"  # Barcelona location code in AEMET
    full_url = f"{base_url}{location_code}?api_key={api_key}"

    response = requests.get(full_url)
    response.raise_for_status()
    data = response.json()

    if "datos" in data:
        hourly_data_url = data["datos"]
        hourly_response = requests.get(hourly_data_url)
        hourly_response.raise_for_status()
        hourly_data = hourly_response.json()

        hourly_temps = []
        for entry in hourly_data[0]["prediccion"]["dia"]:
            if entry["fecha"] == date:
                for hour in entry["hora"]:
                    hourly_temps.append((hour["periodo"], hour["temperatura"]))
        return hourly_temps
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

# Load Excel data
def load_excel_data(file_path):
    return pd.read_excel(file_path)

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

    # Fetch hourly temperatures for 7th and 8th December using AEMET
    hourly_temp_7 = fetch_hourly_temperature_aemet("2024-12-07")
    hourly_temp_8 = fetch_hourly_temperature_aemet("2024-12-08")

    # Fetch electricity prices for 7th, 8th December, and today
    price_7 = fetch_electricity_price("2024-12-07")
    price_8 = fetch_electricity_price("2024-12-08")
    today_date = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")
    today_price = fetch_electricity_price(today_date)
    today_time







