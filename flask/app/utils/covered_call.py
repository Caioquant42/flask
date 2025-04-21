# covered_call.py
import sys
import os
import json
import requests
import time
import cmath
from typing import Dict, List, Any

# Define the underlying assets
underlying = ["PETR4","VALE3", "BOVA11", "BBAS3", "BBDC4", "COGN3", "MGLU3", "ITUB4", "WEGE3", "EMBR3"]

call_bid = 'bid'  # change to bid/close if needed

# Define API key and headers
headers = {
    'Access-Token': 'b3syD+4rUU5WX6rQrBMDtuT1Gbl35a0xyTQw9Ov7+8KTVTSBCVn1Y9maHTvAC4a3--VmCKxj9YzsILWt0fcJaIpQ==--ZDk2NGJiZGRkZTc5M2M4ZDUwOGFlMWQ2NDhhMGZhZDg='
}

# Define base URL for the new API endpoint
option_base_url = 'https://api.oplab.com.br/v3/market/options'

# Define base URL for the new API endpoint
spot_base_url = 'https://api.oplab.com.br/v3/market/stocks'

def fetch_underlying_data(underlying_symbols, max_retries=3, delay=5):
    all_data = []
    
    for symbol in underlying_symbols:
        url = f"{spot_base_url}/{symbol}"
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Filter the data to include only the desired fields
                filtered_data = {
                    "symbol": data.get("symbol"),
                    "type": data.get("type"),
                    "name": data.get("name"),
                    "open": data.get("open"),
                    "high": data.get("high"),
                    "low": data.get("low"),
                    "close": data.get("close"),
                    "volume": data.get("volume"),
                    "financial_volume": data.get("financial_volume"),
                    "trades": data.get("trades"),
                    "bid": data.get("bid"),
                    "ask": data.get("ask"),
                    "category": data.get("category"),
                    "contract_size": data.get("contract_size"),
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at"),
                    "parent_symbol": symbol  # Add parent_symbol to the filtered data
                }
                
                all_data.append(filtered_data)  # Append filtered data for each symbol
                break  # Exit retry loop if successful
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                print(f"Attempt {attempt + 1} failed for {symbol}: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to retrieve data for {symbol} after {max_retries} attempts. Skipping...")
    
    return all_data

def fetch_option_data(underlying_symbols, max_retries=3, delay=5):
    all_data = []
    
    for symbol in underlying_symbols:
        url = f"{option_base_url}/{symbol}"
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                # Add parent_symbol to each option in the data
                for option in data:
                    option['parent_symbol'] = symbol
                all_data.extend(data)  # Combine data from all symbols
                break  # Exit retry loop if successful
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                print(f"Attempt {attempt + 1} failed for {symbol}: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to retrieve data for {symbol} after {max_retries} attempts. Skipping...")
    
    return all_data

def save_raw_data_to_json(data, file_path):
    if not data:
        print("No data to save.")
        return
    
    # Save raw data to JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f"Raw data saved to {file_path}")

def calculate_option_metrics(option, underlying_data):
    # Fetch the close price (spot_price) for the underlying asset
    parent_symbol = option.get('parent_symbol')
    spot_price = None

    # Find the underlying asset data for the parent_symbol
    for underlying_asset in underlying_data:
        if underlying_asset['symbol'] == parent_symbol:
            spot_price = underlying_asset.get('ask')
            break

    # If spot_price is not found, default to 0
    if spot_price is None:
        print(f"Warning: Could not find spot price for {parent_symbol}. Defaulting to 0.")
        spot_price = 0

    # Use the spot_price for calculations
    close_price = option.get(call_bid, 0)
    strike = option.get('strike', 0)
    days_to_maturity = option.get('days_to_maturity', 0)

    # Determine moneyness
    if strike > spot_price:
        moneyness = 'OTM'
    else:
        moneyness = 'ITM'

    # Calculate intrinsic and extrinsic values
    intrinsic_value = max(spot_price - strike, 0)
    extrinsic_value = max(close_price - intrinsic_value, 0)
    protection = intrinsic_value / spot_price if spot_price != 0 else 0
    pm = spot_price - close_price
    embedded_interest = extrinsic_value / spot_price if spot_price != 0 else 0
    annual_return = (1 + embedded_interest)**(252 / days_to_maturity) - 1 if days_to_maturity != 0 else 0
    score = (protection * annual_return) if annual_return != 0 else 0

    # Add calculated metrics to the option
    option['moneyness'] = moneyness
    option['intrinsic_value'] = intrinsic_value
    option['extrinsic_value'] = extrinsic_value
    option['pm'] = pm
    option['protection'] = protection
    option['embedded_interest'] = embedded_interest
    option['annual_return'] = annual_return
    option['score'] = score
    option['spot_price'] = spot_price  # Add spot_price to the option for reference

    return option

