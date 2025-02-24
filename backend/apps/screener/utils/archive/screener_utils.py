import pandas as pd
from dolphindb import session

def connect_db(ip = "46.202.149.154", port = 8848, user = "admin", passwd = "123456"):
    s = session()
    s.connect(ip, port, user, passwd)
    return s  

# Define a function to calculate RSI
def calculate_rsi(data, window=14):
    # Calculate daily returns
    delta = data['Close'].diff()
    
    # Separate positive and negative gains
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi



def screener_rsi(table_name, file_suffix):

    s = connect_db()
    # Load, execute query, and filter at server-side to reduce data size
    query = f'''
        select Datetime, Symbol, Close 
        from loadTable("dfs://yfs", "{table_name}") 
        where Datetime > 2024.01.01T03:00:00
    '''
    data = s.run(query)

    # Convert result directly into DataFrame
    df = pd.DataFrame(data)

    # Parse 'Datetime' column to datetime object
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    # Use the latest datetime for filtering right away
    most_recent_date = df["Datetime"].max()
    df_most_recent = df[df["Datetime"] == most_recent_date].copy()

    # Calculate RSI for the most recent data slice
    overbought_recent_df = pd.DataFrame()
    oversold_recent_df = pd.DataFrame()
    
    if not df_most_recent.empty:
        df_most_recent.loc[:, "RSI"] = calculate_rsi(df_most_recent)
        
        # Directly create overbought/oversold conditions using efficient vectorized comparison
        overbought_recent_df = df_most_recent[df_most_recent["RSI"] > 70]
        oversold_recent_df = df_most_recent[df_most_recent["RSI"] < 30]

        # Optionally, print a few rows for verification
        print(f"\nMost Recent Overbought Conditions for {table_name}:")
        print(overbought_recent_df.head())

        print(f"\nMost Recent Oversold Conditions for {table_name}:")
        print(oversold_recent_df.head())

        # Save results directly to CSV files
        overbought_recent_df.to_csv(f"overbought_stocks_recent_{file_suffix}.csv", index=False)
        oversold_recent_df.to_csv(f"oversold_stocks_recent_{file_suffix}.csv", index=False)

        print(f"\nDataFrames saved successfully for {table_name} to 'overbought_stocks_recent_{file_suffix}.csv' and 'oversold_stocks_recent_{file_suffix}.csv'")
    else:
        print(f"No data available for the most recent date in {table_name}.")

    return overbought_recent_df, oversold_recent_df