import pandas as pd
import numpy as np
from screener_ewma import screener_ewma

def test_screener_ewma():
    # Define test cases
    table_name = "stockdata_1d"
    file_suffix = "1d"

    # Execute the screener function
    highvol_df, lowvol_df = screener_ewma(table_name, file_suffix)

    # Perform assertions or checks
    assert isinstance(highvol_df, pd.DataFrame), f"Expected highvol_df to be a DataFrame, got {type(highvol_df)}"
    assert isinstance(lowvol_df, pd.DataFrame), f"Expected lowvol_df to be a DataFrame, got {type(lowvol_df)}"

    # If DataFrames are not empty, check for expected columns
    if not highvol_df.empty:
        assert 'EWMA' in highvol_df.columns, "highvol_df should contain 'EWMA' column"
        assert 'volatility_key' in highvol_df.columns, "highvol_df should contain 'volatility_key' column"
        assert all(highvol_df['volatility_key'] == 'high'), "All entries in highvol_df should have volatility_key as 'high'"

    if not lowvol_df.empty:
        assert 'EWMA' in lowvol_df.columns, "lowvol_df should contain 'EWMA' column"
        assert 'volatility_key' in lowvol_df.columns, "lowvol_df should contain 'volatility_key' column"
        assert all(lowvol_df['volatility_key'] == 'low'), "All entries in lowvol_df should have volatility_key as 'low'"

    print("All tests passed successfully for screener_ewma.")

if __name__ == "__main__":
    test_screener_ewma()