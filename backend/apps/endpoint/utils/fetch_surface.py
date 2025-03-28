#!/usr/bin/env python3
import subprocess
import dolphindb as ddb
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, project_root)
from backend.apps.utils.dict import TICKERS_DICT

# Function to run update_surface_data.py
def run_update_surface_data():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    update_script_path = os.path.join(current_directory, 'update_surface_data.py')
    
    print("Running update_surface_data.py...")
    try:
        subprocess.run([sys.executable, update_script_path], check=True)
        print("update_surface_data.py completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running update_surface_data.py: {e}")
        sys.exit(1)  # Exit if the update script fails

# Run update_surface_data.py before the main code
run_update_surface_data()

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def fetch_vanilla_data(start_date=None, end_date=None):
    # If no dates are provided, use the last 7 days
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=8)
    
    # Convert dates to string format if they're datetime objects
    if isinstance(start_date, datetime):
        start_date = start_date.strftime('%Y.%m.%d')
    if isinstance(end_date, datetime):
        end_date = end_date.strftime('%Y.%m.%d')

    # DolphinDB script to fetch data
    script = f"""
    def fetchVanillaData(start_date, end_date) {{
        t = loadTable("dfs://zommalab", "vanilla")
        return select 
            symbol, time, spot_price, spot_symbol, option_type, due_date, 
            strike, days_to_maturity, volatility, poe, moneyness
        from t 
        where date(time) between date(start_date) : date(end_date)
    }}
    fetchVanillaData("{start_date}", "{end_date}")
    """

    try:
        # Execute the script and fetch the data
        data = s.run(script)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        print(f"Fetched {len(df)} rows from the vanilla table.")
        return df
    except Exception as e:
        print(f"Error fetching data from DolphinDB: {e}")
        return None


if __name__ == "__main__":
    df = fetch_vanilla_data()
    
    if df is not None:
        all_tickers_data = {}

        for ticker in TICKERS_DICT["TOP10"]:
            # Create a new DataFrame with only single ticker data
            ticker_df = df[df['spot_symbol'] == ticker]
            
            print(f"Created {ticker} DataFrame with {len(ticker_df)} rows.")
            
            # Get the last available time for the ticker
            last_time = ticker_df['time'].max()
            
            # Filter the DataFrame to include only rows with the last available time
            last_time_df = ticker_df[ticker_df['time'] == last_time]
            
            # Convert DataFrame to dict and add to all_tickers_data
            all_tickers_data[ticker] = last_time_df.to_dict(orient='records')
            
            # Display information about the last time data
            print(f"\nLast available time for {ticker}: {last_time}")
            print(f"Number of rows with the last available time: {len(last_time_df)}")
            print("\nFirst few rows of the last time data:")
            print(last_time_df.head)

        # Save all tickers' last time data to a single JSON file in the script directory
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
                
        # Define the export directory
        export_directory = os.path.join(current_directory, "export")

        # Ensure the export directory exists
        os.makedirs(export_directory, exist_ok=True)

        # Save all tickers' last time data to a single JSON file in the export directory
        all_tickers_json = os.path.join(export_directory, "all_tickers_last_time_data.json")

        with open(all_tickers_json, 'w') as json_file:
            json.dump(all_tickers_data, json_file, indent=2, default=str)
    
        print(f"\nSaved last available time data for all tickers to {all_tickers_json}")
        print(f"Code last executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Close the DolphinDB connection
    s.close()
