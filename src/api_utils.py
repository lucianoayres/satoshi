# src/api_utils.py

import requests

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
        print('Access token generated successfully')
        return access_token
    else:
        print('Failed to obtain access token:', response.status_code, response.text)
        return None

def get_ticker_info(base_quote):
    tickers_url = f'{base_url}/tickers?symbols={base_quote}'
    response = requests.get(tickers_url)
    if response.status_code == 200:
        ticker_info = response.json()
        print('Ticker info retrieved successfully:', ticker_info)
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
    if response.status_code == 201:
        order_info = response.json()
        print('Order placed successfully:', order_info)
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
        print('Order Information:', order_info)
        return order_info
    else:
        print('Failed to retrieve order information:', response.status_code, response.text)
        return None