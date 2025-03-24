import unittest
from unittest.mock import patch
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True

class IBOVResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    @patch('app.utils.ibov_stocks.get_ibov_stocks')
    def test_get_ibov(self, mock_get_ibov_stocks):
        mock_data = [
            {'symbol': 'PETR4', 'name': 'PETROBRAS PN', 'close': 28.35},
            {'symbol': 'VALE3', 'name': 'VALE ON', 'close': 68.20}
        ]
        mock_get_ibov_stocks.return_value = mock_data

        response = self.client.get('/api/ibov')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['symbol'], 'PETR4')
        self.assertEqual(data[1]['symbol'], 'VALE3')

    @patch('app.utils.ibov_stocks.get_ibov_stocks')
    def test_get_ibov_error(self, mock_get_ibov_stocks):
        mock_get_ibov_stocks.side_effect = Exception('API Error')
        response = self.client.get('/api/ibov')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error'], 'Internal Server Error')

    @patch('app.utils.ibov_stocks.getstatic_ibov_stocks')
    def test_get_ibov_static(self, mock_getstatic_ibov_stocks):
        mock_data = [
            {'symbol': 'PETR4', 'name': 'PETROBRAS PN', 'close': 28.35},
            {'symbol': 'VALE3', 'name': 'VALE ON', 'close': 68.20}
        ]
        mock_getstatic_ibov_stocks.return_value = mock_data

        response = self.client.get('/api/ibovstatic')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['symbol'], 'PETR4')
        self.assertEqual(data[1]['symbol'], 'VALE3')



@patch('app.utils.volatility_analysis.get_volatility_analysis')
def test_get_volatility_analysis(self, mock_get_volatility_analysis):
    mock_data = [
        {'symbol': 'PETR4', 'iv_to_ewma_ratio_current': 1.2},
        {'symbol': 'VALE3', 'iv_to_ewma_ratio_current': 0.9}
    ]
    mock_get_volatility_analysis.return_value = mock_data

    response = self.client.get('/api/volatility')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(len(data), 2)
    self.assertEqual(data[0]['symbol'], 'PETR4')
    self.assertEqual(data[1]['symbol'], 'VALE3')

@patch('app.utils.cumulative_performance.get_cumulative_performance')
def test_get_cumulative_performance(self, mock_get_cumulative_performance):
    mock_data = {
        "CDI": {"2023-01-01": 1.0, "2023-02-01": 1.01},
        "SP500": {"2023-01-01": 3800, "2023-02-01": 3900}
    }
    mock_get_cumulative_performance.return_value = mock_data

    response = self.client.get('/api/performance')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(len(data), 2)
    self.assertIn('CDI', data)
    self.assertIn('SP500', data)

    # Test filtering by asset
    response = self.client.get('/api/performance?asset=CDI')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(len(data), 1)
    self.assertIn('CDI', data)

@patch('app.utils.rrg_data.get_rrg_data')
def test_get_rrg_data(self, mock_get_rrg_data):
    mock_data = {
        "PETR4": {
            "Dates": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "RS-Ratio": [100.0, 101.0, 102.0, 101.5, 103.0],
            "RS-Momentum": [1.0, 1.01, 1.02, 0.99, 1.03]
        },
        "VALE3": {
            "Dates": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "RS-Ratio": [98.0, 99.0, 100.0, 101.0, 102.0],
            "RS-Momentum": [0.98, 1.01, 1.01, 1.01, 1.01]
        }
    }
    mock_get_rrg_data.return_value = mock_data

    response = self.client.get('/api/rrg')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(len(data), 2)
    self.assertIn('PETR4', data)
    self.assertIn('VALE3', data)

    # Test filtering by symbol
    response = self.client.get('/api/rrg?symbol=PETR4')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(len(data), 1)
    self.assertIn('PETR4', data)

    
if __name__ == '__main__':
    unittest.main()