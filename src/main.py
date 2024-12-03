import time
import sys
from api_utils import (
    fetch_and_validate_credentials,
    save_order_to_file,
    configure_logging,
    load_environment_variables,
    get_ticker_info,
    get_account_info,
    place_order,
    get_order_info,
    format_buy_register
)


def get_ticker(logger, base_quote):
    """Retrieve ticker information for the given base quote."""
    try:
        ticker_info = get_ticker_info(base_quote)
        logger.info(f"Ticker info retrieved successfully: {ticker_info}")
        return ticker_info
    except Exception as e:
        logger.error(f"Failed to retrieve ticker info: {e}")
        return None


def get_account(logger, access_token):
    """Retrieve account information using the access token."""
    account_id, account_info = get_account_info(access_token)
    if not account_id:
        logger.error("Failed to get account info.")
        return None, None
    return account_id, account_info


def place_market_order(logger, access_token, account_id, base_quote, cost):
    """Place a market order."""
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
        return order_info['orderId']
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        return None


def monitor_order(logger, access_token, account_id, base_quote, order_id):
    """Monitor the order until it is filled or canceled."""
    while True:
        order_details = get_order_info(access_token, account_id, base_quote, order_id)
        if order_details:
            order_status = order_details.get('status', '')
            if order_status == 'filled':
                logger.info(f"Order {order_id} was successfully executed.")
                logger.info(f"Order Details: {order_details}")
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


def place_and_monitor_order(logger, access_token, crypto_symbol, currency, cost, output_dir='./data'):
    """Main function to place and monitor an order."""
    base_quote = f"{crypto_symbol}-{currency}"
    
    ticker_info = get_ticker(logger, base_quote)
    if not ticker_info:
        return None

    account_id, account_info = get_account(logger, access_token)
    if not account_id:
        return None

    order_id = place_market_order(logger, access_token, account_id, base_quote, cost)
    if not order_id:
        return None

    order_details = monitor_order(logger, access_token, account_id, base_quote, order_id)
    if order_details:
        formatted_order_details = format_buy_register(order_details)
        save_order_to_file(formatted_order_details, crypto_symbol, currency, output_dir)
        return order_details
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
