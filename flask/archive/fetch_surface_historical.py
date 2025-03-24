import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys
import time

# Add this block at the beginning of the file
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    from utils.dictionary import TICKERS_DICT
else:
    from .dictionary import TICKERS_DICT

def fetch_volatility_surface(spot, from_date, to_date):
    headers = {
        'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
    }

    url = f'https://api.oplab.com.br/v3/market/historical/options/{spot}/{from_date}/{to_date}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        options_data = response.json()
        
        print(f"Data received for {spot}:")
        print(json.dumps(options_data[:1], indent=2))  # Print the first item in the response
        
        if not options_data:
            print(f"No data received for {spot}")
            return None
        
        df = pd.DataFrame(options_data)
        print(f"Columns in the DataFrame: {df.columns}")
        
        if 'time' not in df.columns:
            print(f"'time' column not found in data for {spot}")
            return None
        
        df['time'] = pd.to_datetime(df['time'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        df['option_type'] = df['delta'].apply(lambda x: 'CALL' if x >= 0 else 'PUT')
        
        # Keep only the latest data point
        latest_time = df['time'].max()
        df = df[df['time'] == latest_time]
        
        return df.to_dict(orient='records')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {spot}: {e}")
        return None
    except KeyError as e:
        print(f"KeyError for {spot}: {e}")
        print(f"Data structure: {options_data[0].keys() if options_data else 'No data'}")
        return None
    except Exception as e:
        print(f"Unexpected error for {spot}: {e}")
        return None

def get_volatility_surface(ticker=None):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)  # Fetch data for the last day
    
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')

    all_tickers_data = {}

    tickers = [ticker] if ticker else TICKERS_DICT["TOP10"]

    for ticker in tickers:
        ticker_data = fetch_volatility_surface(ticker, from_date, to_date)
        if ticker_data:
            all_tickers_data[ticker] = ticker_data
        else:
            print(f"No data available for {ticker}")

    # Save the data to a JSON file in the export directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(current_dir, "export")
    os.makedirs(export_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'volatility_surface_{timestamp}.json'
    file_path = os.path.join(export_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tickers_data, f, ensure_ascii=False, indent=4, default=str)

    print(f"Volatility surface data saved to {file_path}")

    if ticker:
        return all_tickers_data.get(ticker, {"error": f"No data found for {ticker}"})
    return all_tickers_data

def get_surface_analysis():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(current_dir, "export")
    
    # Get the most recent file
    files = [f for f in os.listdir(export_dir) if f.startswith('volatility_surface_') and f.endswith('.json')]
    if not files:
        print("No volatility surface files found.")
        return {}
    
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(export_dir, x)))
    json_file_path = os.path.join(export_dir, latest_file)
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            surface_data = json.load(json_file)
        return surface_data
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {json_file_path}")
        return {}

# This part is for testing purposes when running the script directly
if __name__ == "__main__":
    all_data = get_volatility_surface()
    print(json.dumps(all_data, indent=2, default=str))
    
    # Test the get_surface_analysis function
    print("\nTesting get_surface_analysis function:")
    analysis_data = get_surface_analysis()
    print(json.dumps(analysis_data, indent=2, default=str))