import base64
import time
from urllib.parse import urljoin

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

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # PUSH BUTTONS
        self.pushButton_GetProjects.clicked.connect(self.on_submit)
        self.pushButton_connectToHelixServer.clicked.connect(self.getUserInformation)
        self.pushButton_getTCLinks.clicked.connect(self.getTCLinks)
        self.pushButton_addReqToList.clicked.connect(self.add_req)
        self.pushButton_removeSelected.clicked.connect(self.remove_req)
        self.pushButton_LinkSelectedItems.clicked.connect(self.addReqLinkToTC)
        self.pushButton_GetReqDesc.clicked.connect(self.read_table_items)

        self.lineEdit_testCaseNumber.returnPressed.connect(self.getTCLinks)
        self.lineEdit_reqNumber.returnPressed.connect(self.add_req)
        self.lineEdit_password.returnPressed.connect(self.getUserInformation)
        self.lineEdit_userName_2.textChanged.connect(self.filter_table)

        #Combobox
        self.comboBox_projectList.currentIndexChanged.connect(self.updateToken_UUID)


        #Progress Bar
        self.progress_bar_projects.hide()
        self.progress_bar_get_tc_links.hide()
        self.progress_bar_link_reqs.hide()
        self.progress_bar_get_req_desc.hide()

        self.tableWidget_existingTCLinks.setColumnCount(1)
        self.tableWidget_existingTCLinks.setHorizontalHeaderLabels(["Linked requirements"])
        header  = self.tableWidget_existingTCLinks.horizontalHeader()
        header.setStretchLastSection(True)

        self.tableWidget_ReqInfo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.pushButton_SaveCredentials.clicked.connect(self.save_credentials)

        # Load credentials when the application starts
        self.load_credentials()

    from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTableWidgetItem
    from PyQt6.QtGui import QPixmap

    from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTableWidgetItem
    from PyQt6.QtGui import QPixmap
    import base64

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
        msg_box.setStyleSheet(f"""background-color: "#ffffff";""")
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
            self.show_message("Info", "Completed")
            print(USERNAME)
            print(PASSWORD)
        else:
            self.show_message("Input Error", "Please enter both username and password.")

    def updateToken_UUID(self):
        global UUID, ACCESS_TOKEN
        self.progress_bar_projects.setValue(0)
        self.progress_bar_projects.show()  # Show the progress bar at the beginning

        try:
            current_project = self.comboBox_projectList.currentText()
            if current_project not in project_dict:
                raise Exception("Selected project not found in project list")

            self.progress_bar_projects.setValue(50)  # Update progress to 50%

            UUID = project_dict[current_project]
            ACCESS_TOKEN = get_authentication_token(BASE_URL, UUID, HEADERS)
            self.tableWidget_existingTCLinks.setRowCount(0)
            self.tableWidget_ReqInfo.setRowCount(0)

            self.lineEdit_testCaseNumber.clear()

            self.progress_bar_projects.setValue(100)  # Complete the progress
            print(UUID)
            print(ACCESS_TOKEN)
            print("TOKEN WAS UPDATED")

        except Exception as e:
            self.progress_bar_projects.setValue(0)
            self.show_message("Error", str(e), QMessageBox.Icon.Critical)

        finally:
            self.progress_bar_projects.hide()  # Hide the progress bar at the end

    def on_submit(self):
        """Handles the submit button click event with progress bar updates and delay."""
        global project_dict, UUID, ACCESS_TOKEN
        print("on_submit called!")  # Debug print to confirm function is called
        self.progress_bar_projects.hide()  # Hide the progress bar at the beginning

        try:
            print(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")  # Debug print to check values
        except NameError as e:
            self.show_message("Error", "Please login")
            return

        if USERNAME is not None and PASSWORD is not None and USERNAME.strip() != "" and PASSWORD.strip() != "":
            print("Valid username and password.")
            self.error_occurred = False  # Initialize an error flag

            self.progress_bar_projects.setValue(0)
            self.progress_bar_projects.show()  # Show the progress bar when starting the task

            def safe_step(func):
                def wrapper():
                    if self.error_occurred:
                        return  # Skip if an error occurred
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
                # print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")

            QTimer.singleShot(500, lambda: safe_step(step1)())
            QTimer.singleShot(1500, lambda: safe_step(step2)())
            QTimer.singleShot(2500, lambda: safe_step(step3)())
            QTimer.singleShot(3500, lambda: safe_step(finish)())

        else:
            print("Invalid or missing username/password.")
            self.show_message("Input Error", "Please enter both username and password.")

    # def getTCLinks(self):
    #     """Fetch and display requirement links for a given test case."""
    #     global TCID, req_list, ACCESS_TOKEN
    #     self.progress_bar_get_tc_links.hide()  # Hide progress bar at the beginning
    #     prefixes = ("SYS", "SW", "SWDD", "CNST")
    #
    #     try:
    #         print(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")  # Debug print to check values
    #     except NameError as e:
    #         self.show_message("Error", "Please login")
    #         return
    #     try:
    #         print(f"ACCESS TOKEN: {ACCESS_TOKEN}")  # Debug print to check values
    #     except NameError as e:
    #         self.show_message("Error","Please Select a project")
    #         return
    #
    #     test_case_id = self.lineEdit_testCaseNumber.text()
    #     TCID = test_case_id.strip()
    #     headers = {
    #         'Authorization': f'Bearer {ACCESS_TOKEN}',
    #     }
    #
    #     if test_case_id and test_case_id.isdigit() and int(test_case_id) > 0:
    #         self.progress_bar_get_tc_links.setValue(0)  # Reset progress bar
    #         self.progress_bar_get_tc_links.show()  # Show progress bar
    #         value = 40
    #         try:
    #             self.progress_bar_get_tc_links.setValue(value)  # Step 1: Start fetching data
    #             self.progress_bar_get_tc_links.show()  # Show progress bar
    #             test_cases = get_test_cases_links(test_case_id, headers, UUID)
    #             print("Retrieved Test Cases Data:", test_cases)
    #             test_case_requirements = {}
    #
    #             for link in test_cases["linksData"]:
    #                 if link["linkDefinition"]["name"] != "Shared Test Case Steps" :
    #                     tc_id = link["parentChildren"]["children"][0]["itemID"]
    #                     requirement_id = link["parentChildren"]["parent"]["itemID"]
    #                     req_tag = self.get_req_Tag(requirement_id)
    #                     if req_tag.startswith(prefixes):
    #                         print("PREFIX IDENTIFIED")
    #                         if tc_id not in test_case_requirements:
    #                             test_case_requirements[tc_id] = []
    #                         test_case_requirements[tc_id].append(requirement_id)
    #             self.progress_bar_get_tc_links.setValue(70)  # Step 2: Parse the data
    #             self.progress_bar_get_tc_links.show()  # Show progress bar
    #             time.sleep(0.2)
    #             req_list = [req for requirements in test_case_requirements.values() for req in requirements]
    #
    #             self.progress_bar_get_tc_links.setValue(90)  # Step 3: Populate the table
    #             self.progress_bar_get_tc_links.show()  # Show progress bar
    #             self.tableWidget_existingTCLinks.setRowCount(len(req_list))
    #             self.tableWidget_existingTCLinks.setColumnCount(1)
    #             time.sleep(0.2)
    #             for row, value in enumerate(req_list):
    #                 self.tableWidget_existingTCLinks.setItem(row, 0, QTableWidgetItem(str(value)))
    #
    #             self.progress_bar_get_tc_links.setValue(100)  # Task completed
    #             self.progress_bar_get_tc_links.hide()  # Hide progress bar after completion
    #
    #             return req_list
    #
    #         except Exception as e:
    #             self.progress_bar_get_tc_links.setValue(0)
    #             self.progress_bar_get_tc_links.hide()  # Hide progress bar if an error occurs
    #             self.show_message("Error", str(e), QMessageBox.Icon.Critical)
    #     else:
    #         self.show_message("Input Error", "The Test Case ID must be a numeric value greater than 0.")

    def addReqLinkToTC(self):
        global ACCESS_TOKEN

        try:
            print(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")  # Debug print to check values
        except NameError as e:
            self.show_message("Error", f"Missing variable: {e}", QMessageBox.Icon.Critical)
            return
        try:
            print(f"ACCESS TOKEN: {ACCESS_TOKEN}")  # Debug print to check values
        except NameError as e:
            self.show_message("","Please Select a project")
            return

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.progress_bar_link_reqs.setValue(0)  # Initialize progress bar to 0%
        self.progress_bar_link_reqs.show()  # Show the progress bar

        self.getTCLinks()  # Fetch the test case links

        try:
            if not TCID.isdigit() or int(TCID) <= 0:
                raise ValueError(f"Invalid TestCaseId: {TCID}. It must be a positive integer.")

            existing_reqs = set()
            for row in range(self.tableWidget_existingTCLinks.rowCount()):
                existing_reqs.add(int(self.tableWidget_existingTCLinks.item(row, 0).text()))

            for reqs in range(self.listWidget_reqNumbers.count()):
                try:
                    req = self.listWidget_reqNumbers.item(reqs)
                    # print(req)
                    req_id = int(req.text())
                    print(req_id)
                    print("**************")

                    if req_id in existing_reqs:
                        print(f"Skipping ReqId {req_id} — already linked.")
                        continue

                    print(f"Processing TestCaseId: {TCID} with ReqId: {req_id}")
                    recordID = get_recordID(req_id, headers, UUID)
                    add_requirement_link_to_test_case(int(recordID), int(TCID), headers, UUID)
                    print("Requirement link added successfully.")

                    progress = int((reqs + 1) / self.listWidget_reqNumbers.count() * 100)
                    self.progress_bar_link_reqs.setValue(progress)  # Update progress bar value
                    time.sleep(0.5)  # Optional delay to avoid overloading the server

                except ValueError:
                    self.show_message("Error", f"Invalid requirement ID: {req.text()}. It must be a valid integer.",
                                      QMessageBox.Icon.Critical)
                except Exception as e:
                    self.show_message("Error", f"An error occurred while processing ReqId {req.text()}: {str(e)}",
                                      QMessageBox.Icon.Critical)

            self.progress_bar_link_reqs.setValue(100)  # Set progress bar to 100% after completion
            time.sleep(0.5)
            self.progress_bar_link_reqs.hide()  # Hide the progress bar once done

        except ValueError as ve:
            self.progress_bar_link_reqs.hide()
            self.show_message("Error", str(ve), QMessageBox.Icon.Critical)
        except Exception as e:
            self.progress_bar_link_reqs.hide()
            self.show_message("Error", f"An unexpected error occurred: {str(e)}", QMessageBox.Icon.Critical)

    def add_req(self):
        """Add one or multiple numeric items to the list widget with validation."""
        new_items = self.lineEdit_reqNumber.text().strip()

        if not new_items:
            self.show_message("Invalid Input", "The input cannot be empty.")
            return

        # Find all sequences that are purely numeric and not part of a larger word
        items = re.findall(r'\b\d+\b', new_items)
        existing_items = [self.listWidget_reqNumbers.item(i).text() for i in range(self.listWidget_reqNumbers.count())]
        added_any = False
        invalid_entries = False

        for item in items:
            if item not in existing_items:  # Check for duplicates
                self.listWidget_reqNumbers.addItem(item)
                added_any = True
            else:
                print(f"Skipping duplicate item: {item}")

        if not items or any(not part.isdigit() for part in re.split(r'\s+', new_items) if part):
            invalid_entries = True

        if invalid_entries:
            self.show_message("Input Warning", "Some non-numeric values were ignored.", QMessageBox.Icon.Warning)

        if added_any:
            self.lineEdit_reqNumber.clear()
        else:
            self.show_message("No New Items", "No new valid items were added.")

    def remove_req(self):
        """Remove the currently selected item from the list widget."""
        selected_items = self.listWidget_reqNumbers.selectedItems()

        if not selected_items:
            self.show_message("Warning", "Please select an item to remove.", QMessageBox.Icon.Warning)
            return

        for item in selected_items:
            self.listWidget_reqNumbers.takeItem(self.listWidget_reqNumbers.row(item))

        # Check if the list is empty after removing items
        if self.listWidget_reqNumbers.count() == 0:
            self.show_message("Warning", "The list is now empty.", QMessageBox.Icon.Warning)

    def get_req_description(self, reqId):
        """Fetch and display requirement links and discussions for a given test case."""
        global TCID, req_list, ACCESS_TOKEN,UUID
        self.progress_bar_get_tc_links.hide()  # Hide progress bar at the beginning

        try:
            print(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")  # Debug print to check values
        except NameError:
            self.show_message("Error", "Please login")
            return

        try:
            print(f"ACCESS TOKEN: {ACCESS_TOKEN}")  # Debug print to check values
        except NameError:
            self.show_message("Error", "Please Select a project")
            return

        if not ACCESS_TOKEN or not UUID:
            self.show_message("Error", "Invalid ACCESS_TOKEN or UUID")
            print("Invalid ACCESS_TOKEN or UUID")
            return

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
        }

        req_desc = get_req_description(reqId, headers, UUID)
        self.progress_bar_get_req_desc.setValue(50)  # Reset progress bar
        self.progress_bar_get_req_desc.show()  # Show progress bar
        tag = req_desc.get('tag', 'No TAG available')
        summary = next((field['string'] for field in req_desc['fields'] if field['label'] == 'Summary'),
                       'No Summary available')

        # Extract the description and remove HTML tags using BeautifulSoup
        description_html = next(
            (field['formattedString']['text'] for field in req_desc['fields'] if field['label'] == 'Description'),
            'No Description available')

        description_soup = BeautifulSoup(description_html, 'html.parser')

        # Check if the description contains an image
        image_tag = description_soup.find('img')
        if image_tag:
            # image_src = image_tag.get('src', 'No image source available')
            image_src = image_tag.get('src', None)
            # If the image source is a relative path, make it an absolute URL
            # image_url = urljoin(BASE_URL, image_src) if not image_src.startswith('http') else image_src
            image_url = urljoin(BASE_URL, image_src)
            print("IMAGE SOURCE" + image_src)
            print("IMAGE INFO: Image found. URL:", image_url)
            response = requests.get(image_url, verify=False)  # Assuming SSL issues
            if response.status_code == 200:
                print("Image fetched successfully")
            else:
                print(f"Failed to fetch image. Status Code: {response.status_code}")

        if  image_tag :
            description_text = "Requirement contains image, please check Helix"
        else:
            0
            description_text = BeautifulSoup(description_html, 'html.parser').get_text()
        discussions = []
        discussions_field_found = False
        for field in req_desc['fields']:
            if field['label'] == 'Discussion':
                discussions_field_found = True
                discussion_text = BeautifulSoup(field['formattedString']['text'], 'html.parser').get_text()
                discussions.append(discussion_text)

        # Set discussions_text based on whether the 'Discussion' field was found
        if discussions_field_found:
            discussions_text = "\n".join(discussions) if discussions else "No Discussion available"
        else:
            discussions_text = "Field does not exist"
        self.add_row_to_table(tag, summary, description_text, discussions_text)

    def add_row_to_table(self, tag, summary, description, discussions):
        # Check if columns are already set, if not, set them
        if self.tableWidget_ReqInfo.columnCount() == 0:
            self.tableWidget_ReqInfo.setColumnCount(4)
            self.tableWidget_ReqInfo.setHorizontalHeaderLabels(["TAG", "Summary", "Description", "Discussions"])

        # Get the current row count
        current_row_count = self.tableWidget_ReqInfo.rowCount()

        # Insert a new row at the end
        self.tableWidget_ReqInfo.insertRow(current_row_count)

        # Create QTableWidgetItem for each column
        tag_item = QTableWidgetItem(tag)
        summary_item = QTableWidgetItem(summary)
        description_item = QTableWidgetItem(description)
        discussions_item = QTableWidgetItem(discussions)

        # Set text wrapping for the Description and Discussions columns
        description_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #description_item.setFlags(description_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        description_item.setFlags(description_item.flags() | Qt.ItemFlag.ItemIsEditable)
        discussions_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        discussions_item.setFlags(discussions_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        # Add the items to the respective columns in the new row
        self.tableWidget_ReqInfo.setItem(current_row_count, 0, tag_item)
        self.tableWidget_ReqInfo.setItem(current_row_count, 1, summary_item)
        self.tableWidget_ReqInfo.setItem(current_row_count, 2, description_item)
        self.tableWidget_ReqInfo.setItem(current_row_count, 3, discussions_item)

        # Resize "Tag" and "Summary" columns to fit content
        self.tableWidget_ReqInfo.resizeColumnToContents(0)
        self.tableWidget_ReqInfo.resizeColumnToContents(1)

        # Set a fixed width for the "Description" and "Discussions" columns
        self.tableWidget_ReqInfo.setColumnWidth(2, 300)
        self.tableWidget_ReqInfo.setColumnWidth(3, 300)
        self.tableWidget_ReqInfo.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)  # 2 is the index of the last column

        self.tableWidget_ReqInfo.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        self.progress_bar_get_req_desc.setValue(70)  # Reset progress bar
        self.progress_bar_get_req_desc.show()  # Show progress bar
        # time.sleep(0.2)

        # Adjust row height to fit wrapped text
        self.tableWidget_ReqInfo.resizeRowsToContents()

    def read_table_items(self):
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.progress_bar_get_req_desc.hide()
        self.progress_bar_get_req_desc.setValue(0)  # Reset progress bar
        self.progress_bar_get_req_desc.show()  # Show progress bar
        # print("READ TABLE ENTERED")
        self.tableWidget_ReqInfo.setRowCount(0)
        try:
            rows = self.tableWidget_existingTCLinks.rowCount()  # Get total rows
            if rows == 0:
                raise ValueError("The table is empty!")  # Raise an error if no rows exist


            empty = True  # Flag to check if all rows are empty

            for row in range(rows):
                item = self.tableWidget_existingTCLinks.item(row, 0)  # Read only from column 0
                if item and item.text().strip():  # Check if item is not None and not empty
                    reqId = item.text()
                    recordID = get_recordID(reqId, headers, UUID)
                    self.progress_bar_get_req_desc.setValue(50)  # Reset progress bar
                    self.progress_bar_get_req_desc.show()  # Show progress bar
                    empty = False
                    self.get_req_description(recordID) # WE MUST SEND RECORD ID HERE
                    self.progress_bar_get_req_desc.setValue(100)  # Reset progress bar
                    time.sleep(0.1)
                    self.progress_bar_get_req_desc.show()  # Show progress bar
            self.progress_bar_get_req_desc.hide()
            if empty:
                raise ValueError("All rows are empty!")  # Warn if all rows are empty
            self.progress_bar_get_req_desc.hide()
            # print("READ TABLE OUT")

        except ValueError as e:
            QMessageBox.warning(None, "Warning", str(e))  # Show a warning message box

    def get_req_Tag(self, reqId):
        """Fetch and display requirement links and discussions for a given test case."""
        global TCID, req_list, ACCESS_TOKEN,UUID
        self.progress_bar_get_tc_links.hide()  # Hide progress bar at the beginning

        # try:
        #     print(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")  # Debug print to check values
        # except NameError:
        #     self.show_message("Error", "Please login")
        #     return
        #
        # try:
        #     print(f"ACCESS TOKEN: {ACCESS_TOKEN}")  # Debug print to check values
        # except NameError:
        #     self.show_message("Error", "Please Select a project")
        #     return

        if not ACCESS_TOKEN or not UUID:
            self.show_message("Error", "Invalid ACCESS_TOKEN or UUID")
            print("Invalid ACCESS_TOKEN or UUID")
            return

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
        }

        req_desc = get_req_description(reqId, headers, UUID)
        tag = req_desc.get('tag', 'No TAG available')
        return  tag

    def getTCLinks(self):
        """Fetch and display requirement links for a given test case."""
        global TCID, req_list, ACCESS_TOKEN
        self.progress_bar_get_tc_links.hide()
        prefixes = ("SYS", "SW", "SWDD", "CNST")

        # 1) Check that username and token are available
        try:
            _ = USERNAME, ACCESS_TOKEN
        except NameError:
            self.show_message("Error", "Please log in first.", QMessageBox.Icon.Warning)
            return

        # 2) Read the Test Case ID from the input field
        test_case_id = self.lineEdit_testCaseNumber.text().strip()
        TCID = test_case_id

        # 3) Validate the Test Case ID
        if not test_case_id.isdigit() or int(test_case_id) <= 0:
            self.show_message("Input Error", "Test Case ID must be a positive integer.")
            return

        # 4) Send request to the API and parse the response
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
                    # get itemIDs from peers
                    peers = link["peers"]
                    tc_id = next(p["itemID"] for p in peers if p["itemType"] == "testCases")
                    requirement_id = next(p["itemID"] for p in peers if p["itemType"] == "requirements")
                else:
                    # get from parentChildren
                    tc_id = link["parentChildren"]["children"][0]["itemID"]
                    requirement_id = link["parentChildren"]["parent"]["itemID"]

                # optional prefix filter
                if not any(str(requirement_id).startswith(pref) for pref in prefixes):
                    # remove this line if you no longer want to filter by prefix
                    pass

                test_case_requirements.setdefault(tc_id, []).append(requirement_id)

            # Populate the table with requirement IDs
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