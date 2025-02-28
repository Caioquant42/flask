import yfinance as yf
import pandas as pd
import json
import os
from statsmodels.tsa.stattools import coint

# Define the asset pairs
currency_pairs = ["PCAR3.SA","SANB11.SA","SUZB3.SA","RDOR3.SA", "VBBR3.SA", "TAEE11.SA","VALE3.SA"]

# Fetch the daily closing prices for each asset
data = {}
for pair in currency_pairs:
    ticker = yf.Ticker(pair)
    df = ticker.history(period="252d", interval="1d")
    data[pair] = df['Close']
    print(f"Fetched data for {pair}")

# Create a DataFrame with all the asset pairs
df = pd.DataFrame(data)

# Handle missing data
df = df.fillna(method='ffill').dropna()

# Function to perform the Engle-Granger cointegration test
def check_cointegration(asset1, asset2):
    coint_result = coint(df[asset1], df[asset2])
    return coint_result[1]  # Return the p-value

# List to store JSON results
cointegration_results = []

# Counters for cointegrated and non-cointegrated pairs
cointegrated_count = 0
non_cointegrated_count = 0

# Perform the cointegration test for each pair of currency pairs
for i in range(len(currency_pairs)):
    for j in range(i + 1, len(currency_pairs)):
        asset1 = currency_pairs[i]
        asset2 = currency_pairs[j]
        p_value = check_cointegration(asset1, asset2)

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

# Convert results to JSON
cointegration_json = json.dumps(cointegration_results, indent=4)
print("Cointegration Results in JSON format:")
print(cointegration_json)

# Save the JSON file in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
output_file_path = os.path.join(script_dir, "cointegration_results.json")  # Define the output file path

with open(output_file_path, "w") as json_file:
    json_file.write(cointegration_json)

print(f"JSON file saved to: {output_file_path}")

# Calculate percentages
total_pairs = len(cointegration_results)
cointegrated_percentage = (cointegrated_count / total_pairs) * 100
non_cointegrated_percentage = (non_cointegrated_count / total_pairs) * 100

# Print summary
print("\nSummary of Cointegration Results:")
print(f"Total pairs tested: {total_pairs}")
print(f"Cointegrated pairs: {cointegrated_count} ({cointegrated_percentage:.2f}%)")
print(f"Non-cointegrated pairs: {non_cointegrated_count} ({non_cointegrated_percentage:.2f}%)")