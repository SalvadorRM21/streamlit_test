import requests
import json
import pandas as pd
import numpy as np

# Create GET request
def get_data_from_api(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response from {url}: {e}")
            raise Exception(f"Failed to parse JSON response: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        raise Exception(f"API request failed: {e}")

if __name__ == "__main__":
    # Ejemplo: Obtener temperatura desde WeatherAPI
    try:
        url = "https://weatherapi-com.p.rapidapi.com/current.json"
        headers = {
            "X-RapidAPI-Key": "your_api_key",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }
        params = {"q": "Barcelona"}  # Eliminamos "dt" ya que no aplica en "current.json"

        weather_data = get_data_from_api(url, headers, params)
        print(f"Weather Data for Barcelona: {weather_data}")
    except Exception as e:
        print(f"Error fetching weather data: {e}")

    # Ejemplo: Obtener precio de electricidad desde REE API
    try:
        url = "https://api.esios.ree.es/indicators/1001"
        headers = {
            "Authorization": "Token token=your_ree_api_token",
            "Accept": "application/json; application/vnd.esios-api-v1+json"
        }
        params = {"start_date": "2022-12-08T00:00:00", "end_date": "2022-12-09T23:59:59"}

        electricity_price = get_data_from_api(url, headers, params)
        print(f"Electricity Price Data: {electricity_price}")
    except Exception as e:
        print(f"Error fetching electricity price data: {e}")




