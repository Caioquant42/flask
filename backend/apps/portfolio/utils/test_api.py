import requests
import json

def test_optimize_portfolio_api():
    url = 'http://localhost:8000/api/optimize-portfolio/'  # Adjust the URL as needed
    data = {
        'stocks': ['PETR4', 'VALE3', 'BBAS3', 'B3SA3', 'JBSS3'],
        'period': 12
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_optimize_portfolio_api()