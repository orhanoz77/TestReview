"""
Unit tests for HelixAPIClient
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from helix_api_client import HelixAPIClient


class TestHelixAPIClient(unittest.TestCase):
    """Test cases for HelixAPIClient"""
    
    def setUp(self):
        """Set up test client"""
        self.client = HelixAPIClient()
        self.headers = {'Authorization': 'Basic test_auth'}
        self.uuid = 'test-uuid-12345'
    
    @patch('helix_api_client.requests.Session.get')
    def test_get_project_list_success(self, mock_get):
        """Test successful project list retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'projects': [
                {'name': 'Project1', 'uuid': 'uuid1'},
                {'name': 'Project2', 'uuid': 'uuid2'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.client.get_project_list(self.headers)
        
        self.assertEqual(result, {'Project1': 'uuid1', 'Project2': 'uuid2'})
        mock_get.assert_called_once()
    
    @patch('helix_api_client.requests.Session.get')
    def test_get_test_cases_links_success(self, mock_get):
        """Test successful test case links retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {'linksData': [{'name': 'test_link'}]}
        mock_get.return_value = mock_response
        
        result = self.client.get_test_cases_links('123', self.headers, self.uuid)
        
        self.assertEqual(result, {'linksData': [{'name': 'test_link'}]})
        mock_get.assert_called_once()
    
    @patch('helix_api_client.requests.Session.post')
    def test_add_requirement_link_success(self, mock_post):
        """Test successful requirement link creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'link_id_123'}
        mock_post.return_value = mock_response
        
        result = self.client.add_requirement_link_to_test_case('req1', 'tc1', self.headers, self.uuid)
        
        self.assertEqual(result, {'id': 'link_id_123'})
        mock_post.assert_called_once()
    
    @patch('helix_api_client.requests.Session.get')
    def test_get_req_description_success(self, mock_get):
        """Test successful requirement description retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {'tag': 'SW-001', 'fields': []}
        mock_get.return_value = mock_response
        
        result = self.client.get_req_description('req1', self.headers, self.uuid)
        
        self.assertEqual(result['tag'], 'SW-001')
        mock_get.assert_called_once()
    
    @patch('helix_api_client.requests.Session.get')
    def test_get_authentication_token_success(self, mock_get):
        """Test successful token retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {'accessToken': 'token123'}
        mock_get.return_value = mock_response
        
        result = self.client.get_authentication_token(self.uuid, self.headers)
        
        self.assertEqual(result, 'token123')
        mock_get.assert_called_once()
    
    @patch('helix_api_client.requests.Session.post')
    def test_get_record_id_success(self, mock_post):
        """Test successful record ID search"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'requirements': [{'id': 'req_id_123'}]
        }
        mock_post.return_value = mock_response
        
        result = self.client.get_record_id('123', self.headers, self.uuid)
        
        self.assertEqual(result, 'req_id_123')
        mock_post.assert_called_once()
    
    @patch('helix_api_client.requests.Session.get')
    def test_get_authentication_token_failure(self, mock_get):
        """Test failed token retrieval"""
        mock_get.side_effect = Exception("Network error")
        
        with self.assertRaises(Exception):
            self.client.get_authentication_token(self.uuid, self.headers)
    
    def test_close_session(self):
        """Test session closure"""
        self.client.close()
        # If no exception, test passes
        self.assertTrue(True)
    
    def test_context_manager(self):
        """Test context manager support"""
        try:
            with HelixAPIClient() as client:
                self.assertIsNotNone(client)
        except Exception as e:
            self.fail(f"Context manager failed: {str(e)}")
    
    def test_client_initialization(self):
        """Test client initialization with custom parameters"""
        client = HelixAPIClient(
            base_url='https://custom.url/',
            verify_ssl=True,
            timeout=60
        )
        self.assertEqual(client.base_url, 'https://custom.url/')
        self.assertTrue(client.verify_ssl)
        self.assertEqual(client.timeout, 60)


if __name__ == '__main__':
    # Run tests with verbose output
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHelixAPIClient)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print(f"[PASS] All {result.testsRun} tests passed!")
    else:
        print(f"[FAIL] {len(result.failures)} failures, {len(result.errors)} errors")
