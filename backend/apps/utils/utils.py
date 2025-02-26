import yfinance as yf  # For fetching stock data and fundamental information
import pandas as pd  # For handling data in DataFrame format
import numpy as np  # For numerical operations, specifically np.log1p for log returns

"""
Main Classes that will be used along the project, this mainly include the classes for fetching data from API's (Yfinance,Coingecko,AlphaVantage and others)

"""
# Yfinance
class YData:
    def __init__(self, ticker_symbol, interval='1d', period='max', world=False, start_date=None, end_date=None):
        self.ticker_symbol = ticker_symbol
        self.interval = interval
        self.period = period
        self.world = world
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = self._add_sa_to_tickers(self.ticker_symbol) # Initialize ticker here
        self.stock_data = yf.Ticker(self.ticker) # Initialize yf.Ticker once


    def _add_sa_to_tickers(self, tickers):
        return f"{tickers}.SA" if not self.world else tickers

    def get_stock_data(self):
        # Debug statement to check the parameters before fetching data
        print(f"Fetching data for ticker: {self.ticker}, start: {self.start_date}, end: {self.end_date}")

        # Fetch historical data based on date range or period
        if self.start_date and self.end_date:
            historical_data = self.stock_data.history(start=self.start_date, end=self.end_date, interval=self.interval)
        else:
            historical_data = self.stock_data.history(period=self.period, interval=self.interval)

        if historical_data.empty:
            print(f"No historical data found for {self.ticker}. Check the ticker and date range.")
            return pd.DataFrame()  # Return empty dataframe to avoid errors

        # Rename columns for clarity
        rename_cols = {
            'Open': 'Abertura', 
            'High': 'Máxima', 
            'Low': 'Mínima', 
            'Close': 'Fechamento', 
            'Volume': 'Volume', 
            'Dividends': 'Dividendos', 
            'Stock Splits': 'Desdobramentos'
        }
        historical_data.rename(columns=rename_cols, inplace=True)

        # Calculate returns
        historical_data['simple_return'] = historical_data['Fechamento'].pct_change()
        historical_data['log_return'] = np.log1p(historical_data['simple_return'])
        historical_data.dropna(subset=['simple_return', 'log_return'], inplace=True)

        return historical_data

    def get_fundamental_data(self, info_keys=None):
       """Retrieves fundamental data.

       Args:
           info_keys: A list of keys to retrieve from the info dictionary.
                      If None, retrieves all available keys.

       Returns:
           A dictionary containing the requested fundamental data or
           None if no data is found or if there's an error.
       """
       try:
           info = self.stock_data.info
           if info_keys is None:
               return info
           else:
               return {key: info.get(key) for key in info_keys if key in info}
       except Exception as e:
           print(f"Error retrieving fundamental data for {self.ticker}: {e}")
           return None
       
    def get_fundamental_data_summary(self):
        """
        Retrieves and summarizes fundamental data in a DataFrame.

        Returns:
            A pandas DataFrame summarizing the fundamental data, or None if an error occurs.
        """
        try:
            info = self.stock_data.info
            
            # Convert the info dictionary to a DataFrame
            df_info = pd.DataFrame.from_dict(info, orient='index', columns=['Value'])
            df_info.index.name = 'Metric'
            return df_info

        except Exception as e:
            print(f"Error retrieving fundamental data summary for {self.ticker}: {e}")
            return None
       
    def save_fundamental_data_summary_to_txt(self, filename="fundamental_data_summary.txt"):
        """
        Retrieves fundamental data summary and saves it to a text file.

        Args:
            filename: The name of the file to save the data to.
        """

        try:
            df_summary = self.get_fundamental_data_summary()

            if df_summary is not None:
                with open(filename, 'w', encoding='utf-8') as f:  # Abre o arquivo em modo de escrita ('w') com codificação UTF-8
                    f.write(df_summary.to_string())  # Escreve o DataFrame no arquivo
                print(f"Fundamental data summary saved to {filename}")
            
        except Exception as e:
            print(f"Error saving fundamental data summary to {filename}: {e}")

    ''' Example of usage
        ydata = YData("PETR4")
        ydata.save_fundamental_data_summary_to_txt() # Salva no arquivo padrão "fundamental_data_summary.txt"

        # Para salvar em um arquivo diferente:
        ydata.save_fundamental_data_summary_to_txt(filename="petr4_summary.txt")"'''
    
    def check_interval(self):
        valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        if self.interval not in valid_intervals:
            raise ValueError("Intervalo não disponível, opções válidas: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")
        if self.period == 'max':
            if self.interval == '1h':
                self.period = '730d'
            elif self.interval == '1m':
                self.period = '7d'
            elif self.interval in ['1d', '1wk', '1mo', '3mo']:
                self.period = 'max'
            elif self.interval in ['90m', '30m', '15m', '5m']:
                self.period = '60d'
            else:
                raise ValueError("Erro: Período Inválido.")
            return self.period
        else:
            return self.period







