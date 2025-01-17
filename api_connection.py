import requests
import json

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
