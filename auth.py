import base64
import requests
from requests.exceptions import RequestException

def get_authentication_token(base_url, uuid, headers):
    token_url = f"{base_url}{uuid}/token"
    try:
        response = requests.get(url=token_url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json().get('accessToken')
    except RequestException as e:
        raise Exception(f"Failed to retrieve authentication token: {str(e)}")
