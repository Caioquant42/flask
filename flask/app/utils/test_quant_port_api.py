import requests
import json

# API endpoint
url = "http://localhost:5000/api/quant_port"  # Replace with your actual API URL

# Parameters for the POST request
params = {
    "nret_mln": 15,
    "nclusters": 4,
    "period_ret": 2,
    "ret_mc": 7,
    "n_sim_mc": 1000,
    "tam_port": 5
}

# Function to make the API request
def test_quant_port_api(params):
    try:
        # Make the POST request
        response = requests.post(url, json=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            data = response.json()
            print("\nResponse data:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Test with provided parameters
print("Testing with custom parameters:")
test_quant_port_api(params)

# Test with default parameters (empty request body)
print("\nTesting with default parameters:")
test_quant_port_api({})

if __name__ == "__main__":
    print("Quant Port API Test")
    print("==================")