import os
import time
import logging
import sys
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


import os

def load_environment_variables(logger):
    isGithubActionRunning = os.getenv('GITHUB_ACTIONS')

    if isGithubActionRunning:  # Executes if running in GitHub Actions
        logger.info('Running in GitHub Actions mode.')
    else:  # Executes if not running in GitHub Actions
        try:
            from dotenv import load_dotenv  # Import only when needed
            load_dotenv()
            logger.info('Loaded environment variables from .env file.')
        except ImportError:
            logger.error('Failed to import python-dotenv. Install it with "pip install python-dotenv" for development.')
            return None, None

    symbol = os.getenv('SYMBOL')
    currency = os.getenv('CURRENCY')
    cost = os.getenv('COST')

    print(f"Symbol: {symbol}, Currency: {currency}, Cost: {cost}")
    
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
    logger.info(f"Placing order for {cost} {currency} of {crypto_symbol}")
    base_quote = f"{crypto_symbol}-{currency}"
    try:
        ticker_info = get_ticker_info(base_quote)
        logger.info(f"Retrieved ticker info for {base_quote}")
    except Exception as e:
        logger.error(f"Failed to retrieve ticker info: {e}")
        return

    account_id, account_info = get_account_info(access_token)
    if not account_id:
        logger.error("Failed to get account info.")
        return

    order_payload = {
        'type': 'market',
        'side': 'buy',
        'cost': cost
    }

    try:
        order_info = place_order(access_token, account_id, base_quote, order_payload)
        logger.info(f"Order placed successfully. Order ID: {order_info['id']}")
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        return

    order_id = order_info['id']

    while True:
        order_details = get_order_info(access_token, account_id, base_quote, order_id)
        if order_details:
            order_status = order_details.get('status', '')
            if order_status == 'filled':
                logger.info(f"Order {order_id} was successfully executed.")
                break
            elif order_status == 'canceled':
                logger.warning(f"Order {order_id} was canceled.")
                break
            else:
                logger.info(f"Order {order_id} is still pending. Current status: {order_status}")
                time.sleep(5)  # Adjust the sleep time as needed
        else:
            logger.error(f"Failed to retrieve order details for order {order_id}")
            break


def main():
    logger = configure_logging()

    # Load environment variables
    tapi_id, tapi_secret = load_environment_variables(logger)
    if not tapi_id or not tapi_secret:
        return

    # Fetch and validate credentials
    access_token = fetch_and_validate_credentials(logger, tapi_id, tapi_secret)
    if not access_token:
        return

    # Get arguments from command line
    if len(sys.argv) < 4:
        print("Usage: python src/main.py [crypto_symbol] [currency] [cost]")
        return

    crypto_symbol = sys.argv[1]
    currency = sys.argv[2]
    try:
        cost = float(sys.argv[3])  # Convert cost to float (works for integers too)
        if cost <= 0:
            raise ValueError("Cost must be a positive number.")
    except ValueError as e:
        print(f"Invalid cost value: {e}")
        return

    # Place and monitor the order
    place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost)

if __name__ == '__main__':
    import sys
    main()