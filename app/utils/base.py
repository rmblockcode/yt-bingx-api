import requests
import os
import time
import hmac
import hashlib
from fastapi import HTTPException

BINGX_API_URL = os.environ.get('BINGX_API_URL')
BINGX_API_KEY = os.environ.get('BINGX_API_KEY')

BINGX_ERRORS = {
    100001: 'Signature authentication failed',
    100202: 'Insufficient balance',
    100400: 'Invalid parameter',
    100440: 'Order price deviates greatly from the market price',
    100500: 'Internal server error',
    100503: 'Server busy'
}

def api_request(service, method='GET', query_params=None):
    """
    
    """
    url = f'{BINGX_API_URL}{service}'
    timestamp = int(time.time() * 1000)

    params = f'timestamp={timestamp}'

    if query_params:
        params += f'&{query_params}'

    headers = {
        'Content-Type': 'application/json',
        'X-BX-APIKEY': BINGX_API_KEY
    }

    signature = generate_signature(params)
    params += f'&signature={signature}'

    url += f'?{params}'
    print(url)
    if method == 'GET':
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    
    response = response.json()
    if 'success' in response and not response.get('success'):
        raise HTTPException(
            status_code=400,
            detail=BINGX_ERRORS.get(response.get('code'))
        )
    
    return response


def generate_signature(query_params):
    """
        Funcion para generar el signature a partir de los query params 
        enviados en la peticion
    """
    secret_key = os.environ.get('BINGX_SECRET_KEY')
    signature = hmac.new(
        secret_key.encode(),
        msg=query_params.encode(),
        digestmod=hashlib.sha256).hexdigest()
    return signature