# -*- coding: utf-8 -*-
import requests
import csv
from datetime import datetime, timedelta
import dolphindb as ddb
import pandas as pd
import time
import subprocess
import glob
import sys
import os
# Add this block at the beginning of the file
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    from utils.dictionary import TICKERS_DICT
else:
    from .dictionary import TICKERS_DICT


# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

# Create the new "zommalab" database and "vanilla" table in DolphinDB with range partitioning
create_db_and_table_script = """
def createZommalabAndVanillaTable() {
    if(!existsDatabase("dfs://zommalab")) {
        // Create the zommalab database with RANGE partitioning
        db = database("dfs://zommalab", RANGE, 2018.01.01..2030.12.31)
        print("zommalab database created successfully with RANGE partitioning")
    } else {
        db = database("dfs://zommalab")
        print("zommalab database already exists")
    }

    if(existsTable("dfs://zommalab", "vanilla")) {
        print("vanilla table already exists in zommalab database")
        return
    }

    schema = table(
        1:0, 
        ["symbol", "time", "spot_price", "spot_symbol", "option_type", "due_date", "strike", "premium",
         "maturity_type", "days_to_maturity", "moneyness", "delta", "gamma", "vega", "theta",
         "rho", "volatility", "poe", "bs"],
        [SYMBOL, TIMESTAMP, DOUBLE, SYMBOL, SYMBOL, DATE, DOUBLE, DOUBLE,
         SYMBOL, INT, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE,
         DOUBLE, DOUBLE, DOUBLE, DOUBLE]
    )
    
    // Create partitioned table with RANGE on time column
    db.createPartitionedTable(
        table=schema, 
        tableName="vanilla", 
        partitionColumns="time"
    )
    print("vanilla table created successfully in zommalab database with RANGE partitioning on time")
}
createZommalabAndVanillaTable()
"""

try:
    s.run(create_db_and_table_script)
    print("zommalab database and vanilla table setup completed with RANGE partitioning.")
except Exception as e:
    print(f"Error setting up zommalab database and vanilla table: {e}")
    sys.exit(1)


