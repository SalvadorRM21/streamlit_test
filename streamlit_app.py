import requests
import json
import pandas as pd
import numpy as np

# Create GET request
def get_data_from_api(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    # Ejemplo: Obtener temperatura desde WeatherAPI
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {"q": "Barcelona", "dt": "2022-12-08"}

    try:
        weather_data = get_data_from_api(url, headers, params)
        print(f"Weather Data: {weather_data}")
    except Exception as e:
        print(f"Error: {e}")

    # Ejemplo: Obtener precio de electricidad desde REE API
    url = "https://api.esios.ree.es/indicators/1001"
    headers = {
        "Authorization": "Token token=your_ree_api_token",
        "Accept": "application/json; application/vnd.esios-api-v1+json"
    }
    params = {"start_date": "2022-12-08T00:00:00", "end_date": "2022-12-09T23:59:59"}

    try:
        electricity_price = get_data_from_api(url, headers, params)
        print(f"Electricity Price Data: {electricity_price}")
    except Exception as e:
        print(f"Error: {e}")

### Here starts the web app design
# Row A
a1, a2, a3 = st.columns(3)
a1.image(Image.open('HEATER LOGO.png'))
a2.metric("Wind", "9 mph", "-8%")
a3.metric("Humidity", "86%", "4%")

# Row B
b1, b2, b3, b4 = st.columns(4)
b1.metric("Temperature", "70 °F", "1.2 °F")
b2.metric("Wind", "9 mph", "-8%")
b3.metric("Humidity", "86%", "4%")
b4.metric("Humidity", "86%", "4%")



