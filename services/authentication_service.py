"""
Authentication Service
Handles user authentication and token management
"""

import logging
from typing import Dict
from session_manager import SessionManager
from helix_api_client import HelixAPIClient

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Service for managing user authentication and credentials."""
    
    def __init__(self, session: SessionManager, api_client: HelixAPIClient) -> None:
        """
        Initialize authentication service.
        
        Args:
            session: SessionManager instance for storing credentials
            api_client: HelixAPIClient instance for API communication
        """
        self.session = session
        self.api_client = api_client
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user with credentials.
        
        Args:
            username: Helix ALM username
            password: Helix ALM password
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if not username or not password:
                logger.warning("Login attempt with empty credentials")
                return False
            
            logger.info(f"Authenticating user: {username}")
            self.session.set_credentials(username, password)
            logger.info(f"User authenticated: {username}")
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated.
        
        Returns:
            True if authenticated with valid credentials
        """
        return self.session.is_authenticated()
    
    def is_project_selected(self) -> bool:
        """
        Check if a project is selected.
        
        Returns:
            True if project UUID and token are set
        """
        return self.session.is_project_selected()
    
    def get_basic_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with Basic Auth for API requests.
        
        Returns:
            Dictionary with Basic authorization header
        """
        return self.session.headers
    
    def get_bearer_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with Bearer token for API requests.
        
        Returns:
            Dictionary with authorization header
        """
        return self.session.get_bearer_headers()
    
    def logout(self) -> None:
        """Clear all session data."""
        self.session.clear()
        logger.info("User logged out")