def fetch_save_and_load_options_data(spot, from_date, to_date, s, max_retries=5, retry_delay=10):
    """
    Fetches options data from the OPLAB API, saves it to a CSV file, and loads it into DolphinDB.

    Args:
        spot (str): The ticker symbol for the spot asset (e.g., "PETR4").
        from_date (str): The start date for data retrieval (YYYY-MM-DD).
        to_date (str): The end date for data retrieval (YYYY-MM-DD).
        s (ddb.session): The DolphinDB session object.
        max_retries (int): Maximum number of retries for API requests. Default is 5.
        retry_delay (int): Delay in seconds between retries. Default is 10.

    Returns:
        tuple: A tuple containing the number of rows inserted and the ticker symbol.
               Returns (0, spot) if the process fails after multiple retries.
    """
    headers = {
        'Access-Token': 'NV0MENA0YZ9bgJA/Wf+F+tROe+eYX9SpUBuhmxNNkeIVuQKf+/wtVkYT4gGo0uvg--tTAJG2No3ZgblMOUkEql4g==--NzllMzczOTg2ZWI5ZmJlN2U2MjBmMDA3NGIxODcxOWQ='
    }

    url = f'https://api.oplab.com.br/v3/market/historical/options/{spot}/{from_date}/{to_date}'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX, 5XX)

            options_data = response.json()
            print(f"Options Data for {spot} retrieved successfully.")
            
            # Write CSV with column names matching the DolphinDB table schema
            csv_filename = f"{spot}_options.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                header = ['symbol', 'time', 'spot_price', 'spot_symbol', 'option_type', 'due_date', 'strike', 'premium', 
                          'maturity_type', 'days_to_maturity', 'moneyness', 'delta', 'gamma', 'vega', 'theta', 
                          'rho', 'volatility', 'poe', 'bs']
                csvwriter.writerow(header)
                
                for option in options_data:
                    # Determine option type based on delta. This is a common practice, but consider other factors
                    # or data fields if the delta is not always reliable.
                    option_type = 'CALL' if option['delta'] >= 0 else 'PUT'
                    
                    row = [
                        option['symbol'],
                        option['time'],
                        option['spot']['price'],
                        option['spot']['symbol'],
                        option_type,  # Use the determined option type
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
            return load_options_csv_to_dolphindb(spot, s)  # Pass 's' here

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {spot}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to retrieve data for {spot} after {max_retries} attempts.")
                return 0, spot

    return 0, spot

def load_options_csv_to_dolphindb(spot, s):
    csv_filename = f"{spot}_options.csv"
    print(f"Tentando carregar dados de: {csv_filename}")

    if not os.path.exists(csv_filename):
        print(f"Arquivo {csv_filename} não encontrado. Pulando.")
        return 0, spot

    try:
        # Leitura inicial do CSV
        df = pd.read_csv(csv_filename, dtype={'option_type': str})
        print(f"Número de linhas no arquivo CSV original: {len(df)}")
        print("Valores únicos em 'option_type':", df['option_type'].unique())

        # Conversion and error handling for 'time'
        print("Converting 'time' column to datetime...")
        df['time'] = pd.to_datetime(df['time'], format='ISO8601', errors='coerce')
        df['time'] = df['time'].dt.tz_localize(None)
        invalid_times = df['time'].isna().sum()
        print(f"Invalid 'time' dates: {invalid_times}")

        # Conversion and error handling for 'due_date'
        print("Converting 'due_date' column to datetime...")
        df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
        df['due_date'] = df['due_date'].dt.tz_localize(None)
        invalid_due_dates = df['due_date'].isna().sum()
        print(f"Invalid 'due_date' dates: {invalid_due_dates}")

        # Drop rows with invalid dates
        df = df.dropna(subset=['time', 'due_date'])

        # Filter 'time' to be within the partition range (2018-01-01 to 2030-12-31)
        start_date = pd.Timestamp('2018-01-01')
        end_date = pd.Timestamp('2030-12-31')
        df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]

        # Conversão de colunas numéricas
        float_columns = ['spot_price', 'strike', 'premium', 'delta', 'gamma', 'vega', 'theta', 'rho', 'volatility', 'poe', 'bs']
        for col in float_columns:
            if col in df.columns:
                print(f"Convertendo coluna '{col}' para float...")
                df[col] = pd.to_numeric(df[col], errors='coerce')
                na_count = df[col].isna().sum()
                print(f"Valores NaN em '{col}' após conversão: {na_count}")
            else:
                print(f"Coluna {col} não encontrada no arquivo CSV.")

        # Conversão de 'days_to_maturity' para inteiro
        if 'days_to_maturity' in df.columns:
            print("Convertendo coluna 'days_to_maturity' para inteiro...")
            df['days_to_maturity'] = pd.to_numeric(df['days_to_maturity'], errors='coerce').astype('Int64')
            na_count = df['days_to_maturity'].isna().sum()
            print(f"Valores NaN em 'days_to_maturity' após conversão: {na_count}")
        else:
            print("Coluna 'days_to_maturity' não encontrada no arquivo CSV.")

        # Conversão de colunas de string
        string_columns = ['symbol', 'spot_symbol', 'maturity_type', 'moneyness']
        for col in string_columns:
            if col in df.columns:
                print(f"Convertendo coluna '{col}' para string...")
                df[col] = df[col].astype(str)
            else:
                print(f"Coluna {col} não encontrada no arquivo CSV.")

        # Formatação das datas para DolphinDB
        print("Formatando colunas de data para o formato DolphinDB...")
        df['time'] = df['time'].dt.strftime('%Y.%m.%dT%H:%M:%S.%f')[:-3]
        df['due_date'] = df['due_date'].dt.strftime('%Y.%m.%d')

        print(f"Número final de linhas no DataFrame: {len(df)}")

        # Verificação se o DataFrame está vazio
        if df.empty:
            print("O DataFrame está vazio após o processamento. Nenhum dado para inserir.")
            return 0, spot

        # Envio dos dados para DolphinDB
        print("Enviando dados para DolphinDB...")
        s.upload({'data': df})

        # Script DolphinDB para inserção dos dados
        script = """
        def insertOptionsData(data) {
            t = loadTable("dfs://zommalab", "vanilla")
            try {
                inserted = t.append!(select 
                    symbol(symbol) as symbol, 
                    timestamp(time) as time, 
                    spot_price, 
                    symbol(spot_symbol) as spot_symbol, 
                    symbol(option_type) as option_type,
                    date(due_date) as due_date, 
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
                return inserted
            } catch(ex) {
                print("Falha na inserção:", ex)
                return 0
            }
        }
        insertOptionsData(data)
        """
        
        # Execução do script DolphinDB
        print("Executando script DolphinDB...")
        result = s.run(script)
        print(f"Dados de opções para {spot} carregados com sucesso no DolphinDB! Inseridas {result} linhas.")
        return result, None

    except Exception as e:
        print(f"Erro ao processar o arquivo CSV {csv_filename}: {e}")
        return 0, spot


