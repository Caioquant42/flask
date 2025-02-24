import sys
import os
import json
import time
import pandas as pd
import yfinance as yf

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from apps.utils.dict import TICKERS_DICT

tickers = TICKERS_DICT.get('TODOS', [])

class YData:
    def __init__(self, ticker_symbol, interval='1d', period='max', world=False, start_date=None, end_date=None):
        self.ticker_symbol = ticker_symbol
        self.interval = interval
        self.period = period
        self.world = world
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = self._add_sa_to_tickers(self.ticker_symbol)
        self.stock_data = yf.Ticker(self.ticker)

    def _add_sa_to_tickers(self, tickers):
        return f"{tickers}.SA" if not self.world else tickers

    def get_fundamental_data_summary(self):
        try:
            info = self.stock_data.info
            
            # Define the specific fields we want to fetch
            desired_fields = [
                "currentPrice", "targetHighPrice", "targetLowPrice", "targetMeanPrice",
                "targetMedianPrice", "recommendationMean", "recommendationKey",
                "numberOfAnalystOpinions", "averageAnalystRating"
            ]            
            # Create a dictionary with only the desired fields
            filtered_info = {field: info.get(field) for field in desired_fields if field in info}
            
            # Calculate additional metrics
            current_price = filtered_info.get('currentPrice')
            if current_price is not None and current_price != 0:
                filtered_info['% Distance to Mean'] = ((filtered_info.get('targetMeanPrice', 0) - current_price) / current_price) * 100
                filtered_info['% Distance to Median'] = ((filtered_info.get('targetMedianPrice', 0) - current_price) / current_price) * 100
                filtered_info['% Distance to Low'] = ((filtered_info.get('targetLowPrice', 0) - current_price) / current_price) * 100
                filtered_info['% Distance to High'] = ((filtered_info.get('targetHighPrice', 0) - current_price) / current_price) * 100
            else:
                filtered_info['% Distance to Mean'] = None
                filtered_info['% Distance to Median'] = None
                filtered_info['% Distance to Low'] = None
                filtered_info['% Distance to High'] = None
            
            return filtered_info

        except Exception as e:
            print(f"Error retrieving fundamental data summary for {self.ticker}: {e}")
            return None

def save_all_fundamental_data_to_json(filename):
    all_data = {}
    for ticker in tickers:
        ydata = YData(ticker)
        ticker_data = ydata.get_fundamental_data_summary()
        if ticker_data:
            all_data[ticker] = ticker_data

        print(f"{ticker} loaded successfully")
        time.sleep(1)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        
        print(f"All fundamental data summaries saved to {filename}")
    
    except Exception as e:
        print(f"Error saving all fundamental data summaries to {filename}: {e}")

def main():
    filename = "all_BR_recommendations.json"
    save_all_fundamental_data_to_json(filename)

if __name__ == "__main__":
    main()