def save_processed_data_to_json(data, file_path):
    if not data:
        print("No data to save.")
        return
    
    # Save processed data to JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f"Processed data saved to {file_path}")

def filter_covered_calls(data):
    # Filter only CALL options with sufficient financial volume
    filtered_data = [
        option for option in data
        if option['category'] == 'CALL' and option.get('financial_volume', 0) > 1000
    ]
    
    # Sort by annual return in descending order
    filtered_data.sort(key=lambda x: x.get('annual_return', 0), reverse=True)
    
    return filtered_data

def save_to_json(data, current_directory):
    if not data:
        print("No data to save.")
        return

    # Categorize data based on days_to_maturity
    less_than_14 = [option for option in data if option.get('days_to_maturity', 0) < 14]
    between_15_and_30 = [option for option in data if 15 <= option.get('days_to_maturity', 0) < 30]
    between_30_and_60 = [option for option in data if 30 <= option.get('days_to_maturity', 0) < 60]
    more_than_60 = [option for option in data if option.get('days_to_maturity', 0) >= 60]

    # Define file paths for JSON outputs using the current directory
    less_than_14_path = os.path.join(current_directory, "covered_calls_less_than_14_days.json")
    between_15_and_30_path = os.path.join(current_directory, "covered_calls_between_15_and_30_days.json")
    between_30_and_60_path = os.path.join(current_directory, "covered_calls_between_30_and_60_days.json")
    more_than_60_path = os.path.join(current_directory, "covered_calls_more_than_60_days.json")

    # Save JSON data to the respective file paths
    with open(less_than_14_path, 'w', encoding='utf-8') as f:
        json.dump(less_than_14, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {less_than_14_path}")

    with open(between_15_and_30_path, 'w', encoding='utf-8') as f:
        json.dump(between_15_and_30, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {between_15_and_30_path}")

    with open(between_30_and_60_path, 'w', encoding='utf-8') as f:
        json.dump(between_30_and_60, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {between_30_and_60_path}")

    with open(more_than_60_path, 'w', encoding='utf-8') as f:
        json.dump(more_than_60, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {more_than_60_path}")

def get_covered_call_analysis() -> Dict[str, List[Dict[str, Any]]]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(current_dir, "export")
    
    covered_call_data = {}
    
    maturity_ranges = [
        "less_than_14_days",
        "between_15_and_30_days",
        "between_30_and_60_days",
        "more_than_60_days"
    ]
    
    for maturity_range in maturity_ranges:
        file_name = f"covered_calls_{maturity_range}.json"
        file_path = os.path.join(export_dir, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                covered_call_data[maturity_range] = data
        except FileNotFoundError:
            print(f"Warning: File not found at {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file {file_path}")
    
    return covered_call_data

def main():
    # Fetch underlying data
    underlying_data = fetch_underlying_data(underlying)
    
    # Fetch raw option data
    raw_data = fetch_option_data(underlying)
    
    # Calculate option metrics for each option using the underlying data
    processed_data = [calculate_option_metrics(option, underlying_data) for option in raw_data]
    
    # Filter for covered calls only
    covered_calls = filter_covered_calls(processed_data)
    
    # Save processed data to JSON files based on days_to_maturity
    current_directory = os.path.dirname(os.path.abspath(__file__))
    export_directory = os.path.join(current_directory, "export")
    
    # Create export directory if it doesn't exist
    os.makedirs(export_directory, exist_ok=True)
    
    save_to_json(covered_calls, export_directory)

if __name__ == "__main__":
    main()