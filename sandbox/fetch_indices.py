import requests
import json
from datetime import datetime

# Define the instrument symbol and resolution
symbol = 'IMAT'  # Example: PETR4 (Petrobras)
resolution = '1d'  # Default: "1d" (daily data)

# Define the date range (from and to)
start_date = '2024-01-01'  # Example: Start date
end_date = '2025-10-01'    # Example: End date

# Define optional query parameters
amount = None  # Optional: Number of items
raw = False    # Default: False (include financial data)
smooth = False # Default: False (do not fill zero close values)
df = 'timestamp'  # Default: "timestamp" (date format)

# Define API key and headers
headers = {
    'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
}

# Define base URL for the API endpoint
base_url = f'https://api.oplab.com.br/v3/market/historical/{symbol}/{resolution}'

def fetch_historical_data(symbol, resolution, start_date, end_date, amount=None, raw=False, smooth=False, df='timestamp'):
    # Define query parameters
    params = {
        'from': start_date,
        'to': end_date,
        'amount': amount,
        'raw': str(raw).lower(),
        'smooth': str(smooth).lower(),
        'df': df
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()  # Return the JSON data
        else:
            print(f"Failed to retrieve data. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

def save_to_json(data, filename='historical_data.json'):
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Fetch historical data
data = fetch_historical_data(symbol, resolution, start_date, end_date, amount, raw, smooth, df)

# Save the data to a JSON file
save_to_json(data)