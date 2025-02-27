import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def print_top_volatilities(data):
    # Sort data by volatility
    sorted_data = sorted(data, key=lambda x: x['volatility'])
    
    print("Top 5 Lowest Volatility Values:")
    for option in sorted_data[:5]:
        print(f"Volatility: {option['volatility']:.2f}%, Strike: {option['strike']:.2f}, Days to Maturity: {option['days_to_maturity']}")
    
    print("\nTop 5 Highest Volatility Values:")
    for option in sorted_data[-5:][::-1]:
        print(f"Volatility: {option['volatility']:.2f}%, Strike: {option['strike']:.2f}, Days to Maturity: {option['days_to_maturity']}")

def remove_outliers(data):
    volatilities = [option['volatility'] for option in data]
    Q1 = np.percentile(volatilities, 25)
    Q3 = np.percentile(volatilities, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    normal_data = [option for option in data if lower_bound <= option['volatility'] <= upper_bound]
    outliers = [option for option in data if option['volatility'] < lower_bound or option['volatility'] > upper_bound]
    
    return normal_data, outliers

def plot_volatility_surface(data):
    # Remove outliers
    normal_data, outliers = remove_outliers(data)
    
    # Save outliers to JSON
    with open('volatility_outliers.json', 'w') as f:
        json.dump(outliers, f, indent=2)
    print(f"Saved {len(outliers)} outliers to volatility_outliers.json")

    # Extract relevant data
    X = np.array([option['strike'] for option in normal_data])
    Y = np.array([option['days_to_maturity'] for option in normal_data])
    Z = np.array([option['volatility'] for option in normal_data])
    spot_price = normal_data[0]['spot_price']

    # Filter data (strikes within 20% of spot price and maturity <= 100 days)
    mask = (X >= spot_price * 0.8) & (X <= spot_price * 1.2) & (Y <= 300)
    X, Y, Z = X[mask], Y[mask], Z[mask]

    # Create a meshgrid for interpolation
    xi = np.linspace(X.min(), X.max(), 100)
    yi = np.linspace(Y.min(), Y.max(), 100)
    XI, YI = np.meshgrid(xi, yi)

    # Interpolate the volatility values
    ZI = griddata((X, Y), Z, (XI, YI), method='cubic')

    # Create the 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the interpolated surface
    surf = ax.plot_surface(XI, YI, ZI, cmap='viridis', edgecolor='none', alpha=0.8)

    # Plot the actual data points
    scatter = ax.scatter(X, Y, Z, c='red', s=20)

    # Customize the plot
    ax.set_xlabel('Strike')
    ax.set_ylabel('Days to Maturity')
    ax.set_zlabel('Volatility')
    ax.set_title(f'Call Option Volatility Surface for {normal_data[0]["spot_symbol"]}\n'
                 f'(Strikes within 20% of spot price: {spot_price:.2f}, Maturity <= 100 days, Outliers Removed)')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)


    plt.show()

def plot_actual_volatility_surface(data):
    # Remove outliers
    normal_data, outliers = remove_outliers(data)
    
    # Save outliers to JSON
    with open('volatility_outliers.json', 'w') as f:
        json.dump(outliers, f, indent=2)
    print(f"Saved {len(outliers)} outliers to volatility_outliers.json")

    # Extract relevant data
    X = np.array([option['strike'] for option in normal_data])
    Y = np.array([option['days_to_maturity'] for option in normal_data])
    Z = np.array([option['volatility'] for option in normal_data])
    spot_price = normal_data[0]['spot_price']

    # Filter data (strikes within 20% of spot price and maturity <= 100 days)
    mask = (X >= spot_price * 0.80) & (X <= spot_price * 1.2) & (Y <= 300)
    X, Y, Z = X[mask], Y[mask], Z[mask]

    # Create the 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the actual surface using triangulation
    surf = ax.plot_trisurf(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)

    # Plot the actual data points
    scatter = ax.scatter(X, Y, Z, c='black', s=1)

    # Customize the plot
    ax.set_xlabel('Strike')
    ax.set_ylabel('Days to Maturity')
    ax.set_zlabel('Volatility')
    ax.set_title(f'Call Option Volatility Surface for {normal_data[0]["spot_symbol"]}\n'
                 f'(Strikes within 20% of spot price: {spot_price:.2f}, Maturity <= 100 days, Outliers Removed)')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
# Load the JSON data
json_file_path = 'PETR4_last_time_data.json'
option_data = load_json_data(json_file_path)

# Print top volatilities
print_top_volatilities(option_data)
# Plot the volatility surface
plot_actual_volatility_surface(option_data)
plot_volatility_surface(option_data)



