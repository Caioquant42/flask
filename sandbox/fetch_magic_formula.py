import sys
import os
import json
import requests
import time

# Define the attribute and other parameters
attribute = "magic_formula"
group_by = "sector"  # Optional: You can change this to None if not needed
limit = 20  # Default is 20, but you can change this
sort = "desc"  # Default is 'asc', but you can change this
financial_volume_start = 0  # Default is 0, but you can change this

# Define API key and headers
headers = {
    'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
}

# Define base URL for the API endpoint
base_url = f'https://api.oplab.com.br/v3/market/statistics/ranking/{attribute}'

def fetch_fundamental_data(attribute, group_by=None, limit=20, sort='asc', financial_volume_start=0, max_retries=3, delay=5):
    params = {
        'group_by': group_by,
        'limit': limit,
        'sort': sort,
        'financial_volume_start': financial_volume_start
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=30)
            print(f"Response Status Code: {response.status_code}")  # Print status code
            print(f"Response Content: {response.text}")  # Print raw response content
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()  # Return the JSON data if successful
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to retrieve data after {max_retries} attempts.")
                return None  # Return None if all attempts fail

def save_to_json(data, filename='fundamental_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

# Fetch data for the specified attribute and parameters
data = fetch_fundamental_data(attribute, group_by, limit, sort, financial_volume_start)

# Save the data to a JSON file
if data:
    save_to_json(data)
else:
    print("No data to save.")