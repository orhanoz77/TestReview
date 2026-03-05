"""
Session Manager for Helix ALM Application
Manages authentication state, credentials, and API session data.
"""

import base64
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages user session state and authentication credentials."""
    
    def __init__(self):
        self.username: str = ""
        self.password: str = ""
        self.headers: Dict[str, str] = {}
        self.uuid: str = ""
        self.access_token: str = ""
        self.project_dict: Dict[str, str] = {}
    
    def set_credentials(self, username: str, password: str) -> None:
        """
        Set user credentials and generate Basic Auth header.
        
        Args:
            username: Helix ALM username
            password: Helix ALM password
        """
        self.username = username
        self.password = password
        logger.info(f"Credentials set for user: {username}")
        
        # Generate Basic Auth header
        auth_str = f"{username}:{password}"
        auth_bytes = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        self.headers = {'Authorization': f'Basic {auth_bytes}'}
        logger.debug("Basic Auth header generated")
    
    def set_bearer_token(self, access_token: str) -> None:
        """
        Set Bearer token for API authentication.
        
        Args:
            access_token: API access token from Helix ALM
        """
        self.access_token = access_token
    
    def get_bearer_headers(self) -> Dict[str, str]:
        """
        Get headers with Bearer token.
        
        Returns:
            Dict with Bearer token authorization header
        """
        return {'Authorization': f'Bearer {self.access_token}'}
    
    def set_project(self, uuid: str, access_token: str) -> None:
        """
        Set current selected project UUID and access token.
        
        Args:
            uuid: Project UUID from Helix ALM
            access_token: API access token for this project
        """
        self.uuid = uuid
        self.access_token = access_token
        logger.info(f"Project selected: {uuid}")
    
    def set_projects(self, projects: Dict[str, str]) -> None:
        """
        Set available projects mapping.
        
        Args:
            projects: Dict mapping project names to UUIDs
        """
        self.project_dict = projects
    
    def get_project_uuid(self, project_name: str) -> Optional[str]:
        """
        Get UUID for a project by name.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Project UUID or None if not found
        """
        return self.project_dict.get(project_name)
    
    def is_authenticated(self) -> bool:
        """Check if user has valid credentials."""
        return bool(self.username and self.password and self.headers)
    
    def is_project_selected(self) -> bool:
        """Check if a project UUID and token are set."""
        return bool(self.uuid and self.access_token)
    
    def clear(self) -> None:
        """Clear all session data."""
        self.username = ""
        self.password = ""
        self.headers = {}
        self.uuid = ""
        self.access_token = ""
        self.project_dict = {}
