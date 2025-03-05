import sys
import os
import json
import requests
import time

# Define the underlying assets
underlying = ['PETR4', 'VALE3', 'B3SA3']

# Define API key and headers
headers = {
    'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
}

# Define base URL for the API endpoint
base_url = 'https://api.oplab.com.br/v3/market/options/strategies/covered'

def fetch_underlying_data(underlying_symbols, max_retries=3, delay=5):
    # Join the underlying symbols with commas
    underlying_param = ','.join(underlying_symbols)
    url = f"{base_url}?underlying={underlying_param}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)  # Add a timeout
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed for {underlying_param}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to retrieve data for {underlying_param} after {max_retries} attempts. Skipping...")
                return None

def calculate_option_metrics(option):
    """
    Calculate intrinsic value, extrinsic value, protection, embedded interest, and score for an option.
    """
    spot_price = option.get('spot_price', 0)
    close_price = option.get('bid', 0)
    strike = option.get('strike', 0)
    days_to_maturity = option.get('days_to_maturity', 0)

    # Intrinsic value: spot_price - strike
    intrinsic_value = max(spot_price - strike, 0)  # Ensure intrinsic value is not negative
    
    # Extrinsic value: close_price - intrinsic_value
    extrinsic_value = max(close_price - intrinsic_value, 0)  # Ensure extrinsic value is not negative
    
    # Protection: intrinsic_value / spot_price
    protection = intrinsic_value / spot_price if spot_price != 0 else 0

    # Preço Médio
    pm = spot_price - close_price
    
    # Embedded interest: extrinsic_value / spot_price
    embedded_interest = extrinsic_value / spot_price if spot_price != 0 else 0
    annual_return = (1 + embedded_interest)**(252 / days_to_maturity) - 1 if days_to_maturity != 0 else 0

    # Score Indicator 
    score = (protection * annual_return) if annual_return != 0 else 0
    
    # Add calculated metrics to the option dictionary
    option['intrinsic_value'] = intrinsic_value
    option['extrinsic_value'] = extrinsic_value
    option['pm'] = pm
    option['protection'] = protection
    option['embedded_interest'] = embedded_interest
    option['annual_return'] = annual_return
    option['score'] = score
    
    return option

def filter_and_attach_puts(data):
    """
    For each CALL option, find and attach relevant PUT options and calculate additional metrics.
    """
    for call_option in data:
        if call_option['category'] == 'CALL' and 'days_to_maturity' in call_option:
            # Filter PUT options with the same days_to_maturity and strike >= pm
            put_options = [
                put for put in data
                if put['category'] == 'PUT'
                and 'days_to_maturity' in put
                and put['days_to_maturity'] == call_option['days_to_maturity']
                and 'strike' in put
                and put['strike'] >= call_option.get('pm', 0)
                and put['parent_symbol'] == call_option['parent_symbol']
            ]
            
            # Sort PUT options by strike in ascending order
            put_options_sorted = sorted(put_options, key=lambda x: x['strike'])
            
            # Select the top 3 PUT options
            selected_puts = put_options_sorted[:3]
            
            # Extract required fields from the selected PUT options and calculate additional metrics
            call_option['puts'] = []
            for put in selected_puts:
                # Calculate extrinsic_value_result
                extrinsic_value_result = call_option['extrinsic_value'] - put.get('ask', 0)
                
                # Calculate embedded_interest_result
                spot_price = call_option.get('spot_price', 0)
                embedded_interest_result = extrinsic_value_result / spot_price if spot_price != 0 else 0
                
                # Calculate annual_return_result
                days_to_maturity = call_option.get('days_to_maturity', 0)
                annual_return_result = (1 + embedded_interest_result)**(252 / days_to_maturity) - 1 if days_to_maturity != 0 else 0
                
                # Add the PUT option with the new metrics
                call_option['puts'].append({
                    "symbol": put.get('symbol', ''),
                    "category": put.get('category', ''),
                    "days_to_maturity": put.get('days_to_maturity', 0),
                    "market_maker": put.get('market_maker', False),
                    "maturity_type": put.get('maturity_type', ''),
                    "strike": put.get('strike', ''),
                    "open": put.get('open', 0),
                    "high": put.get('high', 0),
                    "low": put.get('low', 0),
                    "close": put.get('close', 0),
                    "ask": put.get('ask', 0),
                    "bid": put.get('bid', 0),
                    "bid_volume": put.get('bid_volume', 0),
                    "ask_volume": put.get('ask_volume', 0),
                    "financial_volume": put.get('financial_volume', 0),
                    "extrinsic_value_result": extrinsic_value_result,
                    "embedded_interest_result": embedded_interest_result,
                    "annual_return_result": annual_return_result
                })
        else:
            # If the CALL option doesn't have 'days_to_maturity', skip it
            call_option['puts'] = []
    return data

def save_to_json(data):
    """
    Save the data to three JSON files based on days_to_maturity.
    """
    # Filter out options with a score of 0
    filtered_data = [option for option in data if option.get('score', 0) != 0]
    
    # Filter out CALL and PUT options with an empty 'puts' list
    filtered_data = [
        option for option in filtered_data
        if not (option['category'] in ['CALL', 'PUT'] and len(option.get('puts', [])) == 0)
    ]

    # Filter out options with financial_volume <= 0
    filtered_data = [
        option for option in filtered_data
        if option.get('financial_volume', 0) > 1000
    ]
    
    # Categorize data based on days_to_maturity
    less_than_14 = [option for option in filtered_data if option.get('days_to_maturity', 0) < 14]
    less_than_30 = [option for option in filtered_data if 14 <= option.get('days_to_maturity', 0) < 30]
    between_30_and_60 = [option for option in filtered_data if 30 <= option.get('days_to_maturity', 0) < 60]
    more_than_60 = [option for option in filtered_data if option.get('days_to_maturity', 0) >= 60]
    
    # Save each category to a separate JSON file
    with open("options_less_than_14_days.json", 'w', encoding='utf-8') as f:
        json.dump(less_than_14, f, indent=4, ensure_ascii=False)
    print("Data saved to options_less_than_14_days.json")   

    with open("options_less_than_30_days.json", 'w', encoding='utf-8') as f:
        json.dump(less_than_30, f, indent=4, ensure_ascii=False)
    print("Data saved to options_less_than_30_days.json")
    
    with open("options_between_30_and_60_days.json", 'w', encoding='utf-8') as f:
        json.dump(between_30_and_60, f, indent=4, ensure_ascii=False)
    print("Data saved to options_between_30_and_60_days.json")
    
    with open("options_more_than_60_days.json", 'w', encoding='utf-8') as f:
        json.dump(more_than_60, f, indent=4, ensure_ascii=False)
    print("Data saved to options_more_than_60_days.json")

# Fetch data for the underlying assets
data = fetch_underlying_data(underlying)

if data:
    # Calculate metrics for each option
    for option in data:
        calculate_option_metrics(option)
    
    # Filter and attach PUT options to CALL options
    data_with_puts = filter_and_attach_puts(data)
    
    # Sort the data by score in descending order
    sorted_data = sorted(data_with_puts, key=lambda x: x.get('score', 0), reverse=True)
    
    # Save the sorted data with metrics to JSON files based on days_to_maturity
    save_to_json(sorted_data)
else:
    print("No data retrieved.")