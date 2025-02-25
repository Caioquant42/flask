import requests
from bs4 import BeautifulSoup
import json
import re

# URL of the website you want to scrape
url = "https://www.dadosdemercado.com.br/fluxo"

# Send a GET request to the URL
response = requests.get(url)

# Function to extract a number from a string using regex and convert to float
def str_to_float_regex(s):
    # Remove the trailing " mi" if present
    s = s.replace(" mi", "")
    # Use regex to find a numeric pattern: optional '-' followed by digits, dots, and a decimal part
    match = re.search(r'-?[\d\.\,]+', s)
    if match:
        num_str = match.group(0)
        # Remove any dot that is used as thousands separator and change comma to dot as the decimal separator
        cleaned = num_str.replace('.', '').replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0

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
        # Create a dictionary for the row
        row_data = {header: cell for header, cell in zip(headers, cells)}
        
        # Calculate the sum for 'Todos' ignoring the 'Data' column
        total = 0.0
        for key, value in row_data.items():
            if key != 'Data':
                total += str_to_float_regex(value)
                
        # Format the total to two decimal places, convert dot to comma
        total_formatted = f"{total:.2f}".replace('.', ',')
        
        # Add 'Todos' to the row data
        row_data['Todos'] = f"{total_formatted} mi"
        
        data.append(row_data)
    
    # Save the extracted data into a JSON file
    with open('fluxo.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print("Table data successfully saved to 'fluxo.json'")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)