"""
Main entry point for ShowTestCaseLinkedReq application
A PyQt6 desktop application for managing Helix ALM test cases and requirements
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from logging_config import configure_logging
from ui import MainWindow

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Application exit code
    """
    # Configure logging
    configure_logging()
    logger.info("Starting ShowTestCaseLinkedReq application")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.setFixedSize(1700, 800)
    window.show()
    logger.debug("Main window displayed")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
