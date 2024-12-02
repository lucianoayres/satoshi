import os
import logging
import sys
from dotenv import load_dotenv  # Import only when needed
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
    environment = os.getenv('ENVIRONMENT', 'development')

    if environment == 'development':
        try:
            load_dotenv()
            logger.info('Loaded environment variables from .env file.')
        except ImportError:
            logger.error('Failed to import python-dotenv. Install it with "pip install python-dotenv" for development.')
            return None, None
    else:
        logger.info('Running in production mode.')

    tapi_id = os.getenv('TAPI_ID')
    tapi_secret = os.getenv('TAPI_SECRET')

    if not tapi_id or not tapi_secret:
        logger.error("Environment variables TAPI_ID and TAPI_SECRET must be set.")
        return None, None

    return tapi_id, tapi_secret


def fetch_and_validate_credentials(logger):
    tapi_id, tapi_secret = load_environment_variables(logger)
    if not tapi_id or not tapi_secret:
        return None

    access_token = authenticate(tapi_id, tapi_secret)
    if not access_token:
        return None

    return access_token


def place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost):
    base_quote = f"{crypto_symbol}-{currency}"
    ticker_info = get_ticker_info(base_quote)

    account_id, account_info = get_account_info(access_token)
    if not account_id:
        return

    order_payload = {
        'type': 'market',
        'side': 'buy',
        'cost': cost
    }

    order_info = place_order(access_token, account_id, base_quote, order_payload)
    if not order_info or 'id' not in order_info:
        logger.error('Order ID not found in order_info.')
        return

    order_id = order_info['id']

    order_details = get_order_info(access_token, account_id, base_quote, order_id)
    if order_details:
        order_status = order_details.get('status', '')
        if order_status == 'filled':
            logger.info(f"Order {order_id} was successfully executed.")
        else:
            logger.warning(f"Order {order_id} was not fully executed. Current status: {order_status}")
    else:
        logger.error('Failed to retrieve order details.')


def main():
    logger = configure_logging()

    # Get arguments from command line
    if len(sys.argv) < 2:
        print("Usage: python src/main.py [crypto_symbol] [currency] cost")
        print("Default crypto symbol: BTC")
        print("Default currency: BRL")
        return

    crypto_symbol = sys.argv[1] if len(sys.argv) >= 2 else 'BTC'
    currency = sys.argv[2] if len(sys.argv) >= 3 else 'BRL'

    if len(sys.argv) < 3:
        print("Cost is a required argument.")
        return

    cost = float(sys.argv[3])  # Convert cost to float

    access_token = fetch_and_validate_credentials(logger)
    if not access_token:
        return

    place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost)


if __name__ == '__main__':
    import sys
    main()