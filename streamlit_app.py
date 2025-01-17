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
    # Load and process data from Excel files
    manual_file = "data/Befre algrtihme - Manual regulation.xlsx"
    auto_file = "data/test with automatic heater regulation.xlsx"

    manual_data = load_excel_data(manual_file)
    auto_data = load_excel_data(auto_file)

    # Create two side-by-side columns for the plots
    col1, col2 = st.columns(2)

    with col1:
        st.header("Manual Regulation")
        fig_manual = plot_temp_state_current(manual_data, "Manual Regulation")
        st.pyplot(fig_manual)

    with col2:
        st.header("Automatic Regulation")
        fig_auto = plot_temp_state_current(auto_data, "Automatic Regulation")
        st.pyplot(fig_auto)

    # Display additional information in the sidebar
    st.sidebar.header("Today's Info")
    st.sidebar.markdown("*Barcelona, Spain*", unsafe_allow_html=True)
    temperature = fetch_current_temperature()
    st.sidebar.metric(label="Temperature (°C)", value=f"{temperature}°C" if temperature else "N/A")
    today_time = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%H:%M")
    st.sidebar.metric(label="Time", value=today_time)

except Exception as e:
    st.sidebar.error(f"Error fetching data: {e}")











