import dolphindb as ddb
import pandas as pd
from datetime import datetime, timedelta

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def fetch_vanilla_data(start_date=None, end_date=None):
    # If no dates are provided, use the last 7 days
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2)
    
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
    # Example usage
    # Fetch data for the last 7 days
    df = fetch_vanilla_data()
    
    if df is not None:
        # Display the first few rows
        print(df.head())
        
        # Display basic statistics
        print(df.describe())
        
        # You can now perform further analysis or save the data
        # For example, to save to a CSV file:
        # df.to_csv("vanilla_data.csv", index=False)
        
        # Or to save to an Excel file:
        df.to_excel("vanilla_data.xlsx", index=False)

    # Close the DolphinDB connection
    s.close()