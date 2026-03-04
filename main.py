"""
Main entry point for ShowTestCaseLinkedReq application
A PyQt6 desktop application for managing Helix ALM test cases and requirements
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Application exit code
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.setFixedSize(1700, 800)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
