from dolphindb import session
import pandas as pd
import json
from datetime import datetime
import numpy as np
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from apps.utils.dict import TICKERS_DICT

tickers = TICKERS_DICT.get('IBOV', [])

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

resolutions = ['1h', '1d']

# Connect to the DolphinDB server
s = session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def process_resolution(resolution):
    # Load the table from the distributed file system
    s.run('t = loadTable("dfs://oplab", "stockdata")')

    # Execute the query to filter the data by Time, Resolution, Symbol, and select specific columns
    query = f'''
    select Time, Symbol, Close 
    from t 
    where Time > 2023.01.01 and Resolution = '{resolution}' and Symbol in {tickers}
    '''
    result = s.run(query)

    # Convert the query result to a DataFrame
    df = pd.DataFrame(result)
    df["Time"] = pd.to_datetime(df["Time"])

    # Remove rows with NaN values in Close
    df = df.dropna(subset=['Close'])

    # Function to calculate RSI for a single symbol
    def calculate_symbol_rsi(group):
        group = group.sort_values(by="Time")
        group["RSI"] = calculate_rsi(group)
        return group.iloc[-1]  # Return only the last row

    # Calculate RSI for each symbol
    latest_rsi = df.groupby("Symbol", group_keys=False).apply(calculate_symbol_rsi).reset_index(drop=True)

    # Filter for overbought (RSI > 70) and oversold (RSI < 30) conditions
    # Also ensure Close is not NaN
    overbought = latest_rsi[(latest_rsi['RSI'] > 70) & (~np.isnan(latest_rsi['Close']))].copy()
    oversold = latest_rsi[(latest_rsi['RSI'] < 30) & (~np.isnan(latest_rsi['Close']))].copy()

    # Convert Time to string format
    overbought['Time'] = overbought['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    oversold['Time'] = oversold['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return {
        "overbought": overbought.to_dict('records'),
        "oversold": oversold.to_dict('records')
    }

# Process all resolutions and store results
all_results = {}
for resolution in resolutions:
    print(f"Processing {resolution}...")
    all_results[resolution] = process_resolution(resolution)
    print(f"Completed processing {resolution}")

# Custom JSON encoder to handle any remaining non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

# Save all results to a single JSON file
with open('ibov_overbought_oversold_rsi_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, cls=CustomJSONEncoder)

print("\nAll data processing completed.")
print("Results have been saved to 'ibov_overbought_oversold_rsi_results.json'")

# Display summary for each resolution
for resolution in resolutions:
    print(f"\nSummary for {resolution}:")
    print(f"Overbought stocks: {len(all_results[resolution]['overbought'])}")
    print(f"Oversold stocks: {len(all_results[resolution]['oversold'])}")

# Display a sample from each category for the first resolution
first_resolution = resolutions[0]
print(f"\nSample of overbought stocks for {first_resolution}:")
print(pd.DataFrame(all_results[first_resolution]['overbought']).head())
print(f"\nSample of oversold stocks for {first_resolution}:")
print(pd.DataFrame(all_results[first_resolution]['oversold']).head())