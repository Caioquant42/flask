from apps.utils.utils import YData
import pandas as pd
import time

def get_analyst_information(tickers, world = False):
    """Retrieves analyst information for a list of tickers.

    Args:
        tickers: A list of ticker symbols.

    Returns:
        A pandas DataFrame containing analyst information, or None if an error occurs or no data is found.
    """
    try:
        data = []
        ignored_tickers = []
        total_tickers = len(tickers)
        processed_tickers = 0

        for ticker in tickers:
            if world == True:
                ydata = YData(ticker,world = True)
                time.sleep(4)  # Add a 5-second delay to avoid overrequest
            else:
                ydata = YData(ticker)  # Add this line to handle the case when USA is False
                time.sleep(2)  # Add a 5-second delay to avoid overrequest
            try:
                info = ydata.get_fundamental_data(info_keys=[
                    'currentPrice', 'recommendationKey', 'numberOfAnalystOpinions',
                    'targetMedianPrice', 'targetMeanPrice', 'targetLowPrice', 'targetHighPrice'
                ])

                if info and info.get('recommendationKey', '').lower() != 'none':
                    info['Ticker'] = ticker

                    current_price = info.get('currentPrice')
                    if current_price is not None and current_price != 0:
                        info['% Distance to Median'] = ((info.get('targetMedianPrice', 0) - current_price) / current_price) * 100
                        info['% Distance to Low'] = ((info.get('targetLowPrice', 0) - current_price) / current_price) * 100
                        info['% Distance to High'] = ((info.get('targetHighPrice', 0) - current_price) / current_price) * 100
                    else:
                        info['% Distance to Median'] = None
                        info['% Distance to Low'] = None
                        info['% Distance to High'] = None
                    
                    data.append(info)
                    processed_tickers += 1
                    print(f"Successfully processed: {ticker}")
                else:
                    ignored_tickers.append(ticker)
                    print(f"Ignored: {ticker} (No data or 'none' recommendation)")

            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing data for {ticker}: {e}")
                ignored_tickers.append(ticker)

        if data:
            df = pd.DataFrame(data)
            df.fillna(0, inplace=True)

            if 'Ticker' in df.columns:
                cols = ['Ticker'] + [col for col in df.columns if col != 'Ticker']
                df = df[cols]

            ignored_count = len(ignored_tickers)
            success_rate = (processed_tickers / total_tickers) * 100

            print("\nProcessing Summary:")
            print(f"Total assets: {total_tickers}")
            print(f"Successfully processed: {processed_tickers}")
            print(f"Ignored assets: {ignored_count}")
            print(f"Success rate: {success_rate:.2f}%")
            print(f"Ignored tickers: {', '.join(ignored_tickers)}")

            return df
        else:
            print("No valid data found for any of the provided tickers.")
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None