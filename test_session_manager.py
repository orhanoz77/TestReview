"""
Unit tests for SessionManager
"""

from session_manager import SessionManager


def test_session_manager_credentials():
    """Test setting and retrieving credentials."""
    session = SessionManager()
    
    # Test initial state
    assert not session.is_authenticated()
    assert not session.is_project_selected()
    
    # Set credentials
    session.set_credentials("testuser", "testpass")
    assert session.username == "testuser"
    assert session.password == "testpass"
    assert session.is_authenticated()
    assert "Authorization" in session.headers
    assert "Basic" in session.headers["Authorization"]
    print("✓ Credentials test passed")


def test_session_manager_project():
    """Test setting and retrieving project information."""
    session = SessionManager()
    
    # Set projects
    projects = {"Project1": "uuid-1", "Project2": "uuid-2"}
    session.set_projects(projects)
    
    assert session.get_project_uuid("Project1") == "uuid-1"
    assert session.get_project_uuid("Project2") == "uuid-2"
    assert session.get_project_uuid("NonExistent") is None
    print("✓ Project lookup test passed")


def test_session_manager_project_selection():
    """Test project selection with token."""
    session = SessionManager()
    
    # Set project
    session.set_project("test-uuid", "test-token")
    assert session.uuid == "test-uuid"
    assert session.access_token == "test-token"
    assert session.is_project_selected()
    
    # Get bearer headers
    headers = session.get_bearer_headers()
    assert "Authorization" in headers
    assert "Bearer test-token" in headers["Authorization"]
    print("✓ Project selection test passed")


def test_session_manager_bearer_token():
    """Test bearer token setting."""
    session = SessionManager()
    session.set_bearer_token("my-token")
    
    assert session.access_token == "my-token"
    headers = session.get_bearer_headers()
    assert headers["Authorization"] == "Bearer my-token"
    print("✓ Bearer token test passed")


def test_session_manager_clear():
    """Test clearing session data."""
    session = SessionManager()
    session.set_credentials("user", "pass")
    session.set_projects({"P1": "uuid"})
    session.set_project("uuid", "token")
    
    assert session.is_authenticated()
    assert session.is_project_selected()
    
    session.clear()
    assert not session.is_authenticated()
    assert not session.is_project_selected()
    assert session.username == ""
    assert session.password == ""
    assert session.uuid == ""
    assert session.access_token == ""
    print("✓ Clear test passed")


if __name__ == "__main__":
    test_session_manager_credentials()
    test_session_manager_project()
    test_session_manager_project_selection()
    test_session_manager_bearer_token()
    test_session_manager_clear()
    print("\n✅ All SessionManager tests passed!")
