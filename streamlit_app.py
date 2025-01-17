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
price_9 = fetch_electricity_price("2024-12-09")
price_10 = fetch_electricity_price("2024-12-10")
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

# Static data for plotting
voltage = 220  # Assumed voltage in volts
data = {
    "2024-12-07": [
        ("6:25:00", 17.00, 0.00, "OFF"), ("6:25:45", 17.16, 0.00, "OFF"), ("6:26:30", 16.59, 0.00, "OFF"),
        ("6:27:15", 17.08, 5.58, "ON"), ("6:28:00", 17.16, 5.53, "ON"), ("6:28:45", 17.08, 5.50, "ON"),
        ("6:29:30", 17.16, 5.54, "ON"), ("6:30:15", 16.91, 5.49, "ON"), ("6:31:00", 17.48, 5.49, "ON"),
        ("6:31:45", 18.20, 5.46, "ON"), ("6:32:30", 17.88, 5.45, "ON"), ("6:33:15", 17.64, 5.46, "ON"),
        ("6:34:00", 17.56, 5.45, "ON"), ("6:34:45", 17.96, 5.46, "ON"), ("6:35:30", 18.20, 5.44, "ON"),
        ("6:36:15", 18.04, 5.43, "ON"), ("6:37:00", 18.04, 5.41, "ON"), ("6:37:45", 18.20, 5.43, "ON"),
        ("6:38:30", 17.96, 5.42, "ON"), ("6:39:15", 17.96, 5.41, "ON"), ("6:40:00", 18.45, 5.40, "ON"),
        ("6:40:45", 18.45, 5.40, "ON"), ("6:41:30", 18.45, 5.40, "ON"), ("6:42:15", 18.45, 5.39, "ON"),
        ("6:43:00", 19.01, 5.38, "ON"), ("6:43:45", 18.69, 5.38, "ON"), ("6:44:30", 19.25, 5.37, "ON"),
        ("6:45:15", 19.33, 5.37, "ON"), ("6:46:00", 19.49, 5.38, "ON"), ("6:46:45", 19.17, 5.38, "ON"),
        ("6:47:30", 19.81, 5.36, "ON"), ("6:48:15", 19.33, 5.37, "ON"), ("6:49:00", 19.41, 5.37, "ON"),
        ("6:49:45", 19.73, 5.37, "ON"), ("6:50:30", 19.65, 5.37, "ON"), ("6:51:15", 19.65, 5.36, "ON"),
        ("6:52:00", 19.65, 5.36, "ON"), ("6:52:45", 19.57, 5.37, "ON"), ("6:53:30", 20.22, 5.36, "ON"),
        ("6:54:15", 19.81, 5.35, "ON"), ("6:55:00", 19.90, 5.35, "ON"), ("6:55:45", 20.38, 5.36, "ON"),
        ("6:56:30", 19.98, 5.35, "ON"), ("6:57:15", 19.98, 5.35, "ON"), ("6:58:00", 20.78, 5.34, "ON"),
        ("6:58:45", 19.90, 5.35, "ON"), ("6:59:30", 20.62, 5.36, "ON"), ("7:00:15", 20.22, 5.37, "ON")
    ],
    "2024-12-08": [
        ("6:25:45", 16.59, 0.00, "OFF"), ("6:26:30", 16.27, 5.66, "ON"), ("6:27:15", 16.19, 5.58, "ON"),
        ("6:28:00", 15.95, 5.54, "ON"), ("6:28:45", 16.03, 5.52, "ON"), ("6:29:30", 15.87, 5.51, "ON"),
        ("6:30:15", 15.95, 5.50, "ON"), ("6:31:00", 16.27, 5.49, "ON"), ("6:31:45", 16.43, 5.49, "ON"),
        ("6:32:30", 16.43, 5.49, "ON"), ("6:33:15", 16.59, 5.47, "ON"), ("6:34:00", 16.43, 5.46, "ON"),
        ("6:34:45", 17.16, 5.48, "ON"), ("6:35:30", 16.59, 5.46, "ON"), ("6:36:15", 16.75, 5.45, "ON"),
        ("6:37:00", 16.59, 5.43, "ON"), ("6:37:45", 16.91, 5.45, "ON"), ("6:38:30", 17.16, 5.44, "ON"),
        ("6:39:15", 16.43, 5.45, "ON"), ("6:40:00", 16.91, 5.44, "ON"), ("6:40:45", 16.67, 5.43, "ON"),
        ("6:41:30", 17.24, 5.42, "ON"), ("6:42:15", 16.75, 5.41, "ON"), ("6:43:00", 17.16, 5.43, "ON"),
        ("6:43:45", 17.72, 5.42, "ON"), ("6:44:30", 17.32, 5.43, "ON"), ("6:45:15", 17.08, 5.42, "ON"),
        ("6:46:00", 17.24, 5.40, "ON"), ("6:46:45", 17.16, 5.41, "ON"), ("6:47:30", 17.16, 5.43, "ON")
    ],
    "2024-12-09": [
        ("6:25:00", 16.00, 0.00, "OFF"), ("6:25:45", 16.10, 5.40, "ON"), ("6:26:30", 16.30, 5.20, "ON"),
        ("6:27:15", 16.50, 5.10, "ON"), ("6:28:00", 16.70, 5.00, "ON"), ("6:28:45", 16.90, 4.80, "ON"),
        ("6:29:30", 17.10, 4.70, "ON"), ("6:30:15", 17.30, 4.60, "ON"), ("6:31:00", 17.50, 4.50, "ON"),
        ("6:31:45", 17.70, 4.40, "ON"), ("6:32:30", 17.90, 4.30, "ON"), ("6:33:15", 18.10, 4.20, "ON"),
        ("6:34:00", 18.30, 4.10, "ON"), ("6:34:45", 18.50, 4.00, "ON"), ("6:35:30", 18.70, 3.90, "ON"),
        ("6:36:15", 18.90, 3.80, "ON"), ("6:37:00", 19.10, 3.70, "ON"), ("6:37:45", 19.30, 3.60, "ON"),
        ("6:38:30", 19.50, 3.50, "ON"), ("6:39:15", 19.70, 3.40, "ON"), ("6:40:00", 19.90, 3.30, "ON"),
        ("6:40:45", 20.10, 3.20, "ON"), ("6:41:30", 20.30, 3.10, "ON"), ("6:42:15", 20.50, 3.00, "ON"),
        ("6:43:00", 20.70, 2.90, "ON"), ("6:43:45", 20.90, 2.80, "ON"), ("6:44:30", 21.10, 2.70, "ON")
    ],
    "2024-12-10": [
        ("6:25:00", 15.80, 0.00, "OFF"), ("6:25:45", 15.90, 4.80, "ON"), ("6:26:30", 16.00, 4.70, "ON"),
        ("6:27:15", 16.20, 4.60, "ON"), ("6:28:00", 16.40, 4.50, "ON"), ("6:28:45", 16.60, 4.40, "ON"),
        ("6:29:30", 16.80, 4.30, "ON"), ("6:30:15", 17.00, 4.20, "ON"), ("6:31:00", 17.20, 4.10, "ON"),
        ("6:31:45", 17.40, 4.00, "ON"), ("6:32:30", 17.60, 3.90, "ON"), ("6:33:15", 17.80, 3.80, "ON"),
        ("6:34:00", 18.00, 3.70, "ON"), ("6:34:45", 18.20, 3.60, "ON"), ("6:35:30", 18.40, 3.50, "ON"),
        ("6:36:15", 18.60, 3.40, "ON"), ("6:37:00", 18.80, 3.30, "ON"), ("6:37:45", 19.00, 3.20, "ON"),
        ("6:38:30", 19.20, 3.10, "ON"), ("6:39:15", 19.40, 3.00, "ON"), ("6:40:00", 19.60, 2.90, "ON"),
        ("6:40:45", 19.80, 2.80, "ON"), ("6:41:30", 20.00, 2.70, "ON"), ("6:42:15", 20.20, 2.60, "ON"),
        ("6:43:00", 20.40, 2.50, "ON"), ("6:43:45", 20.60, 2.40, "ON"), ("6:44:30", 20.80, 2.30, "ON")
    ]
}

