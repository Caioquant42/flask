import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Define the currency pairs
"""
currency_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", "AUDUSD=X", "USDCAD=X", "NZDUSD=X",
                  "EURCHF=X", "EURGBP=X", "GBPJPY=X", "GBPCHF=X", "AUDJPY=X", "AUDCHF=X", "CADJPY=X",
                  "CHFJPY=X", "NZDJPY=X", "NZDCHF=X", "CADCHF=X", "EURCAD=X", "GBPCAD=X", "AUDCAD=X",
                  "EURAUD=X", "GBPAUD=X", "USDMXN=X", "USDTRY=X", "USDZAR=X", "USDNOK=X", "USDSEK=X"]
                  
"""
currency_pairs = ["PETR3.SA","PETR4.SA","VALE3.SA", "BOVA11.SA", "BBAS3.SA", "BBDC4.SA", "COGN3.SA", "MGLU3.SA", "ITUB4.SA", "WEGE3.SA", "EMBR3.SA","PRIO3.SA","ELET6.SA","ELET3.SA"]
# Fetch the daily closing prices for each currency pair
data = {}
for pair in currency_pairs:
    ticker = yf.Ticker(pair)
    df = ticker.history(period="100d", interval="1h")  # Fetching 60 days of 15-minute interval data
    data[pair] = df['Close']
    print(f"Fetched data for {pair}")

# Create a DataFrame with all the currency pairs
df = pd.DataFrame(data)

# Handle missing data by filling NaNs with the previous value (forward fill) or removing rows with NaNs
df = df.fillna(method='ffill').dropna()

# Function to perform the Engle-Granger cointegration test
def check_cointegration(asset1, asset2):
    coint_result = coint(df[asset1], df[asset2])
    return coint_result[1]  # Return the p-value

# Create an empty DataFrame to store the p-values
cointegration_matrix = pd.DataFrame(index=currency_pairs, columns=currency_pairs)

# List to store cointegrated pairs
cointegrated_pairs = []

# Perform the cointegration test for each pair of currency pairs
for i in range(len(currency_pairs)):
    for j in range(i+1, len(currency_pairs)):
        asset1 = currency_pairs[i]
        asset2 = currency_pairs[j]
        p_value = check_cointegration(asset1, asset2)
        cointegration_matrix.loc[asset1, asset2] = p_value
        cointegration_matrix.loc[asset2, asset1] = p_value
        if p_value < 0.05:  # Cointegration significance level
            cointegrated_pairs.append((asset1, asset2, p_value))
        print(f"Cointegration test between {asset1} and {asset2} - p-value: {p_value}")

print("Cointegration matrix:")
print(cointegration_matrix)

print("\nCointegrated Pairs:")
for pair in cointegrated_pairs:
    print(f"{pair[0]} and {pair[1]} - p-value: {pair[2]}")

# Function to calculate the spread and Z-score
def calculate_spread(asset1, asset2):
    X = sm.add_constant(df[asset2])
    model = sm.OLS(df[asset1], X).fit()
    beta = model.params[1]
    spread = df[asset1] - beta * df[asset2]
    return spread

def calculate_zscore(spread):
    mean_spread = np.mean(spread)
    std_spread = np.std(spread)
    zscore = (spread - mean_spread) / std_spread
    return zscore

# Analyze the cointegrated pairs
print("\nTrading Signals:")
long_threshold = -2
short_threshold = 2

for asset1, asset2, p_value in cointegrated_pairs:
    spread = calculate_spread(asset1, asset2)
    zscore = calculate_zscore(spread)

    buy_signals = []
    sell_signals = []
    close_signals = []

    for i in range(len(zscore)):
        if zscore[i] < long_threshold:
            print(f"Go Long: Buy {asset1}, Sell {asset2} at index {i}")
            buy_signals.append(i)
        elif zscore[i] > short_threshold:
            print(f"Go Short: Sell {asset1}, Buy {asset2} at index {i}")
            sell_signals.append(i)
        elif abs(zscore[i]) < 0.5:  # Close position if Z-score is close to mean
            print(f"Close Position at index {i}")
            close_signals.append(i)

    # Plot the spread with buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(spread.index, spread, label='Spread')
    plt.scatter(spread.index[buy_signals], spread[buy_signals], color='green', label='Buy Signal', marker='^', alpha=1)
    plt.scatter(spread.index[sell_signals], spread[sell_signals], color='red', label='Sell Signal', marker='v', alpha=1)
    plt.title(f'Trading Signals for {asset1} and {asset2}')
    plt.xlabel('Date')
    plt.ylabel('Spread')
    plt.legend()
    plt.show()

print("Analysis complete.")
