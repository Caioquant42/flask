import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"JSON data loaded successfully. Total items: {len(data)}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}")
        return None

def safe_get(dictionary, key, default=None):
    return dictionary.get(key, default)

def analyze_b3_data(data):
    print("\n--- Starting analysis ---")
    
    # Step 1: Create DataFrame
    print("\nStep 1: Creating DataFrame")
    df = pd.DataFrame([
        {
            'ticker': ticker,
            'currentPrice': safe_get(stock_data, 'currentPrice'),
            'recommendationKey': safe_get(stock_data, 'recommendationKey'),
            'numberOfAnalystOpinions': safe_get(stock_data, 'numberOfAnalystOpinions'),
            '% Distance to Low': safe_get(stock_data, '% Distance to Low', 0),
            '% Distance to Median': safe_get(stock_data, '% Distance to Median', 0),
            '% Distance to High': safe_get(stock_data, '% Distance to High', 0)
        }
        for ticker, stock_data in data.items()
    ])
    print(f"DataFrame created. Shape: {df.shape}")
    print("Columns:", df.columns.tolist())
    print("\nSample data:")
    print(df.head())

    # Step 2: Filter for strong buy stocks
    print("\nStep 2: Filtering for strong buy stocks")
    strong_buy_assets = df[df['recommendationKey'] == 'strong_buy'].copy()
    print(f"Strong buy assets: {len(strong_buy_assets)}")
    if len(strong_buy_assets) > 0:
        print("\nSample strong buy asset:")
        print(strong_buy_assets.iloc[0])
    else:
        print("No strong buy assets found. Returning empty list.")
        return []

    # Step 3: Convert to numeric and handle NaNs
    print("\nStep 3: Converting to numeric and handling NaNs")
    numeric_columns = ['currentPrice', 'numberOfAnalystOpinions', '% Distance to Low', '% Distance to Median', '% Distance to High']
    for col in numeric_columns:
        strong_buy_assets[col] = pd.to_numeric(strong_buy_assets[col], errors='coerce')
    
    strong_buy_assets = strong_buy_assets.dropna(subset=['% Distance to Low', '% Distance to Median', 'numberOfAnalystOpinions'])
    print(f"Assets after handling NaNs: {len(strong_buy_assets)}")
    if len(strong_buy_assets) == 0:
        print("No assets left after handling NaNs. Returning empty list.")
        return []

    # Preserve original data to re-merge later
    original_data = strong_buy_assets.copy()

    # Normalize and calculate combined score
    print("\nNormalizing and calculating combined score")
    columns_to_normalize = ['numberOfAnalystOpinions', '% Distance to Low', '% Distance to Median']
    scaler = MinMaxScaler()
    strong_buy_assets[columns_to_normalize] = scaler.fit_transform(strong_buy_assets[columns_to_normalize])

    strong_buy_assets['combined_score'] = strong_buy_assets[columns_to_normalize].sum(axis=1)
    
    # Add combined score to original data
    original_data['combined_score'] = strong_buy_assets['combined_score']
    
    # Sort based on combined score
    sorted_tickers = original_data.sort_values(by='combined_score', ascending=False)
    sorted_tickers['relevance'] = range(1, len(sorted_tickers) + 1)
    
    # Print final sorted tickers
    print("\nSorted tickers with original values and combined score:")
    print(sorted_tickers.head())

    # Prepare and return the results
    final_tickers = sorted_tickers[sorted_tickers['numberOfAnalystOpinions'] > 1]
    print(f"\nAssets with more than one original analyst opinion: {len(final_tickers)}")

    result = final_tickers.to_dict(orient='records')

    print(f"\nAnalysis complete. Total results: {len(result)}")
    return result

# Main execution
if __name__ == "__main__":
    file_path = 'all_BR_recommendations.json'  # Replace with your actual file path
    data = load_json_data(file_path)
    
    if data:
        results = analyze_b3_data(data)
        print("\nFinal Results:")
        for item in results[:5]:  # Print first 5 results for quick check
            print(item)
    else:
        print("Analysis could not be performed due to data loading error.")