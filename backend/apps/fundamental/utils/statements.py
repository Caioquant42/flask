import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import unidecode
import os
import sys
import time

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from apps.utils.dict import TICKERS_DICT

tickers = TICKERS_DICT.get('IBOV', [])

def fetch_statements(ticker):
    url = f'https://www.dadosdemercado.com.br/acoes/{ticker}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table', class_='normal-table')

    ticker_data = {}

    for table_index, table in enumerate(tables, start=1):
        # Skip the second table
        if table_index == 2:
            continue

        # Determine table name based on index
        table_name = {
            1: 'Indicators',
            3: 'BalanceSheet',
            4: 'AnnualResults',
            5: 'TriResults',
            6: 'CashFlow'
        }.get(table_index, f"Table_{table_index}")

        # Extract headers
        headers = [unidecode.unidecode(th.text.strip()) for th in table.find('thead').find_all('th')]

        # Extract row data
        rows_data = []
        for row in table.find('tbody').find_all('tr'):
            row_data = [unidecode.unidecode(td.text.strip()) for td in row.find_all('td')]
            rows_data.append(row_data)
        
        # Create DataFrame
        df = pd.DataFrame(rows_data, columns=headers)
        
        # Convert DataFrame to dictionary
        data_dict = df.to_dict(orient='records')

        ticker_data[table_name] = data_dict

    return ticker_data

def main():
    all_tickers_data = {}

    for ticker in tickers:
        print(f"Fetching {ticker} fundamental data.")
        all_tickers_data[ticker] = fetch_statements(ticker)
        time.sleep(3)

    # Get the absolute path of the script directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = 'statements_all.json'
    file_path = os.path.join(current_directory, filename)  # Create full path

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_tickers_data, f, ensure_ascii=False, indent=4)

    print(f"All data saved to {file_path}")

if __name__ == "__main__":
    main()
