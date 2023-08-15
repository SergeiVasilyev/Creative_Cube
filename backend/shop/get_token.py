import os
import requests

# https://www.techcoil.com/blog/how-to-get-an-access-token-to-integrate-with-paypal-rest-apis-in-python/
def get_token(): 
    # Change the URL to https://api-m.paypal.com for live access
    PAYPAL_URL = os.getenv('PAYPAL_URL_DEV')
    APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    
    oauth_url = '%s/v1/oauth2/token' % PAYPAL_URL
    # {'Content-Type': 'application/x-www-form-urlencoded'}
    oauth_response = requests.post(oauth_url,
                                   headers= {'Accept': 'application/json',
                                             'Accept-Language': 'en_US'},
                                   auth=(APP_CLIENT_ID, APP_SECRET),
                                   data={'grant_type': 'client_credentials'})
   
    # Get OAuth JSON in response body
    oauth_body_json = oauth_response.json()
    # Get access token
    access_token = oauth_body_json['access_token']
    return access_token