import pandas as pd
import numpy as np
from dolphindb import session

def connect_db(ip="46.202.149.154", port=8848, user="admin", passwd="123456"):
    s = session()
    s.connect(ip, port, user, passwd)
    return s  

def ewma(underlying_df, t_intervals, decay=0.94):
    if not isinstance(t_intervals, int):
        raise ValueError("t_intervals should be an integer")

    # Calculate logarithmic returns
    underlying_df['log_return'] = np.log(underlying_df['Close'] / underlying_df['Close'].shift(1))
    
    # Calculate EWMA volatility with given parameters
    ewma_volatility = underlying_df['log_return'].ewm(span=t_intervals, min_periods=t_intervals).std() * np.sqrt(252)
    
    # Add EWMA volatility to DataFrame
    underlying_df['EWMA'] = ewma_volatility

    return underlying_df

def screener_ewma(table_name="stockdata_1d", file_suffix="1d"):
    # Connect to the DolphinDB server
    s = connect_db()

    # Query the data required for EWMA calculation
    query = f'''
        select Datetime, Symbol, Close 
        from loadTable("dfs://yfs", "{table_name}") 
        where Datetime > 2021.01.01T03:00:00
    '''
    data = s.run(query)

    # Convert the result directly into a DataFrame
    df = pd.DataFrame(data)

    # Parse the 'Datetime' column as a datetime object
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    if not df.empty:
        # Apply EWMA calculation to each Symbol group
        df = df.groupby('Symbol', group_keys=False).apply(lambda x: ewma(x, t_intervals=21, decay=0.94))
        df.dropna(inplace=True)  # Ensure no NaNs persist

        # Calculate quartiles for each stock and assign volatility keys
        def classify_by_volatility(group):
            if group['EWMA'].isnull().all():
                return group

            first_quartile = group['EWMA'].quantile(0.25)
            third_quartile = group['EWMA'].quantile(0.75)
            group['first_quartile'] = first_quartile
            group['third_quartile'] = third_quartile
            
            group.loc[group['EWMA'] > third_quartile, 'volatility_key'] = 'high'
            group.loc[group['EWMA'] < first_quartile, 'volatility_key'] = 'low'
            return group
        
        df_classified = df.groupby('Symbol', group_keys=False).apply(classify_by_volatility)

        # Consider only the most recent data point for each symbol
        most_recent_date = df_classified["Datetime"].max()
        df_most_recent = df_classified[df_classified["Datetime"] == most_recent_date]

        # Confirm 'volatility_key' existence in most recent entries
        if 'volatility_key' not in df_most_recent.columns:
            print("No volatility classification applied.")
            return pd.DataFrame(), pd.DataFrame()

        # Split into high and low volatility groups
        highvol_df = df_most_recent[df_most_recent['volatility_key'] == 'high']
        lowvol_df = df_most_recent[df_most_recent['volatility_key'] == 'low']

        # Sort DataFrames by EWMA in descending order
        highvol_df = highvol_df.sort_values(by='EWMA', ascending=False)
        lowvol_df = lowvol_df.sort_values(by='EWMA', ascending=False)

        # Save results directly as CSV files with quartiles
        highvol_df.to_csv(f"high_volatility_stocks_recent_{file_suffix}.csv", index=False)
        lowvol_df.to_csv(f"low_volatility_stocks_recent_{file_suffix}.csv", index=False)

        return highvol_df, lowvol_df

    else:
        print(f"No data available for volatility calculation in {table_name}.")

    return pd.DataFrame(), pd.DataFrame()

# Usage example:
# high_vol, low_vol = screener_ewma()