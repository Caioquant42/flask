import sys
import os
import json
import requests
import time

# Define the underlying assets
underlying = ['PETR4']

# Define API key and headers
headers = {
    'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
}

# Define base URL for the API endpoint
base_url = 'https://api.oplab.com.br/v3/market/options'

def fetch_underlying_data(underlying_symbols, max_retries=3, delay=5):
    all_data = {}
    
    for symbol in underlying_symbols:
        url = f"{base_url}/{symbol}"
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=30)  # Add a timeout
                response.raise_for_status()  # Raise an exception for bad status codes
                all_data[symbol] = response.json()
                break  # Exit the retry loop if successful
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                print(f"Attempt {attempt + 1} failed for {symbol}: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to retrieve data for {symbol} after {max_retries} attempts. Skipping...")
                    all_data[symbol] = None  # Store None if all attempts fail
    
    return all_data

def save_to_json(data, filename='options_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

# Fetch data for all underlying symbols
data = fetch_underlying_data(underlying)

# Save the data to a JSON file
save_to_json(data)