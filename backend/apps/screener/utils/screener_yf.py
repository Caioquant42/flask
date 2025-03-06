import subprocess
import sys
import os
from dolphindb import session
import pandas as pd
import json
from datetime import datetime
import numpy as np
import warnings

# Function to run update_screener_data.py
def run_update_screener_data():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    update_script_path = os.path.join(current_directory, 'update_screener_data.py')
    
    print("Running update_screener_data.py...")
    try:
        subprocess.run([sys.executable, update_script_path], check=True)
        print("update_screener_data.py completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running update_screener_data.py: {e}")
        sys.exit(1)  # Exit if the update script fails

# Run update_screener_data.py before the main code
run_update_screener_data()

# Suppress the specific deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, message="DataFrameGroupBy.apply operated on the grouping columns.")
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from apps.utils.dict import TICKERS_DICT

tickers = TICKERS_DICT.get('IBOV', [])

def calculate_rsi(data, window=14):
    delta = data['AdjClose'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

table_names = ['stockdata_15m', 'stockdata_60m', 'stockdata_1d', 'stockdata_1wk']

# Connect to the DolphinDB server
s = session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def process_table(table_name):
    # Load the table from the distributed file system
    s.run(f't = loadTable("dfs://yfs", "{table_name}")')

    # Execute the query to filter the data by Time, Symbol, and select specific columns
    query = f'''
    select Datetime, Symbol, AdjClose 
    from t 
    where Datetime > 2024.01.01T03:00:00 and Symbol in {tickers}
    '''
    result = s.run(query)

    # Convert the query result to a DataFrame
    df = pd.DataFrame(result)
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    # Remove rows with NaN values in AdjClose
    df = df.dropna(subset=['AdjClose'])

    # Function to calculate RSI for a single symbol
    def calculate_symbol_rsi(group):
        group = group.sort_values(by="Datetime")
        group["RSI"] = calculate_rsi(group)
        return group.iloc[-1]  # Return only the last row

    # Calculate RSI for each symbol
    latest_rsi = df.groupby("Symbol", group_keys=False).apply(calculate_symbol_rsi).reset_index(drop=True)

    # Filter for overbought (RSI > 70) and oversold (RSI < 30) conditions
    # Also ensure AdjClose is not NaN
    overbought = latest_rsi[(latest_rsi['RSI'] > 70) & (~np.isnan(latest_rsi['AdjClose']))].copy()
    oversold = latest_rsi[(latest_rsi['RSI'] < 30) & (~np.isnan(latest_rsi['AdjClose']))].copy()

    # Convert Datetime to string format
    overbought['Datetime'] = overbought['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    oversold['Datetime'] = oversold['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return {
        "overbought": overbought.to_dict('records'),
        "oversold": oversold.to_dict('records')
    }

# Process all tables and store results
all_results = {}
for table in table_names:
    print(f"Processing {table}...")
    all_results[table] = process_table(table)
    print(f"Completed processing {table}")

# Custom JSON encoder to handle any remaining non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

# Get the full path for the JSON file in the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'ibov_overbought_oversold_rsi_results.json')

# Save all results to a single JSON file using the full path
with open(json_file_path, 'w') as f:
    json.dump(all_results, f, indent=2, cls=CustomJSONEncoder)

print("\nAll data processing completed.")
print(f"Results have been saved to '{json_file_path}'")

# Display summary for each table
for table in table_names:
    print(f"\nSummary for {table}:")
    print(f"Overbought stocks: {len(all_results[table]['overbought'])}")
    print(f"Oversold stocks: {len(all_results[table]['oversold'])}")

# Display a sample from each category for the first table
first_table = table_names[0]
print(f"\nSample of overbought stocks for {first_table}:")
print(pd.DataFrame(all_results[first_table]['overbought']).head())
print(f"\nSample of oversold stocks for {first_table}:")
print(pd.DataFrame(all_results[first_table]['oversold']).head())

print(f"Code last executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")