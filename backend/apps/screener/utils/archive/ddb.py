from dolphindb import session
import pandas as pd
from screener_utils import calculate_rsi  # Import the RSI function from your module

# Connect to the DolphinDB server
s = session()
s.connect("46.202.149.154", 8848, "admin", "123456")

# Load the table from the distributed file system
s.run('t = loadTable("dfs://yfs", "stockdata_1d")')

# Execute the query to filter the data by Time and select specific columns
# Use a proper datetime format with T separating the date and time
result = s.run('select Datetime, Symbol, Close from t where Datetime > 2024.01.01T03:00:00')

# Print the result to verify the output
print(result)

# Convert the query result to a DataFrame.
df = pd.DataFrame(result)

# Ensure that the 'Datetime' column is parsed as datetime objects
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Group the DataFrame by the 'Symbol' column.
# Setting group_keys=False will prevent grouping keys from being added to the index.
grouped = df.groupby("Symbol", group_keys=False)

# Define a helper function to:
# - Sort the group's data by Datetime
# - Calculate the RSI using the provided function
def calculate_group_rsi(group):
    group = group.sort_values(by="Datetime")
    group["RSI"] = calculate_rsi(group)
    return group

# Apply the RSI calculation for each group and reset the DataFrame's index
df_with_rsi = grouped.apply(calculate_group_rsi).reset_index(drop=True)

# Drop rows where the RSI is NaN
df_with_rsi = df_with_rsi.dropna(subset=["RSI"])

# Display the top rows of the resulting DataFrame with the RSI column
print(df_with_rsi.tail())