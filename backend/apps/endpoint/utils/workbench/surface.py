import dolphindb as ddb
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def fetch_latest_volatility_data(symbol='PETR4'):
    script = f"""
    def fetchLatestVolatilityData(symbol) {{
        t = loadTable("dfs://zommalab", "vanilla")
        latest_time = exec max(time) from t where symbol = symbol
        data = select 
            symbol, time, spot_price, spot_symbol, option_type, due_date, 
            strike, days_to_maturity, volatility
        from t 
        where symbol = symbol and time = latest_time and option_type = 'CALL'
        
        // Filter strikes within 50% of spot price and days to maturity <= 300
        return select * from data 
               where strike >= spot_price * 0.5 and strike <= spot_price * 1.5
               and days_to_maturity <= 300
    }}
    fetchLatestVolatilityData("{symbol}")
    """

    try:
        # Execute the script and fetch the data
        data = s.run(script)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        print(f"Fetched {len(df)} rows for {symbol} from the vanilla table (strikes within 50% of spot price, maturity <= 300 days).")
        return df
    except Exception as e:
        print(f"Error fetching data from DolphinDB: {e}")
        return None

def plot_volatility_surface(df):
    # Prepare the data
    X = df['strike'].values
    Y = df['days_to_maturity'].values
    Z = df['volatility'].values

    # Create a meshgrid
    xi = np.linspace(X.min(), X.max(), 100)
    yi = np.linspace(Y.min(), Y.max(), 100)
    XI, YI = np.meshgrid(xi, yi)

    # Interpolate the volatility values
    ZI = griddata((X, Y), Z, (XI, YI), method='cubic')

    # Create the 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(XI, YI, ZI, cmap='viridis', edgecolor='none', alpha=0.8)

    # Plot the actual data points
    scatter = ax.scatter(X, Y, Z, c='red', s=20)

    # Customize the plot
    ax.set_xlabel('Strike')
    ax.set_ylabel('Days to Maturity')
    ax.set_zlabel('Volatility')
    ax.set_title(f'Call Option Volatility Surface for {df["symbol"].iloc[0]}\n'
                 f'(Strikes within 50% of spot price: {df["spot_price"].iloc[0]:.2f}, Maturity <= 300 days)')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

    plt.show()

if __name__ == "__main__":
    # Fetch the latest data for PETR4
    df = fetch_latest_volatility_data('PETR4')
    
    if df is not None and not df.empty:
        print("Data snapshot:")
        print(df.head())
        print(f"\nSpot price: {df['spot_price'].iloc[0]:.2f}")
        print(f"Strike range: {df['strike'].min():.2f} to {df['strike'].max():.2f}")
        print(f"Days to maturity range: {df['days_to_maturity'].min():.0f} to {df['days_to_maturity'].max():.0f}")
        
        # Plot the volatility surface
        plot_volatility_surface(df)
    else:
        print("No data available for plotting.")

    # Close the DolphinDB connection
    s.close()