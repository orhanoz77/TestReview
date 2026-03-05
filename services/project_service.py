"""
Project Service
Handles project selection and management
"""

import logging
from typing import Dict, Optional
from session_manager import SessionManager
from helix_api_client import HelixAPIClient

logger = logging.getLogger(__name__)


class ProjectService:
    """Service for managing projects and project selection."""
    
    def __init__(self, session: SessionManager, api_client: HelixAPIClient) -> None:
        """
        Initialize project service.
        
        Args:
            session: SessionManager instance for storing project data
            api_client: HelixAPIClient instance for API communication
        """
        self.session = session
        self.api_client = api_client
    
    def load_projects(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Fetch and load available projects from API.
        
        Args:
            headers: HTTP headers with authentication
            
        Returns:
            Dictionary mapping project names to UUIDs
            
        Raises:
            Exception: If API request fails
        """
        try:
            logger.info("Fetching projects from API")
            projects = self.api_client.get_project_list(headers)
            self.session.set_projects(projects)
            logger.info(f"Loaded {len(projects)} projects")
            return projects
        except Exception as e:
            logger.error(f"Failed to load projects: {str(e)}")
            raise
    
    def select_project(self, project_name: str, headers: Dict[str, str]) -> bool:
        """
        Select a project and fetch its authentication token.
        
        Args:
            project_name: Name of the project to select
            headers: HTTP headers with authentication
            
        Returns:
            True if project selected successfully
            
        Raises:
            Exception: If project not found or token retrieval fails
        """
        try:
            logger.debug(f"Selecting project: {project_name}")
            project_uuid = self.session.get_project_uuid(project_name)
            if not project_uuid:
                raise Exception(f"Project not found: {project_name}")
            
            logger.debug(f"Fetching token for project: {project_name}")
            access_token = self.api_client.get_authentication_token(project_uuid, headers)
            self.session.set_project(project_uuid, access_token)
            logger.info(f"Project selected: {project_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to select project: {str(e)}")
            raise
    
    def get_projects(self) -> Dict[str, str]:
        """
        Get currently loaded projects.
        
        Returns:
            Dictionary of projects (name -> UUID)
        """
        return self.session.project_dict
    
    def get_current_project_uuid(self) -> Optional[str]:
        """
        Get the UUID of currently selected project.
        
        Returns:
            Project UUID or None if no project selected
        """
        return self.session.uuid if self.session.is_project_selected() else None
    
    def is_project_selected(self) -> bool:
        """
        Check if a project is currently selected.
        
        Returns:
            True if project is selected
        """
        return self.session.is_project_selected()