# Prepare data for plotting
hourly_temp_7 = data["2024-12-07"]
hourly_temp_8 = data["2024-12-08"]
hourly_temp_9 = data["2024-12-09"]
hourly_temp_10 = data["2024-12-10"]

df_7 = pd.DataFrame(hourly_temp_7, columns=["Time", "Temperature", "Current", "Heater State"])
df_8 = pd.DataFrame(hourly_temp_8, columns=["Time", "Temperature", "Current", "Heater State"])
df_9 = pd.DataFrame(hourly_temp_9, columns=["Time", "Temperature", "Current", "Heater State"])
df_10 = pd.DataFrame(hourly_temp_10, columns=["Time", "Temperature", "Current", "Heater State"])

# Calculate power and consumption in kWh
def calculate_consumption(df):
    df["Power (W)"] = df["Current"] * voltage
    df["Consumption (kWh)"] = df["Power (W)"] * (45 / 3600) / 1000
    return df

df_7 = calculate_consumption(df_7)
df_8 = calculate_consumption(df_8)
df_9 = calculate_consumption(df_9)
df_10 = calculate_consumption(df_10)

# Create two side-by-side columns for the temperature and current plots
for day, df, title in zip([
    "7th December 2024",
    "8th December 2024",
    "9th December 2024",
    "10th December 2024"
], [df_7, df_8, df_9, df_10], ["Room Temperature and Current"] * 4):
    st.header(day)
    fig, ax = plt.subplots(figsize=(6, 3))  # Adjust height
    fig.patch.set_facecolor('none')  # Transparent background for the figure
    ax.set_facecolor((0, 0, 0, 0))  # Transparent background for the axes
    ax.plot(df_8["Time"], df_10[:"room curve"][{"line.text"]




