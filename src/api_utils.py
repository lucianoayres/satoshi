import os
from datetime import datetime, timezone
import json
import requests
import logging

base_url = 'https://api.mercadobitcoin.net/api/v4'

def authenticate(tapi_id, tapi_secret):
    auth_url = f'{base_url}/authorize'
    auth_payload = {
        'login': tapi_id,
        'password': tapi_secret
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(auth_url, json=auth_payload, headers=headers)
    if response.status_code == 200:
        auth_data = response.json()
        access_token = auth_data['access_token']
        return access_token
    else:
        print('Failed to obtain access token:', response.status_code, response.text)
        return None

def get_ticker_info(base_quote):
    tickers_url = f'{base_url}/tickers?symbols={base_quote}'
    response = requests.get(tickers_url)
    if response.status_code == 200:
        ticker_info = response.json()
        return ticker_info
    else:
        print('Failed to retrieve ticker information:', response.status_code, response.text)
        return None

def get_account_info(access_token):
    account_url = f'{base_url}/accounts'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(account_url, headers=headers)
    if response.status_code == 200:
        account_info = response.json()
        account_id = account_info[0]['id']
        return account_id, account_info
    else:
        print('Failed to retrieve account information:', response.status_code, response.text)
        return None, None

def place_order(access_token, account_id, base_quote, order_payload):
    place_order_url = f'{base_url}/accounts/{account_id}/{base_quote}/orders'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(place_order_url, headers=headers, json=order_payload)
    if response.status_code == 200:
        order_info = response.json()
        return order_info
    else:
        print('Failed to place order:', response.status_code, response.text)
        return None

def get_order_info(access_token, account_id, base_quote, order_id):
    get_order_url = f'{base_url}/accounts/{account_id}/{base_quote}/orders/{order_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(get_order_url, headers=headers)
    if response.status_code == 200:
        order_info = response.json()
        return order_info
    else:
        print('Failed to retrieve order information:', response.status_code, response.text)
        return None
    
def load_json_file(filepath):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found. Creating a new file.")
        with open(filepath, 'w') as file:
            json.dump([], file)  
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError(f"The JSON file at {filepath} does not contain a JSON array.")
            return data
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'. Initializing as an empty list.")
        return []

def save_json_file(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def add_entry_to_json(filepath, new_entry):
    try:
        data = load_json_file(filepath)
        data.append(new_entry)  
        save_json_file(filepath, data)  
        return data  
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def format_buy_register(response):
    execution = response["executions"][0]
    return {
        "date": datetime.fromtimestamp(response["created_at"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
        "order_id": response["id"],
        "order_execution_id": execution["id"],
        "coin": response["instrument"].split('-')[0],
        "type": response["type"].lower(),
        "price_per_unit": round(response["avgPrice"], 2),
        "currency": response["instrument"].split('-')[1],
        "cost": response["cost"],
        "fee_rate_percent": round(float(execution["fee_rate"]), 2),
        "fee": f"{float(response['fee']):.8f}",
        "quantity": f"{float(response['filledQty']):.8f}"
    }


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def load_environment_variables(logger):
    isGithubActionRunning = os.getenv('GITHUB_ACTIONS')

    if isGithubActionRunning:  
        logger.info('Running in GitHub Actions mode.')
    else: 
        try:
            from dotenv import load_dotenv  
            load_dotenv()
            logger.info('Loaded environment variables from .env file.')
        except ImportError:
            logger.error('Failed to import python-dotenv. Install it with "pip install python-dotenv" for development.')
            return None, None
    
    tapi_id = os.getenv('MERCADO_BITCOIN_API_ID')
    tapi_secret = os.getenv('MERCADO_BITCOIN_API_SECRET')

    if not tapi_id or not tapi_secret:
        logger.error("Environment variables TAPI_ID and TAPI_SECRET must be set.")
        return None, None

    logger.info("Loaded environment variables successfully.")
    return tapi_id, tapi_secret


def fetch_and_validate_credentials(logger, tapi_id, tapi_secret):
    logger.info("Fetching and validating credentials...")
    access_token = authenticate(tapi_id, tapi_secret)
    if not access_token:
        logger.error("Failed to authenticate. Please check your API credentials.")
        return None

    logger.info("Authentication successful.")
    return access_token


def save_order_to_file(order_details, crypto_symbol, currency, output_dir='.'):
    """Function to save order details to a file with {Symbol}-{Currency} prefix in the specified directory."""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"Output directory created at {output_dir}")

        file_name = f"{crypto_symbol}-{currency}-orders.json"
        file_path = os.path.join(output_dir, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                orders_data = json.load(file)
        else:
            orders_data = []

        orders_data.append(order_details)

        with open(file_path, 'w') as file:
            json.dump(orders_data, file, indent=4)

        logging.info(f"Order details saved to {file_path}")

    except Exception as e:
        logging.error(f"Failed to save order details: {e}")

