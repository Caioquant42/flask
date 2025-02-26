import yfinance as yf
import matplotlib.pyplot as plt

# Downloading the dividend data for VALE3.SA
ticker = 'VALE3.SA'
stock = yf.Ticker(ticker)
dividends = stock.dividends

# Creating the plot with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Plotting the histogram
ax1.hist(dividends, bins=10, edgecolor='black')
ax1.set_title(f'Histogram of Dividends for {ticker}')
ax1.set_xlabel('Dividend Amount')
ax1.set_ylabel('Frequency')
ax1.grid(True)

# Plotting the amount paid over time
ax2.plot(dividends.index, dividends.values, marker='o', linestyle='-')
ax2.set_title(f'Amount Paid Over Time for {ticker}')
ax2.set_xlabel('Date')
ax2.set_ylabel('Dividend Amount')
ax2.grid(True)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
