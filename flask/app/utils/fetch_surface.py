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

def fetch_historical_options_data(spot, from_date, to_date, max_retries=5, retry_delay=10):
    headers = {
        'Access-Token': 'b3syD+4rUU5WX6rQrBMDtuT1Gbl35a0xyTQw9Ov7+8KTVTSBCVn1Y9maHTvAC4a3--VmCKxj9YzsILWt0fcJaIpQ==--ZDk2NGJiZGRkZTc5M2M4ZDUwOGFlMWQ2NDhhMGZhZDg='
    }

    url = f'https://api.oplab.com.br/v3/market/historical/options/{spot}/{from_date}/{to_date}'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            options_data = response.json()
            print(f"Historical Options Data for {spot} retrieved successfully.")
            return options_data, spot

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {spot}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to retrieve data for {spot} after {max_retries} attempts.")
                return None, spot

    return None, spot

from datetime import datetime

def get_surface_data(ticker=None):
    all_tickers_data = {}
    tickers = [ticker] if ticker else TICKERS_DICT["TOP10"]
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    for ticker in tickers:
        historical_data, _ = fetch_historical_options_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        print(f"Data structure for {ticker}:", json.dumps(historical_data[:1], indent=2))
        if historical_data and isinstance(historical_data, list):
            # Processar todos os dados históricos
            ticker_data = []
            latest_time = datetime.min
            for date_data in historical_data:
                if isinstance(date_data, dict):
                    date_data = [date_data]
                if isinstance(date_data, list):
                    for option in date_data:
                        option_time = datetime.strptime(option['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        if option_time > latest_time:
                            latest_time = option_time
                            ticker_data = []  # Limpar dados anteriores
                        if option_time == latest_time:
                            ticker_data.append(option)
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

def get_surface_analysis(ticker=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(current_dir, "export")
    
    # Get the most recent file
    files = [f for f in os.listdir(export_dir) if f.startswith('volatility_surface_') and f.endswith('.json')]
    if not files:
        print("No volatility surface data files found.")
        return {}
    
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(export_dir, x)))
    json_file_path = os.path.join(export_dir, latest_file)
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            surface_data = json.load(json_file)
        if ticker:
            return {ticker: surface_data.get(ticker, {})}
        return surface_data
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {json_file_path}")
        return {}

# This part is for testing purposes when running the script directly
if __name__ == "__main__":
    # Test the get_surface_data function
    print("Testing get_surface_data function:")
    surface_data = get_surface_data()
    print(json.dumps(surface_data, indent=2, default=str))
    
    # Test the get_surface_analysis function
    print("\nTesting get_surface_analysis function:")
    analysis_data = get_surface_analysis()
    print(json.dumps(analysis_data, indent=2, default=str))