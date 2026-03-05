"""
Authentication utilities for Helix ALM
"""

import base64
import logging
import requests
from typing import Dict
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def get_authentication_token(base_url: str, uuid: str, headers: Dict[str, str]) -> str:
    """
    Get authentication token from Helix ALM API.
    
    Args:
        base_url: Base URL for the Helix ALM API
        uuid: Project UUID
        headers: HTTP headers with basic auth
        
    Returns:
        Access token string
        
    Raises:
        Exception: If token retrieval fails
    """
    token_url = f"{base_url}{uuid}/token"
    logger.debug(f"Requesting authentication token from: {token_url}")
    try:
        response = requests.get(url=token_url, headers=headers, verify=False)
        response.raise_for_status()
        token = response.json().get('accessToken')
        if not token:
            logger.error("No access token in response")
            raise Exception("No access token in response")
        logger.info(f"Authentication token retrieved successfully for project: {uuid}")
        return token
    except RequestException as e:
        logger.error(f"Failed to retrieve authentication token: {str(e)}")
        raise Exception(f"Failed to retrieve authentication token: {str(e)}")
