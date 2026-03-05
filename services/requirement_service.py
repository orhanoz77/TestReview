"""
Requirement Service
Handles test case links and requirement details
"""

import logging
from typing import Dict, List, Any, Optional
from helix_api_client import HelixAPIClient

logger = logging.getLogger(__name__)


class RequirementService:
    """Service for managing test case requirements and links."""
    
    def __init__(self, api_client: HelixAPIClient) -> None:
        """
        Initialize requirement service.
        
        Args:
            api_client: HelixAPIClient instance for API communication
        """
        self.api_client = api_client
    
    def get_test_case_links(
        self,
        test_case_id: str,
        headers: Dict[str, str],
        project_uuid: str
    ) -> List[str]:
        """
        Fetch requirement IDs linked to a test case.
        
        Args:
            test_case_id: ID of the test case
            headers: HTTP headers with authentication
            project_uuid: UUID of the project
            
        Returns:
            List of requirement IDs
            
        Raises:
            Exception: If API request fails or test case ID invalid
        """
        try:
            if not test_case_id or not test_case_id.isdigit():
                raise ValueError("Test case ID must be a positive integer")
            
            logger.info(f"Fetching links for test case: {test_case_id}")
            data = self.api_client.get_test_cases_links(test_case_id, headers, project_uuid)
            
            requirement_ids = self._extract_requirement_ids(data)
            logger.info(f"Found {len(requirement_ids)} linked requirements for TC {test_case_id}")
            return requirement_ids
        except Exception as e:
            logger.error(f"Failed to fetch test case links for {test_case_id}: {str(e)}")
            raise
    
    def _extract_requirement_ids(self, link_data: Dict[str, Any]) -> List[str]:
        """
        Extract requirement IDs from link data structure.
        
        Args:
            link_data: Link data from API response
            
        Returns:
            List of requirement IDs
        """
        requirement_ids = []
        
        try:
            for link in link_data.get("linksData", []):
                name = link.get("linkDefinition", {}).get("name", "")
                
                # Skip shared test case steps
                if name == "Shared Test Case Steps":
                    continue
                
                # Extract requirement ID based on link type
                req_id = None
                if name == "Related Items":
                    peers = link.get("peers", [])
                    for peer in peers:
                        if peer.get("itemType") == "requirements":
                            req_id = peer.get("itemID")
                            break
                else:
                    parent = link.get("parentChildren", {}).get("parent")
                    if parent:
                        req_id = parent.get("itemID")
                
                if req_id:
                    requirement_ids.append(str(req_id))
            
            return requirement_ids
        except Exception as e:
            logger.error(f"Error extracting requirement IDs: {str(e)}")
            return []
    
    def get_requirement_details(
        self,
        requirement_id: str,
        headers: Dict[str, str],
        project_uuid: str
    ) -> Dict[str, Any]:
        """
        Fetch detailed information for a requirement.
        
        Args:
            requirement_id: ID of the requirement
            headers: HTTP headers with authentication
            project_uuid: UUID of the project
            
        Returns:
            Dictionary with requirement details (summary, description, etc.)
            
        Raises:
            Exception: If API request fails
        """
        try:
            logger.debug(f"Fetching details for requirement: {requirement_id}")
            details = self.api_client.get_req_description(requirement_id, headers, project_uuid)
            return details
        except Exception as e:
            logger.error(f"Failed to fetch requirement details for {requirement_id}: {str(e)}")
            raise
    
    def add_requirement_link(
        self,
        requirement_id: str,
        test_case_id: str,
        headers: Dict[str, str],
        project_uuid: str
    ) -> bool:
        """
        Create a link between a requirement and test case.
        
        Args:
            requirement_id: ID of the requirement
            test_case_id: ID of the test case
            headers: HTTP headers with authentication
            project_uuid: UUID of the project
            
        Returns:
            True if link created successfully
            
        Raises:
            Exception: If API request fails
        """
        try:
            logger.info(f"Creating link: Req {requirement_id} -> TC {test_case_id}")
            result = self.api_client.add_requirement_link_to_test_case(
                requirement_id,
                test_case_id,
                headers,
                project_uuid
            )
            logger.info(f"Link created successfully: Req {requirement_id} -> TC {test_case_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create link: {str(e)}")
            raise
