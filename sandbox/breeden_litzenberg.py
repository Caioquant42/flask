import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import moment
import json

# Function to calculate implied probability density using Breeden-Litzenberger formula
def calculate_implied_density(strikes, option_prices, spot_price, risk_free_rate=0.0):
    """
    Calculate the implied probability density using the Breeden-Litzenberger formula.
    :param strikes: Array of strike prices
    :param option_prices: Array of option prices (C(K) or P(K))
    :param spot_price: Current spot price of the underlying asset
    :param risk_free_rate: Risk-free interest rate (default is 0)
    :return: Implied probability density and interpolated strikes
    """
    # Interpolate option prices to create a smooth function
    interp_func = interp1d(strikes, option_prices, kind='cubic', fill_value="extrapolate")
    
    # Create a finer grid of strike prices for interpolation
    fine_strikes = np.linspace(min(strikes), max(strikes), 1000)
    
    # Calculate the second derivative of the option prices (Breeden-Litzenberger formula)
    d2C_dK2 = np.gradient(np.gradient(interp_func(fine_strikes), fine_strikes))
    
    # Implied probability density
    implied_density = np.exp(risk_free_rate * (fine_strikes / spot_price)) * d2C_dK2
    
    return implied_density, fine_strikes

# Function to calculate moments of the implied probability density
def calculate_moments(strikes, density):
    """
    Calculate the moments (mean, variance, skewness, kurtosis) of the implied probability density.
    :param strikes: Array of strike prices
    :param density: Implied probability density
    :return: Dictionary of moments
    """
    # Normalize the density to ensure it sums to 1
    density_normalized = density / np.trapz(density, strikes)
    
    # Calculate mean
    mean = np.trapz(strikes * density_normalized, strikes)
    
    # Calculate variance
    variance = np.trapz((strikes - mean)**2 * density_normalized, strikes)
    
    # Calculate skewness
    skewness = np.trapz((strikes - mean)**3 * density_normalized, strikes) / (variance**1.5)
    
    # Calculate kurtosis
    kurtosis = np.trapz((strikes - mean)**4 * density_normalized, strikes) / (variance**2)
    
    return {
        "mean": mean,
        "variance": variance,
        "skewness": skewness,
        "kurtosis": kurtosis
    }

# Main script
if __name__ == "__main__":
    specific_due_date = "2025-03-21T00:00:00"
    # Load the filtered calls and puts data
    with open("petr4_calls_specific_due_date_data.json", 'r') as f:
        calls_data = json.load(f)
    
    with open("petr4_puts_specific_due_date_data.json", 'r') as f:
        puts_data = json.load(f)
    
    # Convert JSON data to DataFrames
    calls_df = pd.DataFrame(calls_data)
    puts_df = pd.DataFrame(puts_data)
    
    # Extract strike prices and close prices for calls and puts
    call_strikes = calls_df['strike'].values
    call_prices = calls_df['close'].values
    
    put_strikes = puts_df['strike'].values
    put_prices = puts_df['close'].values
    
    # Spot price (assume it's the same for all options)
    spot_price = calls_df['spot_price'].iloc[0]
    
    # Calculate implied probability density for calls and puts
    call_density, call_fine_strikes = calculate_implied_density(call_strikes, call_prices, spot_price)
    put_density, put_fine_strikes = calculate_implied_density(put_strikes, put_prices, spot_price)
    
    # Calculate moments for calls and puts
    call_moments = calculate_moments(call_fine_strikes, call_density)
    put_moments = calculate_moments(put_fine_strikes, put_density)
    
    # Print moments
    print("Call Option Moments:")
    print(call_moments)
    
    print("\nPut Option Moments:")
    print(put_moments)
    
    # Plot the implied probability density
    plt.figure(figsize=(12, 6))
    
    # Plot call density
    plt.plot(call_fine_strikes, call_density, label='Call Implied Density', color='blue', linestyle='--')
    
    # Plot put density
    plt.plot(put_fine_strikes, put_density, label='Put Implied Density', color='red', linestyle='--')
    
    # Add labels and title
    plt.xlabel('Strike Price')
    plt.ylabel('Implied Probability Density')
    plt.title(f"Implied Probability Density for PETR4 (Due Date: {specific_due_date})")
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.show()