def remove_duplicates(s):
    script = """
    def removeDuplicates() {
        vanillaTable = loadTable("dfs://zommalab", "vanilla")
        
        // Find duplicates based on symbol, time, and option_type
        duplicates = select symbol, time, option_type, count(*) as cnt from vanillaTable 
                     group by symbol, time, option_type having count(*) > 1
        
        if (size(duplicates) > 0) {
            // Select unique records
            uniqueData = select 
                symbol, time, first(spot_price) as spot_price, first(spot_symbol) as spot_symbol,
                option_type, first(due_date) as due_date, first(strike) as strike,
                first(premium) as premium, first(maturity_type) as maturity_type,
                first(days_to_maturity) as days_to_maturity, first(moneyness) as moneyness,
                first(delta) as delta, first(gamma) as gamma, first(vega) as vega,
                first(theta) as theta, first(rho) as rho, first(volatility) as volatility,
                first(poe) as poe, first(bs) as bs
            from vanillaTable
            group by symbol, time, option_type
            
            // Create a new partitioned table with unique data
            db = database("dfs://zommalab")
            if(existsTable("dfs://zommalab", "vanilla")){
                dropTable(db, "vanilla")  // Drop the old table
            }
            newTable = db.createPartitionedTable(table(uniqueData), "vanilla", "time")
            newTable.append!(uniqueData)
        }
        
        return size(duplicates)
    }

    removeDuplicates()
    """
    
    # Run the script to remove duplicates
    num_duplicates_removed = s.run(script)
    if num_duplicates_removed == 0:
        print("No duplicates found in the vanilla table.")
    else:
        print(f"Removed {num_duplicates_removed} duplicate entries from the vanilla table.")

# Call this function after uploading data for all symbols


if __name__ == "__main__":
    # Defina from_date e to_date
    today = datetime.now()
    from_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    total_inserted = 0
    failed_tickers = []

    # Estabelecendo a conexão com o DolphinDB
    s = ddb.session()
    try:
        s.connect("46.202.149.154", 8848, "admin", "123456")  # Use o endereço IP correto aqui
        print("Conexão com DolphinDB estabelecida com sucesso.")

        # Teste de conexão
        try:
            version = s.run("version()")
            print(f"Versão do DolphinDB: {version}")
        except Exception as e:
            print(f"Erro ao testar a conexão com DolphinDB: {e}")
            sys.exit(1)

        for spot in TICKERS_DICT["TOP10"]:
            try:
                print(f"Iniciando o processamento para o ticker: {spot}")
                rows_inserted, failed_ticker = fetch_save_and_load_options_data(spot, from_date, to_date, s)
                if rows_inserted > 0:
                    total_inserted += rows_inserted
                    print(f"Inserção bem-sucedida para {spot}. Total inserido: {total_inserted}")
                else:
                    failed_tickers.append(spot)
                    print(f"Falha na inserção para {spot}. Rows inserted: {rows_inserted}")
            except Exception as e:
                print(f"Erro ao processar {spot}: {e}")
                failed_tickers.append(spot)
            finally:
                print(f"Processamento para {spot} concluído.")

        # Após o loop, remova duplicatas e imprima os resultados
        try:
            remove_duplicates(s)
            print("Remoção de duplicatas concluída.")
        except Exception as e:
            print(f"Erro ao remover duplicatas: {e}")

        # Verifique se a tabela existe antes de contar as linhas
        table_exists = s.run("existsTable('dfs://zommalab', 'vanilla')")
        if table_exists:
            try:
                total_rows = s.run("select count(*) from loadTable('dfs://zommalab', 'vanilla')")
                print(f"Total de linhas na tabela vanilla após processamento: {total_rows}")
            except Exception as e:
                print(f"Erro ao obter contagem total de linhas: {e}")
        else:
            print("A tabela vanilla não existe.")

    except Exception as e:
        print(f"Erro geral no script: {e}")
    finally:
        s.close()
        print("Conexão com DolphinDB fechada.")

    # Save failed tickers to a file
    with open('failed_tickers.txt', 'w') as f:
        for ticker in failed_tickers:
            f.write(f"{ticker}\n")
    print("Failed tickers saved to failed_tickers.txt")

    # After successful operations, execute additional cleaning scripts
    print("Cleaning CSV data")

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

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
    print(f"Code last executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")