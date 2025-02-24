import json
import pandas as pd
from typing import List, Dict
import os

def read_json_file(file_path: str) -> List[Dict]:
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return json.load(file)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to decode the file {file_path} with any of the attempted encodings.")

def calculate_ratios(stock: Dict) -> Dict:
    ratio_1y = stock['iv_1y_percentile'] / stock['ewma_1y_percentile'] if stock['ewma_1y_percentile'] != 0 else float('inf')
    ratio_6m = stock['iv_6m_percentile'] / stock['ewma_6m_percentile'] if stock['ewma_6m_percentile'] != 0 else float('inf')
    ratio_current = stock['iv_current'] / stock['ewma_current'] if stock['ewma_current'] != 0 else float('inf')
    
    return {
        'symbol': stock['symbol'],
        'open': stock['open'],
        'high': stock['high'],
        'low': stock['low'],
        'close': stock['close'],
        'variation': stock['variation'],
        'volume': stock['volume'],
        'financial_volume': stock['financial_volume'],
        'ewma_1y_max': stock['ewma_1y_max'],
        'ewma_1y_min': stock['ewma_1y_min'],
        'ewma_1y_percentile': stock['ewma_1y_percentile'],
        'ewma_1y_rank': stock['ewma_1y_rank'],
        'ewma_6m_max': stock['ewma_6m_max'],
        'ewma_6m_min': stock['ewma_6m_min'],
        'ewma_6m_percentile': stock['ewma_6m_percentile'],
        'ewma_6m_rank': stock['ewma_6m_rank'],
        'ewma_current': stock['ewma_current'],
        'iv_1y_max': stock['iv_1y_max'],
        'iv_1y_min': stock['iv_1y_min'],
        'iv_1y_percentile': stock['iv_1y_percentile'],
        'iv_1y_rank': stock['iv_1y_rank'],
        'iv_6m_max': stock['iv_6m_max'],
        'iv_6m_min': stock['iv_6m_min'],
        'iv_6m_percentile': stock['iv_6m_percentile'],
        'iv_6m_rank': stock['iv_6m_rank'],
        'iv_current': stock['iv_current'],
        'middle_term_trend': stock['middle_term_trend'],
        'semi_return_1y': stock['semi_return_1y'],
        'short_term_trend': stock['short_term_trend'],
        'beta_ibov': stock['beta_ibov'],
        'garch11_1y': stock['garch11_1y'],
        'correl_ibov': stock['correl_ibov'],
        'entropy': stock['entropy'],
        'iv_to_ewma_ratio_1y': ratio_1y,
        'iv_to_ewma_ratio_6m': ratio_6m,
        'iv_to_ewma_ratio_current': ratio_current
    }

def analyze_volatility(stocks: List[Dict]) -> List[Dict]:
    analyzed_stocks = [calculate_ratios(stock) for stock in stocks]
    return sorted(analyzed_stocks, key=lambda x: x['iv_to_ewma_ratio_current'], reverse=True)

def save_results(results: List[Dict], output_file: str):
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=2)

def is_valid_stock(stock):
    return (
        stock['iv_to_ewma_ratio_1y'] != float('inf') and
        stock['iv_to_ewma_ratio_6m'] != float('inf') and
        stock['iv_to_ewma_ratio_current'] != float('inf') and
        not pd.isna(stock['iv_to_ewma_ratio_1y']) and
        not pd.isna(stock['iv_to_ewma_ratio_6m']) and
        not pd.isna(stock['iv_to_ewma_ratio_current'])
    )

def main():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the input JSON file
    input_file = os.path.join(current_dir, 'IBOV_stocks.json')
    
    try:
        # Read the input JSON file
        stocks = read_json_file(input_file)
        
        # Analyze volatility
        analyzed_stocks = analyze_volatility(stocks)
        
        # Filter out stocks with infinite or NaN ratios
        valid_stocks = [stock for stock in analyzed_stocks if is_valid_stock(stock)]
        
        # Construct the full path to the output JSON file
        output_file = os.path.join(current_dir, 'volatility_analysis_results.json')
        
        # Save the results
        save_results(valid_stocks, output_file)
        
        print(f"Volatility analysis completed. Results saved to {output_file}")
        print(f"Total stocks analyzed: {len(analyzed_stocks)}")
        print(f"Valid stocks saved: {len(valid_stocks)}")
        print(f"Stocks removed due to infinite or NaN ratios: {len(analyzed_stocks) - len(valid_stocks)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()