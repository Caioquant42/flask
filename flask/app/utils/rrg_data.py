# app/utils/rrg_data.py

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import dolphindb as ddb
from datetime import datetime, timedelta
import json
import requests

# Add this block at the beginning of the file
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    from utils.dictionary import TICKERS_DICT
else:
    from .dictionary import TICKERS_DICT

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

# Define API key and headers for the external API
headers = {
    'Access-Token': 'b3syD+4rUU5WX6rQrBMDtuT1Gbl35a0xyTQw9Ov7+8KTVTSBCVn1Y9maHTvAC4a3--VmCKxj9YzsILWt0fcJaIpQ==--ZDk2NGJiZGRkZTc5M2M4ZDUwOGFlMWQ2NDhhMGZhZDg='
}

# Define base URL for the API endpoint
base_url = 'https://api.oplab.com.br/v3/market/historical'

def fetch_stockdata_1d(tickers, start_date=None, end_date=None):
    # If no dates are provided, use the last 60 days
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    # Convert dates to string format if they're datetime objects
    if isinstance(start_date, datetime):
        start_date = start_date.strftime('%Y.%m.%dT%H:%M:%S')
    if isinstance(end_date, datetime):
        end_date = end_date.strftime('%Y.%m.%dT%H:%M:%S')

    # Convert tickers list to a string format for the query
    tickers_str = '(' + ', '.join([f'"{ticker}"' for ticker in tickers]) + ')'

    # DolphinDB script to fetch data from stockdata_1d
    script = f"""
    t = loadTable("dfs://yfs", "stockdata_1d")
    select Datetime, Symbol, AdjClose 
    from t 
    where Datetime between {start_date} : {end_date} and Symbol in {tickers_str}
    """

    try:
        # Execute the script and fetch the data
        data = s.run(script)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        print(f"Fetched {len(df)} rows from the stockdata_1d table.")
        return df
    except Exception as e:
        print(f"Error fetching data from DolphinDB: {e}")
        return None

def fetch_historical_data(symbol, resolution, start_date, end_date, amount=None, raw=False, smooth=False, df='iso'):
    params = {
        'from': start_date,
        'to': end_date,
        'amount': amount,
        'raw': str(raw).lower(),
        'smooth': str(smooth).lower(),
        'df': df
    }
    
    url = f"{base_url}/{symbol}/{resolution}"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"Fetching data for {symbol}...")
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
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
    rs_momentum = (rs_ratio.pct_change(periods=1) + 1) * 100  # Shift to center around 1
    return rs_momentum

def get_rrg_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "export", "rrg_data.json")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            rrg_data = json.load(json_file)
        print(f"RRG data loaded: {rrg_data}")
        
        for ticker in rrg_data:
            rrg_data[ticker]['RS_Ratio'] = rrg_data[ticker].pop('RS-Ratio')
            rrg_data[ticker]['RS_Momentum'] = rrg_data[ticker].pop('RS-Momentum')
        
        return rrg_data
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {json_file_path}")
        return {}

def calculate_rrg(data, benchmark):
    rs_ratios = {}
    rs_momentums = {}
    json_data = {}

    for ticker in data.columns:
        if ticker != benchmark:
            rs_ratios[ticker] = calculate_rs_ratio(data[ticker], data[benchmark])
            rs_momentums[ticker] = calculate_rs_momentum(rs_ratios[ticker])
            
            last_rs_ratio = rs_ratios[ticker].dropna().tail(5)
            last_rs_momentum = rs_momentums[ticker].dropna().tail(5)
            last_dates = pd.to_datetime(last_rs_ratio.index).strftime('%Y-%m-%d').tolist()

            if len(last_dates) > 0:
                json_data[ticker] = {
                    "Dates": last_dates,
                    "RS-Ratio": last_rs_ratio.tolist(),
                    "RS-Momentum": last_rs_momentum.tolist()
                }
                
                print(f"\n{ticker} - Last 5 Entries:")
                for date, rs_ratio, rs_momentum in zip(last_dates, last_rs_ratio, last_rs_momentum):
                    print(f"Date: {date}, RS-Ratio: {rs_ratio:.4f}, RS-Momentum: {rs_momentum:.4f}")
            else:
                print(f"\n{ticker} - No valid data")

    return json_data

if __name__ == "__main__":
    # Define the date range (60 days from today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    # 1. Fetch data from API for index tickers
    api_tickers = [
        "IBOV", "IBXX", "IBXL", "IBRA", "IGCX", "ITAG", "IGNM", "IGCT",
        "IDIV", "MLCX", "SMLL", "IVBX2", "ICO2", "ISEE", "ICON", "IEEX",
        "IFNC", "IMOB", "INDX", "IMAT", "UTIL", "IFIX", "BDRX"
    ]
    
    df_list_api = []
    for ticker in api_tickers:
        data = fetch_historical_data(ticker, '1d', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if data and 'data' in data:
            for entry in data['data']:
                df_list_api.append({
                    'Datetime': pd.to_datetime(entry['time']),
                    'Symbol': ticker,
                    'AdjClose': entry['close']
                })
    
    df_api = pd.DataFrame(df_list_api)
    data_api = df_api.pivot(index='Datetime', columns='Symbol', values='AdjClose')
    
    # Calculate RRG for API data
    json_data_api = calculate_rrg(data_api, 'IBOV')

    # 2. Fetch data from DolphinDB for TICKERS_DICT["IBOV"]
    ibov_tickers = TICKERS_DICT["IBOV"] + ['BOVA11']  # Add BOVA11 to the list of tickers
    df_dolphin = fetch_stockdata_1d(ibov_tickers, start_date, end_date)
    
    if df_dolphin is not None and not df_dolphin.empty:
        # Convert Datetime to pandas datetime
        df_dolphin['Datetime'] = pd.to_datetime(df_dolphin['Datetime'])
        
        data_dolphin = df_dolphin.pivot(index='Datetime', columns='Symbol', values='AdjClose')
        
        # Calculate RRG for DolphinDB data using BOVA11 as benchmark
        json_data_dolphin = calculate_rrg(data_dolphin, 'BOVA11')
    else:
        json_data_dolphin = {}
        print("Error: Unable to fetch data from DolphinDB or data is empty")

    # Combine results
    json_data = {**json_data_api, **json_data_dolphin}

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the export directory
    export_directory = os.path.join(current_directory, "export")

    # Ensure the export directory exists
    os.makedirs(export_directory, exist_ok=True)

    # Save the data to a JSON file in the export directory
    json_filename = os.path.join(export_directory, 'rrg_data.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    print("\nRS-Ratio and RS-Momentum data saved to rrg_data.json")
    print(f"Code last executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")