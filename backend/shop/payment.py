import requests
from .make_paypal_dict import *


def paypal_pay(token, data):
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
    # data = gen_test_data()
    PAYPAL_CHECKOUT_ORDERS_URL = os.getenv('PAYPAL_CHECKOUT_ORDERS_URL')
    response = requests.post(PAYPAL_CHECKOUT_ORDERS_URL, headers=headers, data=data)
    return response


def paypal_capture(orderID):
    token = get_token()
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture', headers=headers)
    return response


def paypal_checkout_orders(orderID):
    token = get_token()
    headers = {
            'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'https://api.sandbox.paypal.com/v2/checkout/orders/{orderID}', headers=headers)
    return response



# https://www.techcoil.com/blog/how-to-get-an-access-token-to-integrate-with-paypal-rest-apis-in-python/
def get_token(): 
    PAYPAL_URL = os.getenv('PAYPAL_URL_DEV')
    APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    
    oauth_url = '%s/v1/oauth2/token' % PAYPAL_URL
    oauth_response = requests.post(oauth_url,
                                   headers= {'Accept': 'application/json',
                                             'Accept-Language': 'en_US'},
                                   auth=(APP_CLIENT_ID, APP_SECRET),
                                   data={'grant_type': 'client_credentials'})
   
    oauth_body_json = oauth_response.json()
    access_token = oauth_body_json['access_token']
    return access_token


