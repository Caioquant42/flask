import pandas as pd
import json
import os
import sys
from statsmodels.tsa.stattools import coint
from datetime import datetime, timedelta
from dolphindb import session  # Assuming dolphinDB is the correct module for DolphinDB

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from apps.utils.dict import TICKERS_DICT

# Connect to the DolphinDB server
s = session()
s.connect("46.202.149.154", 8848, "admin", "123456")

# Get the tickers from TICKERS_DICT
tickers = TICKERS_DICT.get('IBOV', [])

# Define the table name
table_name = "stockdata_1d"

# Function to fetch data from DolphinDB
def fetch_data(table_name, tickers, start_date):
    # Load the table from the distributed file system
    s.run(f't = loadTable("dfs://yfs", "{table_name}")')

    # Execute the query to filter the data by Time, Symbol, and select specific columns
    query = f'''
    select Datetime, Symbol, AdjClose 
    from t 
    where Datetime > {start_date} and Symbol in {tickers}
    '''
    result = s.run(query)

    # Convert the query result to a DataFrame
    df = pd.DataFrame(result)
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    # Remove rows with NaN values in AdjClose
    df = df.dropna(subset=['AdjClose'])

    return df

# Function to perform the Engle-Granger cointegration test
def check_cointegration(asset1, asset2, df):
    try:
        coint_result = coint(df[asset1], df[asset2])
        return coint_result[1]  # Return the p-value
    except KeyError:
        print(f"Skipping cointegration test for {asset1} and {asset2} due to missing data.")
        return None  # Return None if either ticker is missing

# Function to perform cointegration analysis for a given time period
def perform_cointegration_analysis(tickers, start_date, period_name):
    # Fetch data for the specified period
    df = fetch_data(table_name, tickers, start_date)

    # Pivot the DataFrame to have tickers as columns
    df_pivot = df.pivot(index='Datetime', columns='Symbol', values='AdjClose')

    # Handle missing data
    df_pivot = df_pivot.fillna(method='ffill').dropna()

    # List to store JSON results
    cointegration_results = []

    # Counters for cointegrated and non-cointegrated pairs
    cointegrated_count = 0
    non_cointegrated_count = 0

    # Perform the cointegration test for each pair of tickers
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            asset1 = tickers[i]
            asset2 = tickers[j]

            # Skip if either asset is not in the DataFrame
            if asset1 not in df_pivot.columns or asset2 not in df_pivot.columns:
                print(f"Skipping cointegration test for {asset1} and {asset2} due to missing data.")
                continue

            p_value = check_cointegration(asset1, asset2, df_pivot)

            # Skip if p_value is None (due to missing data)
            if p_value is None:
                continue

            # Determine if they are cointegrated
            is_cointegrated = bool(p_value < 0.05)  # Convert to native Python boolean

            # Update counters
            if is_cointegrated:
                cointegrated_count += 1
            else:
                non_cointegrated_count += 1

            # Create dictionary for each result
            result = {
                "asset1": asset1,
                "asset2": asset2,
                "p_value": float(p_value),  # Ensure p_value is a native float
                "cointegrated": is_cointegrated
            }
            cointegration_results.append(result)
            print(f"Cointegration test between {asset1} and {asset2} - p-value: {p_value}")

    # Calculate percentages
    total_pairs = len(cointegration_results)
    if total_pairs > 0:
        cointegrated_percentage = (cointegrated_count / total_pairs) * 100
        non_cointegrated_percentage = (non_cointegrated_count / total_pairs) * 100
    else:
        cointegrated_percentage = 0
        non_cointegrated_percentage = 0

    # Return results and summary
    return {
        "results": cointegration_results,
        "summary": {
            "total_pairs": total_pairs,
            "cointegrated_pairs": cointegrated_count,
            "cointegrated_percentage": cointegrated_percentage,
            "non_cointegrated_pairs": non_cointegrated_count,
            "non_cointegrated_percentage": non_cointegrated_percentage
        }
    }

# Define start dates for the last 6 months and last 12 months
now = datetime.now()
start_date_6m = (now - timedelta(days=180)).strftime("%Y.%m.%d")
start_date_12m = (now - timedelta(days=365)).strftime("%Y.%m.%d")

# Perform cointegration analysis for the last 6 months
results_6m = perform_cointegration_analysis(tickers, start_date_6m, "last_6_months")

# Perform cointegration analysis for the last 12 months
results_12m = perform_cointegration_analysis(tickers, start_date_12m, "last_12_months")

# Combine results into a single JSON structure
combined_results = {
    "last_6_months": results_6m,
    "last_12_months": results_12m
}

# Convert combined results to JSON
combined_json = json.dumps(combined_results, indent=4)
print("Combined Cointegration Results in JSON format:")
print(combined_json)

# Save the combined JSON file in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
output_file_path = os.path.join(script_dir, "combined_cointegration_results.json")  # Define the output file path

with open(output_file_path, "w") as json_file:
    json_file.write(combined_json)

print(f"Combined JSON file saved to: {output_file_path}")