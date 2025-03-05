import pandas as pd
from datetime import datetime, timedelta
import json
import requests
import time
import matplotlib.pyplot as plt

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

def fetch_vanilla_data(start_date=None, end_date=None):
    # Fetch data from the API
    underlying_symbols = ['PETR4']  # Only fetch data for PETR4
    api_data = fetch_underlying_data(underlying_symbols)
    
    if not api_data or not api_data.get('PETR4'):
        print("No data fetched from the API.")
        return None
    
    # Convert API data to a DataFrame
    data = api_data['PETR4']
    df = pd.DataFrame(data)
    
    # Add a 'spot_symbol' column to match the original DataFrame structure
    df['spot_symbol'] = 'PETR4'
    
    # Convert 'due_date' to datetime for filtering
    df['due_date'] = pd.to_datetime(df['due_date'])
    
    print(f"Fetched {len(df)} rows from the API.")
    return df


if __name__ == "__main__":
    df = fetch_vanilla_data()
    
    if df is not None:
        # Filter for the specific due_date
        specific_due_date = "2025-03-21T00:00:00"
        specific_due_date_df = df[df['due_date'] == specific_due_date]
        
        # Filter calls: strike >= spot_price
        calls_df = specific_due_date_df[
            (specific_due_date_df['type'] == 'CALL') & 
            (specific_due_date_df['strike'] >= specific_due_date_df['spot_price'])
        ]
        
        # Filter puts: strike <= spot_price
        puts_df = specific_due_date_df[
            (specific_due_date_df['type'] == 'PUT') & 
            (specific_due_date_df['strike'] <= specific_due_date_df['spot_price'])
        ]
        
        # Convert the DataFrames to lists of dictionaries (records)
        calls_data = calls_df.to_dict(orient='records')
        puts_data = puts_df.to_dict(orient='records')
        
        # Convert Timestamp objects to strings
        for record in calls_data + puts_data:
            for key, value in record.items():
                if isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat()
        
        # Save the calls data to a JSON file
        with open("petr4_calls_specific_due_date_data.json", 'w', encoding='utf-8') as f:
            json.dump(calls_data, f, indent=4, ensure_ascii=False)
        print(f"Call data for 'PETR4' with due_date '{specific_due_date}' has been saved to 'petr4_calls_specific_due_date_data.json'.")
        
        # Save the puts data to a JSON file
        with open("petr4_puts_specific_due_date_data.json", 'w', encoding='utf-8') as f:
            json.dump(puts_data, f, indent=4, ensure_ascii=False)
        print(f"Put data for 'PETR4' with due_date '{specific_due_date}' has been saved to 'petr4_puts_specific_due_date_data.json'.")

        # Plotting the close price against the strike price
        plt.figure(figsize=(12, 6))

        # Plot calls data
        plt.scatter(calls_df['strike'], calls_df['close'], color='blue', label='Calls', alpha=0.7)
        
        # Plot puts data
        plt.scatter(puts_df['strike'], puts_df['close'], color='red', label='Puts', alpha=0.7)
        
        # Add labels and title
        plt.xlabel('Strike Price')
        plt.ylabel('Close Price')
        plt.title(f"Close Price vs Strike Price for PETR4 (Due Date: {specific_due_date})")
        plt.legend()
        plt.grid(True)
        
        # Show the plot
        plt.show()