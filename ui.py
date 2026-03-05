"""
MainWindow UI controller for ShowTestCaseLinkedReq
Handles user interactions and API communication
"""

import base64
import time
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
from PyQt6.QtCore import Qt, QSettings, QTimer, QObject, pyqtSignal, QRunnable, QThreadPool
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractItemView, QMessageBox
from bs4 import BeautifulSoup
from helix_api_client import HelixAPIClient
from main_window import Ui_MainWindow
from session_manager import SessionManager
from services import AuthenticationService, ProjectService, RequirementService
from PyQt6.QtGui import QPixmap, QIcon
import requests
import os

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Constants
REQUIREMENT_PREFIXES = ("SYS", "SW", "SWDD", "CNST")

# ---------------- Worker infrastructure ----------------

class WorkerSignals(QObject):
    """Signals emitted by worker threads"""
    row_ready = pyqtSignal(str, str, str, str)   # tag, summary, desc, discussions
    progress_tick = pyqtSignal(int)              # +1 per completed fetch
    error = pyqtSignal(str)
    finished = pyqtSignal()

class ReqBatchWorker(QRunnable):
    """Worker thread for fetching requirement details in batch"""
    
    def __init__(self, ids: List[str], headers: Dict[str, str], uuid: str, api_client: HelixAPIClient) -> None:
        """
        Initialize the batch worker.
        
        Args:
            ids: List of requirement IDs to fetch
            headers: HTTP headers with authentication
            uuid: Project UUID
            api_client: Instance of HelixAPIClient
        """
        super().__init__()
        self.ids = ids
        self.headers = headers
        self.uuid = uuid
        self.api_client = api_client
        self.signals = WorkerSignals()

    def run(self) -> None:
        """Execute the worker thread task"""
        try:
            # Session per worker -> connection reuse without thread-safety problems
            with requests.Session() as sess:
                sess.verify = False
                for rid in self.ids:
                    try:
                        data = self.api_client.get_req_description(rid, self.headers, self.uuid, session=sess)
                        tag = data.get('tag', 'No TAG available')
                        summary = next((f['string'] for f in data['fields'] if f['label'] == 'Summary'), 'No Summary available')
                        description_html = next((f['formattedString']['text'] for f in data['fields'] if f['label'] == 'Description'), 'No Description available')
                        soup = BeautifulSoup(description_html, 'html.parser')
                        if soup.find('img'):
                            description_text = "Requirement contains image, please check Helix"
                        else:
                            description_text = soup.get_text()
                        discussions = []
                        discussions_field_found = False
                        for field in data['fields']:
                            if field['label'] == 'Discussion':
                                discussions_field_found = True
                                discussions.append(BeautifulSoup(field['formattedString']['text'], 'html.parser').get_text())
                        if discussions_field_found:
                            discussions_text = "\n".join(discussions) if discussions else "No Discussion available"
                        else:
                            discussions_text = "Field does not exist"
                        self.signals.row_ready.emit(tag, summary, description_text, discussions_text)
                        self.signals.progress_tick.emit(1)
                    except Exception as e:
                        self.signals.error.emit(str(e))
                        self.signals.progress_tick.emit(1)
        finally:
            self.signals.finished.emit()

