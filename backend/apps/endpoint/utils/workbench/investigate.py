import dolphindb as ddb
import pandas as pd
from datetime import datetime

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def fetch_latest_vanilla_data(spot_symbol='PETR4'):
    # DolphinDB script corrigido para fetch the most recent data for a specific spot_symbol
    script = f"""
    def fetchLatestVanillaData(spot_symbol) {{
        t = loadTable("dfs://zommalab", "vanilla")
        latest_time = exec max(time) from t where spot_symbol = spot_symbol
        return select * from t where spot_symbol = spot_symbol and time = latest_time
    }}
    fetchLatestVanillaData("{spot_symbol}")
    """

    try:
        # Execute the script and fetch the data
        data = s.run(script)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        print(f"Fetched {len(df)} rows for {spot_symbol} from the vanilla table (most recent data).")
        return df
    except Exception as e:
        print(f"Error fetching data from DolphinDB: {e}")
        return None

def print_top_bottom_values(df):
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            print(f"\nTop 5 highest values for {column}:")
            print(df[column].nlargest(5))
            print(f"\nTop 5 lowest values for {column}:")
            print(df[column].nsmallest(5))
        elif df[column].dtype == 'object':
            print(f"\nTop 5 values for {column}:")
            print(df[column].value_counts().nlargest(5))
            print(f"\nBottom 5 values for {column}:")
            print(df[column].value_counts().nsmallest(5))

if __name__ == "__main__":
    spot_symbol = 'PETR4'
    # Fetch the most recent data for PETR4
    df = fetch_latest_vanilla_data(spot_symbol)
    
    if df is not None and not df.empty:
        print(f"\nAnalysis for {spot_symbol}:")
        print("=" * 40)
        
        # Display the first few rows
        print("\nData snapshot:")
        print(df.head())
        
        # Display basic statistics
        print("\nBasic statistics:")
        print(df.describe())
        
        # Print top 5 highest and lowest values for each column
        print_top_bottom_values(df)
        
        # Additional information
        print(f"\nTotal number of options: {len(df)}")
        print(f"Spot price: {df['spot_price'].iloc[0]:.2f}")
        print(f"Strike price range: {df['strike'].min():.2f} to {df['strike'].max():.2f}")
        print(f"Days to maturity range: {df['days_to_maturity'].min()} to {df['days_to_maturity'].max()}")
        
        # You can now perform further analysis or save the data
        # For example, to save to a CSV file:
        df.to_csv(f"{spot_symbol}_latest_vanilla_data.csv", index=False)
        
        # Or to save to an Excel file:
        # df.to_excel(f"{spot_symbol}_latest_vanilla_data.xlsx", index=False)
    else:
        print(f"No data available for {spot_symbol}")

    # Close the DolphinDB connection
    s.close()