import requests
from bs4 import BeautifulSoup
import json

# URL of the website you want to scrape
url = "https://www.dadosdemercado.com.br/fluxo"

# Send a GET request to the URL
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with the specified ID and class
    table = soup.find('table', {'class': 'normal-table', 'id': 'flow'})

    # Extract the headers
    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]

    # Initialize a list to hold all the rows
    data = []

    # Extract each row of data and convert into a dictionary
    for tr in table.find('tbody').find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        # Create a dictionary for the row and append to the data list
        row_data = {header: cell for header, cell in zip(headers, cells)}
        data.append(row_data)

    # Save the extracted data into a JSON file
    with open('fluxo.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Table data successfully saved to 'fluxo.json'")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)