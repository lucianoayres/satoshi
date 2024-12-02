import os
import time
import logging
import sys
import json
from api_utils import (
    authenticate,
    get_ticker_info,
    get_account_info,
    place_order,
    get_order_info
)


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


def place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost):
    logger.info(f"Placing order for {cost} {currency} of {crypto_symbol} in {currency}")
    base_quote = f"{crypto_symbol}-{currency}"
    try:
        ticker_info = get_ticker_info(base_quote)
        logger.info(f"Ticker info retrieved successfully: {ticker_info}")
    except Exception as e:
        logger.error(f"Failed to retrieve ticker info: {e}")
        return None

    account_id, account_info = get_account_info(access_token)
    if not account_id:
        logger.error("Failed to get account info.")
        return None

    order_payload = {
        'type': 'market',
        'side': 'buy',
        'cost': cost
    }

    try:
        order_info = place_order(access_token, account_id, base_quote, order_payload)
        if order_info is None:
            logger.error("Order placement returned None.")
            return None
        logger.info(f"Order placed successfully. Order ID: {order_info['orderId']}")
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        return None

    order_id = order_info['orderId']

    while True:
        order_details = get_order_info(access_token, account_id, base_quote, order_id)
        if order_details:
            logger.info(f"Order details: {order_details}")
            order_status = order_details.get('status', '')
            if order_status == 'filled':
                logger.info(f"Order {order_id} was successfully executed.")
                return order_details
            elif order_status == 'canceled':
                logger.warning(f"Order {order_id} was canceled.")
                return None
            else:
                logger.info(f"Order {order_id} is still pending. Current status: {order_status}")
                time.sleep(5)
        else:
            logger.error(f"Failed to retrieve order details for order {order_id}")
            return None

def main():
    logger = configure_logging()

    tapi_id, tapi_secret = load_environment_variables(logger)
    if not tapi_id or not tapi_secret:
        return None

    access_token = fetch_and_validate_credentials(logger, tapi_id, tapi_secret)
    if not access_token:
        return None

    if len(sys.argv) < 4:
        print("Usage: python src/main.py [crypto_symbol] [currency] [cost]")
        return None

    crypto_symbol = sys.argv[1]
    currency = sys.argv[2]
    try:
        cost = float(sys.argv[3])
        if cost <= 0:
            raise ValueError("Cost must be a positive number.")
    except ValueError as e:
        print(f"Invalid cost value: {e}")
        return None

    return place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost)

if __name__ == '__main__':
    result = main()
    if result:
        print(json.dumps(result))  # Output the result for the workflow to capture
