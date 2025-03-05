import requests
import json
from datetime import datetime, timedelta

# List of tickers
tickers = [
    "IBOV", "IBXX", "IBXL", "IBRA", "IGCX", "ITAG", "IGNM", "IGCT",
    "IDIV", "MLCX", "SMLL", "IVBX2", "ICO2", "ISEE", "ICON", "IEEX",
    "IFNC", "IMOB", "INDX", "IMAT", "UTIL", "IFIX", "BDRX"
]

# Define the resolution
resolution = '1d'  # Daily data

# Define optional query parameters
amount = None  # Optional: Number of items
raw = False    # Default: False (include financial data)
smooth = False # Default: False (do not fill zero close values)
df = 'iso'  # Default: "timestamp" (date format)

# Define API key and headers
headers = {
    'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
}

# Define base URL for the API endpoint
base_url = 'https://api.oplab.com.br/v3/market/historical'

def fetch_historical_data(symbol, resolution, start_date, end_date, amount=None, raw=False, smooth=False, df='iso'):
    # Define query parameters
    params = {
        'from': start_date,
        'to': end_date,
        'amount': amount,
        'raw': str(raw).lower(),
        'smooth': str(smooth).lower(),
        'df': df
    }
    
    # Construct the full URL
    url = f"{base_url}/{symbol}/{resolution}"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"Fetching data for {symbol}...")
        print(f"Response Status Code: {response.status_code}")
        
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()  # Return the JSON data
        else:
            print(f"Failed to retrieve data for {symbol}. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {symbol}: {str(e)}")
        return None

def save_to_json(data, filename='historical_data.json'):
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Define the date range (60 days from today)
end_date = datetime.now().strftime('%Y-%m-%d')  # Current date
start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')  # 60 days ago

# Fetch historical data for all tickers
all_data = {}
for ticker in tickers:
    data = fetch_historical_data(ticker, resolution, start_date, end_date, amount, raw, smooth, df)
    if data:
        all_data[ticker] = data

# Save the data to a JSON file
save_to_json(all_data)