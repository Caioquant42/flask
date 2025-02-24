import dolphindb as ddb

# Create a session and connect to the DolphinDB server
s = ddb.session()
s.connect("46.202.149.154", 8848, "admin", "123456")

# Script to delete the table
delete_table_script = """
if (existsTable('dfs://oplab', 'stockinfo')) {
    db = database('dfs://oplab')
    dropTable(db, 'stockinfo')
    print("Table 'stockinfo' in 'dfs://oplab' has been successfully deleted.")
} else {
    print("Table 'stockinfo' in 'dfs://oplab' does not exist.")
}
"""

# Run the delete table script
result = s.run(delete_table_script)

# Print the result
print(result)

# Close the connection
s.close()
