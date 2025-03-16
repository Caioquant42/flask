import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import requests
import os

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

def calculate_rs_ratio(security, benchmark):
    rs = security / benchmark
    rs_ratio = rs / rs.rolling(window=14).mean() * 100  # Smoothed RS
    return rs_ratio

def calculate_rs_momentum(rs_ratio):
    # Adjust momentum to float around 1
    rs_momentum = (rs_ratio.pct_change(periods=1) + 1) * 100  # Shift to center around 1
    return rs_momentum

def save_to_json(data, filename='rrg_indices_data.json'):
    if data:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the export directory
        export_directory = os.path.join(current_directory, "export")

        # Ensure the export directory exists
        os.makedirs(export_directory, exist_ok=True)

        # Define the full path to save the file in the export directory
        full_path = os.path.join(export_directory, filename)

        # Save the data to a JSON file in the export directory
        with open(full_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Data saved to {full_path}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    # Define the date range (60 days from today)
    end_date = datetime.now().strftime('%Y-%m-%d')  # Current date
    start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')  # 60 days ago

    # Fetch historical data for all tickers
    all_data = {}
    for ticker in tickers:
        data = fetch_historical_data(ticker, resolution, start_date, end_date, amount, raw, smooth, df)
        if data:
            all_data[ticker] = data

    # Convert the fetched data into a pandas DataFrame
    df_list = []
    for ticker, data in all_data.items():
        if data and 'data' in data:
            for entry in data['data']:
                df_list.append({
                    'Datetime': entry['time'],
                    'Symbol': ticker,
                    'close': entry['close']
                })
    
    df = pd.DataFrame(df_list)

    # Pivot the DataFrame to have dates as index and tickers as columns
    data = df.pivot(index='Datetime', columns='Symbol', values='close')

    # Calculate RS-Ratio and RS-Momentum
    rs_ratios = {}
    rs_momentums = {}
    benchmark = 'IBOV'  # Assuming IBOV is part of the data and used as a benchmark
    json_data = {}

    for ticker in tickers:
        if ticker != benchmark and ticker in data.columns:
            rs_ratios[ticker] = calculate_rs_ratio(data[ticker], data[benchmark])
            rs_momentums[ticker] = calculate_rs_momentum(rs_ratios[ticker])
            
            # Get the last 5 valid RS-Ratio and RS-Momentum values along with their dates
            last_rs_ratio = rs_ratios[ticker].dropna().tail(5)
            last_rs_momentum = rs_momentums[ticker].dropna().tail(5)
            last_dates = pd.to_datetime(last_rs_ratio.index).strftime('%Y-%m-%d').tolist()

            # Store the last 5 RS-Ratio, RS-Momentum values, and their dates in JSON format
            json_data[ticker] = {
                "Dates": last_dates,
                "RS-Ratio": last_rs_ratio.tolist(),
                "RS-Momentum": last_rs_momentum.tolist()
            }
            
            # Print the last 5 RS-Ratio, RS-Momentum values, and their dates
            print(f"\n{ticker} - Last 5 Entries:")
            for date, rs_ratio, rs_momentum in zip(last_dates, last_rs_ratio, last_rs_momentum):
                print(f"Date: {date}, RS-Ratio: {rs_ratio:.4f}, RS-Momentum: {rs_momentum:.4f}")

    # Save the data to a JSON file
    save_to_json(json_data)
    print(f"Code last executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")