"""
Logging Configuration
Configures structured logging for ShowTestCaseLinkedReq application
"""

import logging
import os
from typing import Optional


# Logging constants
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE: Optional[str] = os.getenv('LOG_FILE', None)
LOG_FORMAT: str = os.getenv(
    'LOG_FORMAT',
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log levels mapping
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}


def configure_logging() -> None:
    """
    Configure logging for the application.
    Sets up console and optional file logging with specified level and format.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if LOG_FILE is specified)
    if LOG_FILE:
        try:
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except (IOError, OSError) as e:
            console_handler.emit(
                logging.LogRecord(
                    'logging_config',
                    logging.WARNING,
                    '',
                    0,
                    f'Failed to create log file {LOG_FILE}: {e}',
                    (),
                    None
                )
            )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance for the specified module
    """
    return logging.getLogger(name)
