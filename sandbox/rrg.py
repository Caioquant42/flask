import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download historical data
tickers = ['PETR4.SA', 'VALE3.SA', 'BOVA11.SA', 'COGN3.SA', 'SUZB5.SA']
data = yf.download(tickers, start='2024-02-27', end='2025-02-27')['Close']

# Calculate Relative Strength (RS) and RS-Ratio
def calculate_rs_ratio(security, benchmark):
    rs = security / benchmark
    rs_ratio = rs / rs.rolling(window=14).mean()  # Smoothed RS
    return rs_ratio

# Calculate RS-Momentum
def calculate_rs_momentum(rs_ratio):
    # Adjust momentum to float around 1
    rs_momentum = (rs_ratio.pct_change(periods=1) + 1)  # Shift to center around 1
    return rs_momentum

# Calculate RS-Ratio and RS-Momentum for each security
rs_ratios = {}
rs_momentums = {}
for ticker in tickers[:-1]:  # Exclude benchmark from this loop
    rs_ratios[ticker] = calculate_rs_ratio(data[ticker], data['BOVA11.SA'])
    rs_momentums[ticker] = calculate_rs_momentum(rs_ratios[ticker])
    
    # Print the last 5 RS-Ratio and RS-Momentum values
    print(f"\n{ticker} - Last 5 RS-Ratio values:")
    print(rs_ratios[ticker].dropna().tail(5))
    
    print(f"\n{ticker} - Last 5 RS-Momentum values:")
    print(rs_momentums[ticker].dropna().tail(5))

# Plot RRG
plt.figure(figsize=(10, 10))
for ticker in tickers[:-1]:
    # Plot last 5 data points with interconnected lines
    plt.plot(rs_ratios[ticker][-5:], rs_momentums[ticker][-5:], marker='o', label=f'{ticker} Last 5', alpha=0.7)
    
    # Add an arrow for the last data point
    plt.arrow(rs_ratios[ticker].iloc[-2], rs_momentums[ticker].iloc[-2],
              rs_ratios[ticker].iloc[-1] - rs_ratios[ticker].iloc[-2],
              rs_momentums[ticker].iloc[-1] - rs_momentums[ticker].iloc[-2],
              head_width=0.005, head_length=0.01, fc='red', ec='red')

# Add annotations
for ticker in tickers[:-1]:
    plt.annotate(ticker, (rs_ratios[ticker].iloc[-1], rs_momentums[ticker].iloc[-1]))

# Add quadrants and labels
plt.axhline(1, color='black', linewidth=0.5)
plt.axvline(1, color='black', linewidth=0.5)
plt.title('Relative Rotation Graph (RRG)')
plt.xlabel('RS-Ratio')
plt.ylabel('RS-Momentum')
plt.legend()
plt.grid(True)
plt.show()