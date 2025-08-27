
import base64
import time
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout
from bs4 import BeautifulSoup
from api import *
from auth import get_authentication_token
from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QHeaderView, QSizePolicy,QLabel,QAbstractItemView
from PyQt6.QtWidgets import QMessageBox, QProgressBar
from PyQt6.QtCore import QTimer
from main_window import Ui_MainWindow  # Import the converted UI file
from io import BytesIO
import base64
import re
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QTableWidgetItem
from bs4 import BeautifulSoup
import imageio
import os  # For file saving

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Light styling improvements for readability
        self.setStyleSheet("""
        QGroupBox { font-weight: 600; }
        QTableWidget { gridline-color: #d0d0d0; }
        QHeaderView::section { font-weight: 600; padding: 6px; }
        QPushButton { padding: 6px 10px; }
        """)

        # PUSH BUTTONS
        self.pushButton_GetProjects.clicked.connect(self.on_submit)
        self.pushButton_connectToHelixServer.clicked.connect(self.getUserInformation)
        self.pushButton_getTCLinks.clicked.connect(self.getTCLinks)
        self.pushButton_GetReqDesc.clicked.connect(self.read_table_items)

        self.lineEdit_testCaseNumber.returnPressed.connect(self.getTCLinks)
        self.lineEdit_password.returnPressed.connect(self.getUserInformation)
        self.lineEdit_userName_2.textChanged.connect(self.filter_table)

        #Combobox
        self.comboBox_projectList.currentIndexChanged.connect(self.updateToken_UUID)

        #Progress Bars
        self.progress_bar_projects.hide()
        self.progress_bar_get_tc_links.hide()
        self.progress_bar_get_req_desc.hide()

        self.tableWidget_existingTCLinks.setColumnCount(1)
        self.tableWidget_existingTCLinks.setHorizontalHeaderLabels(["Linked requirements"])
        header  = self.tableWidget_existingTCLinks.horizontalHeader()
        header.setStretchLastSection(True)

        self.tableWidget_ReqInfo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tableWidget_ReqInfo.setAlternatingRowColors(True)
        self.tableWidget_ReqInfo.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.pushButton_SaveCredentials.clicked.connect(self.save_credentials)
        self.load_credentials()

    def save_credentials(self):
        settings = QSettings("MyCompany", "MyApp")  # Replace with your app details
        settings.setValue("username", self.lineEdit_userName.text())
        settings.setValue("password", self.lineEdit_password.text())

    def load_credentials(self):
        settings = QSettings("MyCompany", "MyApp")
        username = settings.value("username", "")
        password = settings.value("password", "")
        self.lineEdit_userName.setText(username)
        self.lineEdit_password.setText(password)

    def show_message(self, title, message, icon=QMessageBox.Icon.Warning,progress_bar=None):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

    def getUserInformation(self):
        global USERNAME, PASSWORD, HEADERS
        USERNAME = self.lineEdit_userName.text()
        PASSWORD = self.lineEdit_password.text()

        if USERNAME and PASSWORD:
            auth_str = f"{USERNAME}:{PASSWORD}"
            auth_str = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            HEADERS = {'Authorization': f'Basic {auth_str}'}
            self.statusBar().showMessage("Login data captured", 3000)
        else:
            self.show_message("Input Error", "Please enter both username and password.")

    def updateToken_UUID(self):
        global UUID, ACCESS_TOKEN
        self.progress_bar_projects.setValue(0)
        self.progress_bar_projects.show()

        try:
            current_project = self.comboBox_projectList.currentText()
            if current_project not in project_dict:
                raise Exception("Selected project not found in project list")

            self.progress_bar_projects.setValue(50)
            UUID = project_dict[current_project]
            ACCESS_TOKEN = get_authentication_token(BASE_URL, UUID, HEADERS)
            self.tableWidget_existingTCLinks.setRowCount(0)
            self.tableWidget_ReqInfo.setRowCount(0)
            self.lineEdit_testCaseNumber.clear()
            self.progress_bar_projects.setValue(100)
            self.statusBar().showMessage("Project selected", 3000)
        except Exception as e:
            self.progress_bar_projects.setValue(0)
            self.show_message("Error", str(e), QMessageBox.Icon.Critical)
        finally:
            self.progress_bar_projects.hide()

    def on_submit(self):
        global project_dict, UUID, ACCESS_TOKEN
        self.progress_bar_projects.hide()

        try:
            _ = USERNAME, PASSWORD
        except NameError:
            self.show_message("Error", "Please login")
            return

        if USERNAME and PASSWORD and USERNAME.strip() and PASSWORD.strip():
            self.error_occurred = False
            self.progress_bar_projects.setValue(0)
            self.progress_bar_projects.show()

            def safe_step(func):
                def wrapper():
                    if self.error_occurred:
                        return
                    try:
                        func()
                    except Exception as e:
                        self.error_occurred = True
                        self.progress_bar_projects.setValue(0)
                        self.progress_bar_projects.hide()
                        self.show_message("Error", str(e), QMessageBox.Icon.Critical)
                return wrapper

            def step1():
                self.progress_bar_projects.setValue(20)

            def step2():
                global project_dict
                project_dict = get_project_list(HEADERS)
                self.progress_bar_projects.setValue(50)
                self.comboBox_projectList.currentIndexChanged.disconnect()
                self.comboBox_projectList.clear()
                self.comboBox_projectList.addItems(project_dict.keys())
                self.comboBox_projectList.currentIndexChanged.connect(self.updateToken_UUID)

            def step3():
                global UUID, ACCESS_TOKEN
                self.progress_bar_projects.setValue(70)
                current_project = self.comboBox_projectList.currentText()
                if current_project not in project_dict:
                    raise Exception("Selected project not found in project list")
                UUID = project_dict[current_project]
                ACCESS_TOKEN = get_authentication_token(BASE_URL, UUID, HEADERS)

            def finish():
                self.progress_bar_projects.setValue(100)
                self.progress_bar_projects.hide()
                self.statusBar().showMessage("Projects loaded", 3000)

            QTimer.singleShot(200, lambda: safe_step(step1)())
            QTimer.singleShot(600, lambda: safe_step(step2)())
            QTimer.singleShot(900, lambda: safe_step(step3)())
            QTimer.singleShot(1200, lambda: safe_step(finish)())
        else:
            self.show_message("Input Error", "Please enter both username and password.")

    def get_req_description(self, reqId):
        global TCID, req_list, ACCESS_TOKEN,UUID
        self.progress_bar_get_tc_links.hide()

        try:
            _ = USERNAME
        except NameError:
            self.show_message("Error", "Please login")
            return

        try:
            _ = ACCESS_TOKEN
        except NameError:
            self.show_message("Error", "Please Select a project")
            return

        if not ACCESS_TOKEN or not UUID:
            self.show_message("Error", "Invalid ACCESS_TOKEN or UUID")
            return

        headers = { 'Authorization': f'Bearer {ACCESS_TOKEN}' }

        req_desc = get_req_description(reqId, headers, UUID)
        self.progress_bar_get_req_desc.setValue(50)
        self.progress_bar_get_req_desc.show()
        tag = req_desc.get('tag', 'No TAG available')
        summary = next((f['string'] for f in req_desc['fields'] if f['label'] == 'Summary'), 'No Summary available')

        description_html = next((f['formattedString']['text'] for f in req_desc['fields'] if f['label'] == 'Description'),
            'No Description available')
        description_soup = BeautifulSoup(description_html, 'html.parser')

        image_tag = description_soup.find('img')
        if image_tag:
            description_text = "Requirement contains image, please check Helix"
        else:
            description_text = description_soup.get_text()
        discussions = []
        discussions_field_found = False
        for field in req_desc['fields']:
            if field['label'] == 'Discussion':
                discussions_field_found = True
                discussion_text = BeautifulSoup(field['formattedString']['text'], 'html.parser').get_text()
                discussions.append(discussion_text)

        discussions_text = "\\n".join(discussions) if discussions_field_found and discussions else \
            ("Field does not exist" if not discussions_field_found else "No Discussion available")

        self.add_row_to_table(tag, summary, description_text, discussions_text)

    def add_row_to_table(self, tag, summary, description, discussions):
        if self.tableWidget_ReqInfo.columnCount() == 0:
            self.tableWidget_ReqInfo.setColumnCount(4)
            self.tableWidget_ReqInfo.setHorizontalHeaderLabels(["TAG", "Summary", "Description", "Discussions"])

        row = self.tableWidget_ReqInfo.rowCount()
        self.tableWidget_ReqInfo.insertRow(row)

        tag_item = QTableWidgetItem(tag)
        summary_item = QTableWidgetItem(summary)
        description_item = QTableWidgetItem(description)
        discussions_item = QTableWidgetItem(discussions)

        description_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        description_item.setFlags(description_item.flags() | Qt.ItemFlag.ItemIsEditable)
        discussions_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        discussions_item.setFlags(discussions_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        self.tableWidget_ReqInfo.setItem(row, 0, tag_item)
        self.tableWidget_ReqInfo.setItem(row, 1, summary_item)
        self.tableWidget_ReqInfo.setItem(row, 2, description_item)
        self.tableWidget_ReqInfo.setItem(row, 3, discussions_item)

        self.tableWidget_ReqInfo.resizeColumnToContents(0)
        self.tableWidget_ReqInfo.resizeColumnToContents(1)
        self.tableWidget_ReqInfo.setColumnWidth(2, 350)
        self.tableWidget_ReqInfo.setColumnWidth(3, 350)
        self.tableWidget_ReqInfo.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tableWidget_ReqInfo.resizeRowsToContents()

        self.progress_bar_get_req_desc.setValue(100)
        self.progress_bar_get_req_desc.hide()

    def read_table_items(self):
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.progress_bar_get_req_desc.hide()
        self.progress_bar_get_req_desc.setValue(0)
        self.progress_bar_get_req_desc.show()
        self.tableWidget_ReqInfo.setRowCount(0)
        try:
            rows = self.tableWidget_existingTCLinks.rowCount()
            if rows == 0:
                raise ValueError("The table is empty!")

            empty = True
            for row in range(rows):
                item = self.tableWidget_existingTCLinks.item(row, 0)
                if item and item.text().strip():
                    reqId = item.text()
                    self.progress_bar_get_req_desc.setValue(50)
                    empty = False
                    self.get_req_description(reqId)
                    self.progress_bar_get_req_desc.setValue(100)
                    time.sleep(0.05)
            self.progress_bar_get_req_desc.hide()
            if empty:
                raise ValueError("All rows are empty!")
        except ValueError as e:
            QMessageBox.warning(None, "Warning", str(e))

    def get_req_Tag(self, reqId):
        global TCID, req_list, ACCESS_TOKEN,UUID
        self.progress_bar_get_tc_links.hide()

        if not ACCESS_TOKEN or not UUID:
            self.show_message("Error", "Invalid ACCESS_TOKEN or UUID")
            return

        headers = { 'Authorization': f'Bearer {ACCESS_TOKEN}' }
        req_desc = get_req_description(reqId, headers, UUID)
        tag = req_desc.get('tag', 'No TAG available')
        return  tag

    def getTCLinks(self):
        global TCID, req_list, ACCESS_TOKEN
        self.progress_bar_get_tc_links.hide()
        prefixes = ("SYS", "SW", "SWDD", "CNST")

        try:
            _ = USERNAME, ACCESS_TOKEN
        except NameError:
            self.show_message("Error", "Please log in first.", QMessageBox.Icon.Warning)
            return

        test_case_id = self.lineEdit_testCaseNumber.text().strip()
        TCID = test_case_id

        if not test_case_id.isdigit() or int(test_case_id) <= 0:
            self.show_message("Input Error", "Test Case ID must be a positive integer.")
            return

        self.tableWidget_ReqInfo.setRowCount(0)
        self.progress_bar_get_tc_links.setValue(0)
        self.progress_bar_get_tc_links.show()

        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

        try:
            test_cases = get_test_cases_links(test_case_id, headers, UUID)
            test_case_requirements = {}

            for link in test_cases["linksData"]:
                name = link["linkDefinition"]["name"]
                if name == "Shared Test Case Steps":
                    continue

                if name == "Related Items":
                    peers = link["peers"]
                    tc_id = next(p["itemID"] for p in peers if p["itemType"] == "testCases")
                    requirement_id = next(p["itemID"] for p in peers if p["itemType"] == "requirements")
                else:
                    tc_id = link["parentChildren"]["children"][0]["itemID"]
                    requirement_id = link["parentChildren"]["parent"]["itemID"]

                if not any(str(requirement_id).startswith(pref) for pref in prefixes):
                    pass

                test_case_requirements.setdefault(tc_id, []).append(requirement_id)

            req_list = [req for reqs in test_case_requirements.values() for req in reqs]
            self.tableWidget_existingTCLinks.setRowCount(len(req_list))
            for row, rid in enumerate(req_list):
                self.tableWidget_existingTCLinks.setItem(row, 0, QTableWidgetItem(str(rid)))

            self.progress_bar_get_tc_links.setValue(100)
            self.progress_bar_get_tc_links.hide()
            return req_list

        except Exception as e:
            self.progress_bar_get_tc_links.setValue(0)
            self.progress_bar_get_tc_links.hide()
            self.show_message("Error", str(e), QMessageBox.Icon.Critical)

    def filter_table(self):
        filter_text = self.lineEdit_userName_2.text().lower()
        for row in range(self.tableWidget_ReqInfo.rowCount()):
            match = False
            for col in range(self.tableWidget_ReqInfo.columnCount()):
                item = self.tableWidget_ReqInfo.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.tableWidget_ReqInfo.setRowHidden(row, not match)
