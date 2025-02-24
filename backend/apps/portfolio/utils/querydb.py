from dolphindb import session
import pandas as pd

def query_dolphindb():
    # Connect to the DolphinDB server
    s = session()
    s.connect("46.202.149.154", 8848, "admin", "123456")

    # Load the table from the distributed file system
    s.run('t = loadTable("dfs://yfs", "stockdata_1d")')

    # Execute the query to filter the data by Time and select specific columns
    # Use a proper datetime format with T separating the date and time
    ddb_data = s.run('select Datetime, Symbol, AdjClose from t where Datetime > 2022.01.01T03:00:00')
    

    return ddb_data

ddb_data = query_dolphindb()
print(ddb_data)
