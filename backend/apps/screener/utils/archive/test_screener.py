import pandas as pd
from screener_utils import screener_rsi

def test_screener_rsi():
    # Define a couple of test cases with known table names from the server
    test_cases = [
        ("stockdata_60m", "60m"),
        ("stockdata_1d", "1d")
    ]
    
    for table_name, file_suffix in test_cases:
        print(f"\nTesting for table: {table_name}")

        # Call the screener_rsi function
        overbought_df, oversold_df = screener_rsi(table_name, file_suffix)

        # Assertions or simple checks to validate the output
        assert isinstance(overbought_df, pd.DataFrame), "Expected output is a DataFrame"
        assert isinstance(oversold_df, pd.DataFrame), "Expected output is a DataFrame"

        # Check if the output DataFrames contain the expected columns
        for df, condition in zip([overbought_df, oversold_df], ["Overbought", "Oversold"]):
            if not df.empty:
                assert 'RSI' in df.columns, f"{condition} DataFrame should contain 'RSI' column"
                
        print(f"Pass: {table_name} results processed successfully.")

if __name__ == "__main__":
    test_screener_rsi()