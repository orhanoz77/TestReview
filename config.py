"""
Configuration management for ShowTestCaseLinkedReq
Loads configuration from environment variables or uses default values
"""

import os
from typing import Dict, Any

# ============================================================================
# API Configuration
# ============================================================================

# Helix ALM API Base URL
HELIX_ALM_BASE_URL: str = os.getenv(
    'HELIX_ALM_BASE_URL',
    'https://10.214.41.6:8443/helix-alm/api/v0/'
)

# API Request timeout (seconds)
API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '30'))

# SSL Certificate verification (set to 'true' for production)
API_VERIFY_SSL: bool = os.getenv('API_VERIFY_SSL', 'false').lower() == 'true'

# ============================================================================
# Application Configuration
# ============================================================================

# Application name
APP_NAME: str = 'ShowTestCaseLinkedReq'

# Organization name for QSettings
ORGANIZATION_NAME: str = 'ShowTestCaseLinkedReq'

# Application display name
APP_DISPLAY_NAME: str = 'Test Case Requirement Linker'

# ============================================================================
# UI Configuration
# ============================================================================

# Main window dimensions
MAIN_WINDOW_WIDTH: int = int(os.getenv('MAIN_WINDOW_WIDTH', '1600'))
MAIN_WINDOW_HEIGHT: int = int(os.getenv('MAIN_WINDOW_HEIGHT', '900'))

# Table column widths
TABLE_DESC_COLUMN_WIDTH: int = int(os.getenv('TABLE_DESC_COLUMN_WIDTH', '350'))
TABLE_DISC_COLUMN_WIDTH: int = int(os.getenv('TABLE_DISC_COLUMN_WIDTH', '350'))

# ============================================================================
# Threading Configuration
# ============================================================================

# Maximum number of worker threads for parallel requirement fetching
MAX_WORKER_THREADS: int = int(os.getenv('MAX_WORKER_THREADS', '8'))

# Minimum number of worker threads
MIN_WORKER_THREADS: int = int(os.getenv('MIN_WORKER_THREADS', '1'))

# ============================================================================
# Requirement Prefixes
# ============================================================================

# Valid requirement type prefixes
REQUIREMENT_PREFIXES: tuple = (
    'SYS',      # System Requirement
    'SW',       # Software Requirement
    'SWDD',     # Software Design Decision
    'CNST',     # Constant
)

# ============================================================================
# Logging Configuration
# ============================================================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

# Log file path (empty string means no file logging)
LOG_FILE: str = os.getenv('LOG_FILE', '')

# Log format
LOG_FORMAT: str = os.getenv(
    'LOG_FORMAT',
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# UI Styling
# ============================================================================

MAIN_STYLESHEET: str = """
    QGroupBox { font-weight: 600; }
    QTableWidget { gridline-color: #d0d0d0; }
    QHeaderView::section { font-weight: 600; padding: 6px; }
    QPushButton { padding: 6px 10px; }
"""

# ============================================================================
# Status Messages
# ============================================================================

STATUS_MESSAGES: Dict[str, str] = {
    'login_captured': 'Login data captured',
    'project_selected': 'Project selected',
    'projects_loaded': 'Projects loaded',
    'tcp_loading': 'Loading test case links...',
    'details_loaded': 'Requirement details loaded',
    'links_loaded': 'Test case links loaded',
    'no_tag': 'No TAG available',
    'error_prefix': 'Error: ',
}

# Status message duration (milliseconds)
STATUS_MESSAGE_DURATION: int = 3000

# ============================================================================
# Error Messages
# ============================================================================

ERROR_MESSAGES: Dict[str, str] = {
    'login_required': 'Please login',
    'select_project': 'Please select a project first',
    'project_required': 'Please select a project first',
    'enter_credentials': 'Please enter both username and password.',
    'invalid_token': 'Invalid ACCESS_TOKEN or UUID',
    'project_not_found': 'Selected project not found in project list',
    'invalid_tc_id': 'Test Case ID must be a positive integer.',
    'no_requirements': 'No requirement IDs found to fetch.',
    'failed_login': 'Failed to retrieve authentication token',
}

# ============================================================================
# Validation Configuration
# ============================================================================

# Minimum test case ID value
MIN_TEST_CASE_ID: int = 1

# ============================================================================
# Function to get configuration summary
# ============================================================================

def get_config_summary() -> Dict[str, Any]:
    """
    Get a summary of current configuration.
    
    Returns:
        Dictionary with configuration details
    """
    return {
        'api': {
            'base_url': HELIX_ALM_BASE_URL,
            'timeout': API_TIMEOUT,
            'verify_ssl': API_VERIFY_SSL,
        },
        'ui': {
            'window_width': MAIN_WINDOW_WIDTH,
            'window_height': MAIN_WINDOW_HEIGHT,
        },
        'threading': {
            'max_workers': MAX_WORKER_THREADS,
            'min_workers': MIN_WORKER_THREADS,
        },
        'logging': {
            'level': LOG_LEVEL,
            'file': LOG_FILE or 'console only',
        },
    }
