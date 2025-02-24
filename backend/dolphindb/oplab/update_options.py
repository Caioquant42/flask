import sys
import os
# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from backend.apps.utils.dict import TICKERS_DICT
import requests
import csv
from datetime import datetime, timedelta
import dolphindb as ddb
import pandas as pd
import time
import subprocess

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

def fetch_save_and_load_options_data(spot, from_date, to_date, max_retries=5, retry_delay=10):
    headers = {
        'Access-Token': 'a9Ib6XOXdn+ciXZAbUE5W/Rf4ppoD4igNbqA9dw4Qsh607TXEsTV/y8BoLmkqE8G--jnyfnMiGmkZjFR/mwnxbnQ==--NWU4MTUyODcyNjYyOGEyYmY0MWExOTNiZDg5MTg1MDM='
    }

    url = f'https://api.oplab.com.br/v3/market/historical/options/{spot}/{from_date}/{to_date}'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            options_data = response.json()
            print(f"Options Data for {spot} retrieved successfully.")
            
            # Write CSV with column names matching the DolphinDB table schema
            csv_filename = f"{spot}_options.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                header = ['symbol', 'time', 'spot_price', 'spot_symbol', 'type', 'due_date', 'strike', 'premium', 
                          'maturity_type', 'days_to_maturity', 'moneyness', 'delta', 'gamma', 'vega', 'theta', 
                          'rho', 'volatility', 'poe', 'bs']
                csvwriter.writerow(header)
                
                for option in options_data:
                    # Force the 'type' field to be a string upon writing CSV
                    row = [
                        option['symbol'],
                        option['time'],
                        option['spot']['price'],
                        option['spot']['symbol'],
                        str(option['type']),
                        option['due_date'],
                        option['strike'],
                        option['premium'],
                        option['maturity_type'],
                        option['days_to_maturity'],
                        option['moneyness'],
                        option['delta'],
                        option['gamma'],
                        option['vega'],
                        option['theta'],
                        option['rho'],
                        option['volatility'],
                        option['poe'],
                        option['bs']
                    ]
                    csvwriter.writerow(row)
            
            print(f"Data has been written to {csv_filename}")
            return load_options_csv_to_dolphindb(spot)

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {spot}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to retrieve data for {spot} after {max_retries} attempts.")
                return 0, spot

    return 0, spot

def load_options_csv_to_dolphindb(spot):
    csv_filename = f"{spot}_options.csv"
    if not os.path.exists(csv_filename):
        print(f"File {csv_filename} not found. Skipping.")
        return 0, spot

    # Ler o CSV sem conversores específicos para "type"
    df = pd.read_csv(csv_filename, dtype={'type': str})
    print('dtypes após leitura:')
    print(df.dtypes)
    print("Unique values in 'type':", df['type'].unique())

    # Preencher valores nulos na coluna "type" com uma string vazia e converter explicitamente para string
    df['type'] = df['type'].fillna("").apply(lambda x: str(x))
    
    # Verificar novamente os valores únicos, para confirmar a conversão
    print("Unique values in 'type' após conversão:", df['type'].unique())

    # Converter as colunas de data e remover fuso horário, se necessário
    df['time'] = pd.to_datetime(df['time']).dt.tz_localize(None)
    df['due_date'] = pd.to_datetime(df['due_date']).dt.tz_localize(None)

    # Converter colunas numéricas para float
    float_columns = ['spot_price', 'strike', 'premium', 'delta', 'gamma', 'vega', 'theta', 'rho', 'volatility', 'poe', 'bs']
    for col in float_columns:
        df[col] = df[col].astype('float64')
    df['days_to_maturity'] = df['days_to_maturity'].astype('int64')

    # Converter outras colunas para string (confirmação)
    string_columns = ['symbol', 'spot_symbol', 'maturity_type', 'moneyness']
    for col in string_columns:
        df[col] = df[col].astype(str)

    # Se houver alguma conversão adicional para "type", garanta que não haja interferência
    # Neste caso, se os valores já estão corretos (ex.: 'CALL', 'PUT'), mantenha a coluna assim.
    
    # Upload do DataFrame para DolphinDB
    s.upload({'data': df})

    # Script de inserção no DolphinDB usando a coluna "type" original
    script = """
    def insertOptionsData(data) {
        t = loadTable("dfs://oplab", "new_options")
        t.append!(select 
            symbol(symbol) as symbol, 
            time, 
            spot_price, 
            symbol(spot_symbol) as spot_symbol, 
            string(type) as type, 
            due_date, 
            strike, 
            premium, 
            symbol(maturity_type) as maturity_type, 
            days_to_maturity, 
            symbol(moneyness) as moneyness, 
            delta, 
            gamma, 
            vega, 
            theta, 
            rho, 
            volatility, 
            poe, 
            bs 
            from data)
        return size(data)
    }
    insertOptionsData(data)
    """
    
    try:
        result = s.run(script)
        print(f"Options data for {spot} loaded successfully into DolphinDB! Inserted {result} rows.")
        return result, None
    except Exception as e:
        print(f"Error loading data for {spot} into DolphinDB: {e}")
        return 0, spot

if __name__ == "__main__":
    # Set date range for data fetching
    today = datetime.now()
    from_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')
    # Example alternative date range:
    # from_date = '2024-06-30'
    # to_date = '2025-02-01'

    total_inserted = 0
    failed_tickers = []

    for spot in TICKERS_DICT["TOP10"]:
        try:
            rows_inserted, failed_ticker = fetch_save_and_load_options_data(spot, from_date, to_date)
            total_inserted += rows_inserted
            if failed_ticker:
                failed_tickers.append(failed_ticker)
        except Exception as e:
            print(f"Error processing {spot}: {e}")
            failed_tickers.append(spot)

    print(f"Total rows inserted across all symbols: {total_inserted}")
    print(f"Tickers with unavailable information: {failed_tickers}")

    try:
        total_rows = s.run("select count(*) from loadTable('dfs://oplab', 'new_options')")
        print(f"Total rows in the options table: {total_rows}")
    except Exception as e:
        print(f"Error getting total row count: {e}")

    # Save failed tickers to a file
    with open('failed_tickers.txt', 'w') as f:
        for ticker in failed_tickers:
            f.write(f"{ticker}\n")
    print("Failed tickers saved to failed_tickers.txt")

    # After successful operations, execute additional cleaning scripts
    print("Cleaning CSV data")
    import os
    import glob

    # Get the current directory
    current_directory = os.getcwd()

    # Find all .csv files in the current directory
    csv_files = glob.glob(os.path.join(current_directory, "*.csv"))

    # Delete each .csv file
    for file in csv_files:
        try:
            os.remove(file)
            #print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print("All .csv files deleted.")