class MainWindow(QMainWindow, Ui_MainWindow):
    """Main application window"""
    
    def __init__(self) -> None:
        """Initialize the main window"""
        super().__init__()
        self.setupUi(self)

        # Styling
        self.setStyleSheet("""
            QGroupBox { font-weight: 600; }
            QTableWidget { gridline-color: #d0d0d0; }
            QHeaderView::section { font-weight: 600; padding: 6px; }
            QPushButton { padding: 6px 10px; }
        """)

        # Connections
        self.pushButton_GetProjects.clicked.connect(self.on_submit)
        self.pushButton_connectToHelixServer.clicked.connect(self.getUserInformation)
        self.pushButton_getTCLinks.clicked.connect(self.getTCLinks)
        self.pushButton_GetReqDesc.clicked.connect(self.read_table_items)

        self.lineEdit_testCaseNumber.returnPressed.connect(self.getTCLinks)
        self.lineEdit_password.returnPressed.connect(self.getUserInformation)
        self.lineEdit_userName_2.textChanged.connect(self.filter_table)
        self.comboBox_projectList.currentIndexChanged.connect(self.updateToken_UUID)

        # Progress bars
        self.progress_bar_projects.hide()
        self.progress_bar_get_tc_links.hide()
        self.progress_bar_get_req_desc.hide()

        # Table setup
        self.tableWidget_existingTCLinks.setColumnCount(1)
        self.tableWidget_existingTCLinks.setHorizontalHeaderLabels(["Linked requirements"])
        self.tableWidget_existingTCLinks.horizontalHeader().setStretchLastSection(True)

        self.tableWidget_ReqInfo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tableWidget_ReqInfo.setAlternatingRowColors(True)
        self.tableWidget_ReqInfo.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.pushButton_SaveCredentials.clicked.connect(self.save_credentials)
        self.load_credentials()

        # Session management and API Client
        self.session: SessionManager = SessionManager()
        self.api_client: HelixAPIClient = HelixAPIClient()
        
        # Initialize services (business logic layer)
        self.auth_service: AuthenticationService = AuthenticationService(self.session, self.api_client)
        self.project_service: ProjectService = ProjectService(self.session, self.api_client)
        self.requirement_service: RequirementService = RequirementService(self.api_client)

        # Thread pool
        self.threadpool: QThreadPool = QThreadPool.globalInstance()
        self._pending_total: int = 0
        self._pending_done: int = 0
        self._pending_workers: int = 0

    # ---------- Credentials ----------
    def save_credentials(self) -> None:
        """Save credentials to QSettings"""
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("username", self.lineEdit_userName.text())
        settings.setValue("password", self.lineEdit_password.text())

    def load_credentials(self) -> None:
        """Load credentials from QSettings"""
        settings = QSettings("MyCompany", "MyApp")
        self.lineEdit_userName.setText(settings.value("username", ""))
        self.lineEdit_password.setText(settings.value("password", ""))

    def show_message(self, title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Icon.Warning) -> None:
        """
        Show message dialog to user.
        
        Args:
            title: Dialog title
            message: Message text
            icon: Message icon type
        """
        QMessageBox(icon, title, message, parent=self).exec()

    # ---------- Auth / Projects ----------
    def getUserInformation(self) -> None:
        """Capture login information from UI"""
        username = self.lineEdit_userName.text()
        password = self.lineEdit_password.text()

        if self.auth_service.login(username, password):
            self.statusBar().showMessage("Login data captured", 3000)
            logger.debug("Login successful, credentials set in session")
        else:
            logger.warning("Login attempt failed")
            self.show_message("Input Error", "Please enter both username and password.")

    def updateToken_UUID(self) -> None:
        """Update project token and UUID when project selection changes"""
        self.progress_bar_projects.setValue(0)
        self.progress_bar_projects.show()

        try:
            current_project = self.comboBox_projectList.currentText()
            logger.debug(f"Updating token/UUID for project: {current_project}")
            self.progress_bar_projects.setValue(50)
            
            # Use project service to select project with Basic Auth
            self.project_service.select_project(
                current_project,
                self.auth_service.get_basic_headers()
            )
            
            self.tableWidget_existingTCLinks.setRowCount(0)
            self.tableWidget_ReqInfo.setRowCount(0)
            self.lineEdit_testCaseNumber.clear()
            self.progress_bar_projects.setValue(100)
            self.statusBar().showMessage("Project selected", 3000)
            logger.info(f"Project token and UUID updated successfully: {current_project}")
        except Exception as e:
            logger.error(f"Error updating token/UUID: {str(e)}")
            self.progress_bar_projects.setValue(0)
            self.show_message("Error", str(e), QMessageBox.Icon.Critical)
        finally:
            self.progress_bar_projects.hide()

    def on_submit(self) -> None:
        """Load and display available projects"""
        if not self.auth_service.is_authenticated():
            logger.warning("Project load attempt without authentication")
            self.show_message("Error", "Please login")
            return

        logger.info("Loading projects from API")
        self.progress_bar_projects.setValue(0)
        self.progress_bar_projects.show()

        def safe_step(func):
            def wrapper():
                try:
                    func()
                except Exception as e:
                    logger.error(f"Error in project loading step: {str(e)}")
                    self.progress_bar_projects.setValue(0)
                    self.progress_bar_projects.hide()
                    self.show_message("Error", str(e), QMessageBox.Icon.Critical)
            return wrapper

        def step1():
            self.progress_bar_projects.setValue(20)

        def step2():
            # Use project service to load projects with Basic Auth headers
            projects = self.project_service.load_projects(
                self.auth_service.get_basic_headers()
            )
            self.progress_bar_projects.setValue(50)
            try:
                self.comboBox_projectList.currentIndexChanged.disconnect()
            except Exception:
                pass
            self.comboBox_projectList.clear()
            self.comboBox_projectList.addItems(projects.keys())
            self.comboBox_projectList.currentIndexChanged.connect(self.updateToken_UUID)
            logger.debug(f"Projects loaded: {len(projects)} projects found")

        def step3():
            self.progress_bar_projects.setValue(70)
            current_project = self.comboBox_projectList.currentText()
            # Use project service to select project with Basic Auth
            self.project_service.select_project(
                current_project,
                self.auth_service.get_basic_headers()
            )

        def finish():
            self.progress_bar_projects.setValue(100)
            self.progress_bar_projects.hide()
            self.statusBar().showMessage("Projects loaded", 3000)
            logger.info("Projects loaded and displayed successfully")

        QTimer.singleShot(50, safe_step(step1))
        QTimer.singleShot(100, safe_step(step2))
        QTimer.singleShot(150, safe_step(step3))
        QTimer.singleShot(200, safe_step(finish))

    # ---------- Requirement details (parallel) ----------
    def _on_worker_row(self, tag: str, summary: str, description: str, discussions: str) -> None:
        """
        Handle worker signal for requirement row data.
        
        Args:
            tag: Requirement tag
            summary: Requirement summary
            description: Requirement description
            discussions: Requirement discussions
        """
        # Buffer rows quickly without resizing every time for speed
        if self.tableWidget_ReqInfo.columnCount() == 0:
            self.tableWidget_ReqInfo.setColumnCount(4)
            self.tableWidget_ReqInfo.setHorizontalHeaderLabels(["TAG", "Summary", "Description", "Discussions"])

        row = self.tableWidget_ReqInfo.rowCount()
        self.tableWidget_ReqInfo.insertRow(row)
        self.tableWidget_ReqInfo.setItem(row, 0, QTableWidgetItem(tag))
        self.tableWidget_ReqInfo.setItem(row, 1, QTableWidgetItem(summary))

        desc_item = QTableWidgetItem(description)
        desc_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        desc_item.setFlags(desc_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.tableWidget_ReqInfo.setItem(row, 2, desc_item)

        disc_item = QTableWidgetItem(discussions)
        disc_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        disc_item.setFlags(disc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.tableWidget_ReqInfo.setItem(row, 3, disc_item)

        # progress
        self._pending_done += 1
        percent = int((self._pending_done / max(1, self._pending_total)) * 100)
        self.progress_bar_get_req_desc.setValue(percent)

    def _on_worker_error(self, msg: str) -> None:
        """
        Handle worker error signal.
        
        Args:
            msg: Error message
        """
        logger.error(f"Worker error: {msg}")
        # Log to status bar; avoid modal dialogs during bulk load
        self.statusBar().showMessage(f"Error: {msg}", 5000)

    def _on_worker_finished(self) -> None:
        """Handle worker finished signal"""
        self._pending_workers -= 1
        if self._pending_workers <= 0:
            logger.info(f"All workers finished, displaying {self._pending_done} requirement details")
            # Finalize table sizing once
            self.tableWidget_ReqInfo.resizeColumnToContents(0)
            self.tableWidget_ReqInfo.resizeColumnToContents(1)
            self.tableWidget_ReqInfo.setColumnWidth(2, 350)
            self.tableWidget_ReqInfo.setColumnWidth(3, 350)
            self.tableWidget_ReqInfo.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.tableWidget_ReqInfo.resizeRowsToContents()
            self.progress_bar_get_req_desc.hide()
            self.statusBar().showMessage("Requirement details loaded", 3000)

    def read_table_items(self) -> None:
        """Fetch and display requirement details for all linked test case requirements"""
        if not self.session.is_project_selected():
            logger.warning("Attempt to read table items without project selection")
            self.show_message("Error", "Please select a project first")
            return

        # Collect unique req IDs
        ids: List[str] = []
        seen: set = set()
        rows = self.tableWidget_existingTCLinks.rowCount()
        for r in range(rows):
            item = self.tableWidget_existingTCLinks.item(r, 0)
            if item:
                rid = item.text().strip()
                if rid and rid not in seen:
                    seen.add(rid)
                    ids.append(rid)

        if not ids:
            logger.warning("No requirement IDs found to fetch")
            QMessageBox.warning(self, "Warning", "No requirement IDs found to fetch.")
            return

        logger.info(f"Starting parallel fetch of requirement details for {len(ids)} requirements")
        # Reset table and progress
        self.tableWidget_ReqInfo.setRowCount(0)
        self.progress_bar_get_req_desc.setValue(0)
        self.progress_bar_get_req_desc.show()

        # Threading plan: split into N chunks
        thread_count = min(8, max(1, len(ids)))
        chunk_size = max(1, len(ids) // thread_count)
        chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
        logger.debug(f"Created {len(chunks)} worker threads for requirement fetching")

        self._pending_total = len(ids)
        self._pending_done = 0
        self._pending_workers = len(chunks)

        # Launch workers
        for chunk in chunks:
            worker = ReqBatchWorker(chunk, self.session.get_bearer_headers(), self.session.uuid, self.api_client)
            worker.signals.row_ready.connect(self._on_worker_row)
            worker.signals.error.connect(self._on_worker_error)
            worker.signals.finished.connect(self._on_worker_finished)
            self.threadpool.start(worker)

    # ---------- Test case links ----------
    def get_req_Tag(self, reqId: str) -> Optional[str]:
        """
        Get requirement tag by ID.
        
        Args:
            reqId: Requirement ID
            
        Returns:
            Requirement tag or None if error
        """
        if not self.session.is_project_selected():
            self.show_message("Error", "Invalid ACCESS_TOKEN or UUID")
            return None
        headers = self.session.get_bearer_headers()
        req_desc = self.api_client.get_req_description(reqId, headers, self.session.uuid)
        return req_desc.get('tag', 'No TAG available')

    def getTCLinks(self) -> None:
        """Fetch and display test case links for entered test case ID"""
        if not self.auth_service.is_project_selected():
            logger.warning("Attempt to get TC links without project selection")
            self.show_message("Error", "Please log in first.", QMessageBox.Icon.Warning)
            return

        test_case_id = self.lineEdit_testCaseNumber.text().strip()
        if not test_case_id.isdigit() or int(test_case_id) <= 0:
            logger.warning(f"Invalid test case ID: {test_case_id}")
            self.show_message("Input Error", "Test Case ID must be a positive integer.")
            return

        logger.info(f"Fetching links for test case: {test_case_id}")
        self.tableWidget_ReqInfo.setRowCount(0)
        self.progress_bar_get_tc_links.setValue(0)
        self.progress_bar_get_tc_links.show()

        try:
            # Use requirement service to get test case links
            req_list = self.requirement_service.get_test_case_links(
                test_case_id,
                self.auth_service.get_bearer_headers(),
                self.session.uuid
            )

            self.tableWidget_existingTCLinks.setRowCount(len(req_list))
            for row, rid in enumerate(req_list):
                self.tableWidget_existingTCLinks.setItem(row, 0, QTableWidgetItem(str(rid)))

            self.progress_bar_get_tc_links.setValue(100)
            self.progress_bar_get_tc_links.hide()
            logger.info(f"Test case links fetched successfully: {len(req_list)} requirements found")
        except Exception as e:
            logger.error(f"Error fetching test case links for ID {test_case_id}: {str(e)}")
            self.progress_bar_get_tc_links.setValue(0)
            self.progress_bar_get_tc_links.hide()
            self.show_message("Error", str(e), QMessageBox.Icon.Critical)

    # ---------- Filtering ----------
    def filter_table(self) -> None:
        """Filter requirement table based on search text"""
        filter_text = self.lineEdit_userName_2.text().lower()
        for row in range(self.tableWidget_ReqInfo.rowCount()):
            match = False
            for col in range(self.tableWidget_ReqInfo.columnCount()):
                item = self.tableWidget_ReqInfo.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.tableWidget_ReqInfo.setRowHidden(row, not match)
