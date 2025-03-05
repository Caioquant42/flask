import requests
from bs4 import BeautifulSoup
import json
import re

# URL of the website you want to scrape
url = "https://www.dadosdemercado.com.br/indices/cdi?form=MG0AV3"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the id "index-values"
table = soup.find('table', id='index-values')

# Initialize a dictionary to store the data
cdi_data = {}

# Iterate through the table rows
for row in table.find_all('tr')[1:]:  # Skip the header row
    columns = row.find_all('td')
    year = columns[0].text.strip()
    
    # Extract monthly data
    monthly_data = {}
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    for i, month in enumerate(months):
        value = columns[i+1].get('data-value')
        if value and value != 'None':
            monthly_data[month] = float(value)
    
    cdi_data[year] = monthly_data

# Convert the data to JSON
json_data = json.dumps(cdi_data, indent=2, ensure_ascii=False)

# Print the JSON data
print(json_data)

# Optionally, save the JSON data to a file
with open('scraped_cdi_data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)