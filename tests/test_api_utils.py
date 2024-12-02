import unittest
from unittest.mock import patch, Mock
from src import api_utils

class TestApiUtils(unittest.TestCase):

    @patch('src.api_utils.requests.post')
    def test_authenticate_success(self, mock_post):
        # Arrange
        tapi_id = 'test_id'
        tapi_secret = 'test_secret'
        expected_token = 'mock_access_token'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': expected_token}
        mock_post.return_value = mock_response

        # Act
        access_token = api_utils.authenticate(tapi_id, tapi_secret)

        # Assert
        mock_post.assert_called_once_with(
            f'{api_utils.base_url}/authorize',
            json={'login': tapi_id, 'password': tapi_secret},
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(access_token, expected_token)

    @patch('src.api_utils.requests.post')
    def test_authenticate_failure(self, mock_post):
        # Arrange
        tapi_id = 'test_id'
        tapi_secret = 'wrong_secret'
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_post.return_value = mock_response

        # Act
        access_token = api_utils.authenticate(tapi_id, tapi_secret)

        # Assert
        mock_post.assert_called_once()
        self.assertIsNone(access_token)

    @patch('src.api_utils.requests.get')
    def test_get_ticker_info_success(self, mock_get):
        # Arrange
        base_quote = 'BTC/USD'
        expected_data = {'symbol': base_quote, 'price': '50000'}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        # Act
        ticker_info = api_utils.get_ticker_info(base_quote)

        # Assert
        mock_get.assert_called_once_with(f'{api_utils.base_url}/tickers?symbols={base_quote}')
        self.assertEqual(ticker_info, expected_data)

    @patch('src.api_utils.requests.get')
    def test_get_ticker_info_failure(self, mock_get):
        # Arrange
        base_quote = 'BTC/USD'
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        mock_get.return_value = mock_response

        # Act
        ticker_info = api_utils.get_ticker_info(base_quote)

        # Assert
        mock_get.assert_called_once()
        self.assertIsNone(ticker_info)

    @patch('src.api_utils.requests.get')
    def test_get_account_info_success(self, mock_get):
        # Arrange
        access_token = 'valid_token'
        expected_account_info = [{'id': 'account123', 'balance': 1000}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_account_info
        mock_get.return_value = mock_response

        # Act
        account_id, account_info = api_utils.get_account_info(access_token)

        # Assert
        mock_get.assert_called_once_with(
            f'{api_utils.base_url}/accounts',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(account_id, 'account123')
        self.assertEqual(account_info, expected_account_info)

    @patch('src.api_utils.requests.get')
    def test_get_account_info_failure(self, mock_get):
        # Arrange
        access_token = 'invalid_token'
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = 'Forbidden'
        mock_get.return_value = mock_response

        # Act
        account_id, account_info = api_utils.get_account_info(access_token)

        # Assert
        mock_get.assert_called_once()
        self.assertIsNone(account_id)
        self.assertIsNone(account_info)

    @patch('src.api_utils.requests.post')
    def test_place_order_success(self, mock_post):
        # Arrange
        access_token = 'valid_token'
        account_id = 'account123'
        base_quote = 'BTC/USD'
        order_payload = {'type': 'buy', 'amount': 1, 'price': 50000}
        expected_order_info = {'order_id': 'order456', 'status': 'placed'}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_order_info
        mock_post.return_value = mock_response

        # Act
        order_info = api_utils.place_order(access_token, account_id, base_quote, order_payload)

        # Assert
        mock_post.assert_called_once_with(
            f'{api_utils.base_url}/accounts/{account_id}/{base_quote}/orders',
            headers={'Authorization': f'Bearer {access_token}'},
            json=order_payload
        )
        self.assertEqual(order_info, expected_order_info)

    @patch('src.api_utils.requests.post')
    def test_place_order_failure(self, mock_post):
        # Arrange
        access_token = 'valid_token'
        account_id = 'account123'
        base_quote = 'BTC/USD'
        order_payload = {'type': 'buy', 'amount': 1, 'price': 50000}
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'
        mock_post.return_value = mock_response

        # Act
        order_info = api_utils.place_order(access_token, account_id, base_quote, order_payload)

        # Assert
        mock_post.assert_called_once()
        self.assertIsNone(order_info)

    @patch('src.api_utils.requests.get')
    def test_get_order_info_success(self, mock_get):
        # Arrange
        access_token = 'valid_token'
        account_id = 'account123'
        base_quote = 'BTC/USD'
        order_id = 'order456'
        expected_order_info = {'order_id': order_id, 'status': 'filled'}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_order_info
        mock_get.return_value = mock_response

        # Act
        order_info = api_utils.get_order_info(access_token, account_id, base_quote, order_id)

        # Assert
        mock_get.assert_called_once_with(
            f'{api_utils.base_url}/accounts/{account_id}/{base_quote}/orders/{order_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(order_info, expected_order_info)

    @patch('src.api_utils.requests.get')
    def test_get_order_info_failure(self, mock_get):
        # Arrange
        access_token = 'valid_token'
        account_id = 'account123'
        base_quote = 'BTC/USD'
        order_id = 'nonexistent_order'
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Order Not Found'
        mock_get.return_value = mock_response

        # Act
        order_info = api_utils.get_order_info(access_token, account_id, base_quote, order_id)

        # Assert
        mock_get.assert_called_once()
        self.assertIsNone(order_info)

if __name__ == '__main__':
    unittest.main()
