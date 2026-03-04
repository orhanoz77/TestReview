"""
Helix ALM API Client
Provides a clean, type-safe interface to interact with Helix ALM REST API.
"""

import requests
import random
import json
from typing import Dict, Any, Optional
from requests import Session
import logging

logger = logging.getLogger(__name__)


class HelixAPIClient:
    """Client for interacting with Helix ALM REST API."""
    
    # Constants
    BASE_URL = 'https://10.214.41.6:8443/helix-alm/api/v0/'
    DEFAULT_TIMEOUT = 30  # seconds
    VERIFY_SSL = False  # Note: Should be True in production
    
    def __init__(self, base_url: str = BASE_URL, verify_ssl: bool = VERIFY_SSL, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the Helix ALM API Client.
        
        Args:
            base_url: Base URL for the Helix ALM API
            verify_ssl: Whether to verify SSL certificates (default: False for dev)
            timeout: Default timeout for requests in seconds
        """
        self.base_url = base_url
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = verify_ssl
    
    def get_project_list(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Fetch list of all projects.
        
        Args:
            headers: HTTP headers with authentication
            
        Returns:
            Dict mapping project names to UUIDs
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}projects"
        try:
            response = self.session.get(url=url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            projects = response.json().get('projects', [])
            return {project['name']: project['uuid'] for project in projects}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch projects: {str(e)}")
            raise Exception(f"Failed to fetch projects: {str(e)}")
    
    def get_test_cases_links(self, test_case_id: str, headers: Dict[str, str], uuid: str) -> Dict[str, Any]:
        """
        Fetch all links for a test case.
        
        Args:
            test_case_id: ID of the test case
            headers: HTTP headers with authentication
            uuid: Project UUID
            
        Returns:
            Dict containing link data
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}{uuid}/testCases/{test_case_id}/links"
        try:
            response = self.session.get(url=url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch test case links for ID {test_case_id}: {str(e)}")
            raise Exception(f"Failed to fetch test cases: {str(e)}")
    
    def add_requirement_link_to_test_case(
        self, 
        req_id: str, 
        test_case_id: str, 
        headers: Dict[str, str], 
        uuid: str
    ) -> Dict[str, Any]:
        """
        Add a link between a requirement and a test case.
        
        Args:
            req_id: Requirement ID
            test_case_id: Test case ID
            headers: HTTP headers with authentication
            uuid: Project UUID
            
        Returns:
            Dict containing the created link data
            
        Raises:
            Exception: If API request fails
        """
        data = {
            "linksData": [
                {
                    "id": random.randint(0, 4294967295),
                    "comment": "This is a list of linked related items",
                    "linkDefinition": {"id": 2003, "name": "Requirement Tested By"},
                    "type": "parentChildren",
                    "parentChildren": {
                        "parent": {
                            "itemID": req_id,
                            "itemType": "requirements",
                            "isSuspect": False,
                            "link": f"{self.base_url}{{{uuid}}}/requirements/{str(req_id)}"
                        },
                        "children": [
                            {
                                "itemID": test_case_id,
                                "itemType": "testCases",
                                "isSuspect": False,
                                "link": f"{self.base_url}{{{uuid}}}/testcases/{str(test_case_id)}"
                            }
                        ]
                    }
                }
            ]
        }
        url = f"{self.base_url}{uuid}/testCases/{str(test_case_id)}/links"
        try:
            response = self.session.post(
                url=url, 
                headers=headers, 
                data=json.dumps(data), 
                timeout=self.timeout
            )
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"Failed to add requirement link. Status: {response.status_code}")
                raise Exception(f"Failed to add requirement link. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add requirement link: {str(e)}")
            raise Exception(f"Failed to add requirement link: {str(e)}")
    
    def get_req_description(
        self, 
        req_id: str, 
        headers: Dict[str, str], 
        uuid: str,
        session: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Fetch requirement details (Summary, Description, Discussion).
        
        Args:
            req_id: Requirement ID
            headers: HTTP headers with authentication
            uuid: Project UUID
            session: Optional requests.Session for connection reuse
            
        Returns:
            Dict containing requirement data
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}{uuid}/requirements/{req_id}?fields=Summary,Description,Discussion"
        try:
            sess = session or self.session
            response = sess.get(url=url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch requirement {req_id}: {str(e)}")
            raise Exception(f"Failed to fetch requirement {req_id}: {str(e)}")
    
    def get_record_id(self, req_id: str, headers: Dict[str, str], uuid: str) -> str:
        """
        Search for a requirement by tag and return its ID.
        Supports tags: SW-*, CNST-*, SYS-*, SWA-*, SYSA-*.
        
        Args:
            req_id: Requirement ID to search for
            headers: HTTP headers with authentication
            uuid: Project UUID
            
        Returns:
            Requirement ID from search results
            
        Raises:
            Exception: If no matching requirement found or API fails
        """
        url = f"{self.base_url}{uuid}/requirements/search"
        search_clause = (
            "("
            "'REQ / RE / TASK Type' = 'Software Requirement' and "
            f"'Tag' = 'SW-{str(req_id)}'"
            ") or ("
            "'REQ / RE / TASK Type' = 'Constant' and "
            f"'Tag' = 'CNST-{str(req_id)}'"
            ") or ("
            "'REQ / RE / TASK Type' = 'System Requirement' and "
            f"'Tag' = 'SYS-{str(req_id)}'"
            ") or ("
            "'REQ / RE / TASK Type' = 'Software Architecture Requirement' and "
            f"'Tag' = 'SWA-{str(req_id)}'"
            ") or ("
            "'REQ / RE / TASK Type' = 'System Architecture Requirement' and "
            f"'Tag' = 'SYSA-{str(req_id)}'"
            ")"
        )
        data = {"fields": ['linked Items'], "search": search_clause}
        try:
            response = self.session.post(
                url, 
                headers=headers, 
                data=json.dumps(data), 
                timeout=self.timeout
            )
            response.raise_for_status()
            reqs = response.json().get('requirements', [])
            if not reqs:
                logger.warning(f"No matching requirements found for ID {req_id}")
                raise Exception("No matching requirements found.")
            return reqs[0]['id']
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get record ID for {req_id}: {str(e)}")
            raise Exception(f"Something went wrong while getting requirements: {str(e)}")
    
    def close(self) -> None:
        """Close the session and cleanup resources."""
        if self.session:
            self.session.close()
            logger.debug("API client session closed")
    
    def get_authentication_token(self, uuid: str, headers: Dict[str, str]) -> str:
        """
        Get an authentication token for a project.
        
        Args:
            uuid: Project UUID
            headers: HTTP headers with basic auth
            
        Returns:
            Access token string
            
        Raises:
            Exception: If token retrieval fails
        """
        token_url = f"{self.base_url}{uuid}/token"
        try:
            response = self.session.get(url=token_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            token = response.json().get('accessToken')
            if not token:
                raise Exception("No access token in response")
            logger.debug(f"Successfully obtained authentication token for UUID {uuid}")
            return token
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve authentication token for UUID {uuid}: {str(e)}")
            raise Exception(f"Failed to retrieve authentication token: {str(e)}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
