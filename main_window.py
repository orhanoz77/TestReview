"""
Auto-generated UI layout for MainWindow
Built with PyQt6 for ShowTestCaseLinkedReq application
"""

from PyQt6 import QtCore, QtGui, QtWidgets
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Ui_MainWindow(object):
    """UI Layout class for MainWindow"""
    
    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """
        Set up the main window UI layout.
        
        Args:
            MainWindow: The main window widget
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)

        # ----- Central widget & master layout -----
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.masterLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.masterLayout.setContentsMargins(10, 10, 10, 10)
        self.masterLayout.setSpacing(12)

        # ===== Left column (controls) =====
        self.leftPanel = QtWidgets.QFrame(parent=self.centralwidget)
        self.leftPanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftPanel.setMinimumWidth(320)
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftPanel)
        self.leftLayout.setSpacing(10)

        # --- Login group ---
        self.groupLogin = QtWidgets.QGroupBox("Login", parent=self.leftPanel)
        self.groupLoginLayout = QtWidgets.QFormLayout(self.groupLogin)
        self.label_userName = QtWidgets.QLabel("USER NAME", parent=self.groupLogin)
        self.lineEdit_userName = QtWidgets.QLineEdit(parent=self.groupLogin)
        self.lineEdit_userName.setObjectName("lineEdit_userName")
        self.label_Password = QtWidgets.QLabel("PASSWORD", parent=self.groupLogin)
        self.lineEdit_password = QtWidgets.QLineEdit(parent=self.groupLogin)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.buttonsLoginRow = QtWidgets.QHBoxLayout()
        self.pushButton_connectToHelixServer = QtWidgets.QPushButton("Login", parent=self.groupLogin)
        self.pushButton_connectToHelixServer.setObjectName("pushButton_connectToHelixServer")
        self.pushButton_SaveCredentials = QtWidgets.QPushButton("Save Credentials", parent=self.groupLogin)
        self.pushButton_SaveCredentials.setObjectName("pushButton_SaveCredentials")
        self.buttonsLoginRow.addWidget(self.pushButton_connectToHelixServer)
        self.buttonsLoginRow.addWidget(self.pushButton_SaveCredentials)

        self.groupLoginLayout.addRow(self.label_userName, self.lineEdit_userName)
        self.groupLoginLayout.addRow(self.label_Password, self.lineEdit_password)
        self.groupLoginLayout.addRow(self.buttonsLoginRow)

        # --- Project group ---
        self.groupProject = QtWidgets.QGroupBox("Project", parent=self.leftPanel)
        self.groupProjectLayout = QtWidgets.QGridLayout(self.groupProject)
        self.comboBox_projectList = QtWidgets.QComboBox(parent=self.groupProject)
        self.comboBox_projectList.setObjectName("comboBox_projectList")
        self.pushButton_GetProjects = QtWidgets.QPushButton("Get Projects", parent=self.groupProject)
        self.pushButton_GetProjects.setObjectName("pushButton_GetProjects")
        self.progress_bar_projects = QtWidgets.QProgressBar(parent=self.groupProject)
        self.progress_bar_projects.setObjectName("progress_bar_projects")
        self.progress_bar_projects.setTextVisible(False)
        self.progress_bar_projects.setRange(0, 100)
        self.progress_bar_projects.setValue(0)
        self.groupProjectLayout.addWidget(self.comboBox_projectList, 0, 0, 1, 2)
        self.groupProjectLayout.addWidget(self.pushButton_GetProjects, 1, 0, 1, 1)
        self.groupProjectLayout.addWidget(self.progress_bar_projects, 1, 1, 1, 1)

        # --- Test Case group ---
        self.groupTC = QtWidgets.QGroupBox("Test Case", parent=self.leftPanel)
        self.groupTCLayout = QtWidgets.QGridLayout(self.groupTC)
        self.lineEdit_testCaseNumber = QtWidgets.QLineEdit(parent=self.groupTC)
        self.lineEdit_testCaseNumber.setObjectName("lineEdit_testCaseNumber")
        self.pushButton_getTCLinks = QtWidgets.QPushButton("Get TC Links", parent=self.groupTC)
        self.pushButton_getTCLinks.setObjectName("pushButton_getTCLinks")
        self.progress_bar_get_tc_links = QtWidgets.QProgressBar(parent=self.groupTC)
        self.progress_bar_get_tc_links.setObjectName("progress_bar_get_tc_links")
        self.progress_bar_get_tc_links.setTextVisible(False)
        self.progress_bar_get_tc_links.setRange(0, 100)
        self.progress_bar_get_tc_links.setValue(0)
        self.groupTCLayout.addWidget(self.lineEdit_testCaseNumber, 0, 0, 1, 2)
        self.groupTCLayout.addWidget(self.pushButton_getTCLinks, 1, 0, 1, 1)
        self.groupTCLayout.addWidget(self.progress_bar_get_tc_links, 1, 1, 1, 1)

        # --- Linked Requirements group ---
        self.groupLinks = QtWidgets.QGroupBox("Existing Test Case Links", parent=self.leftPanel)
        self.groupLinksLayout = QtWidgets.QVBoxLayout(self.groupLinks)
        self.tableWidget_existingTCLinks = QtWidgets.QTableWidget(parent=self.groupLinks)
        self.tableWidget_existingTCLinks.setObjectName("tableWidget_existingTCLinks")
        self.tableWidget_existingTCLinks.setColumnCount(1)
        self.tableWidget_existingTCLinks.setHorizontalHeaderLabels(["Linked Reqs"])
        self.tableWidget_existingTCLinks.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_existingTCLinks.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_existingTCLinks.setAlternatingRowColors(True)
        self.pushButton_GetReqDesc = QtWidgets.QPushButton("Get Req Desc", parent=self.groupLinks)
        self.pushButton_GetReqDesc.setObjectName("pushButton_GetReqDesc")
        self.progress_bar_get_req_desc = QtWidgets.QProgressBar(parent=self.groupLinks)
        self.progress_bar_get_req_desc.setObjectName("progress_bar_get_req_desc")
        self.progress_bar_get_req_desc.setTextVisible(False)
        self.progress_bar_get_req_desc.setRange(0, 100)
        self.progress_bar_get_req_desc.setValue(0)
        self.groupLinksLayout.addWidget(self.tableWidget_existingTCLinks)
        self.groupLinksLayout.addWidget(self.pushButton_GetReqDesc)
        self.groupLinksLayout.addWidget(self.progress_bar_get_req_desc)

        # Add groups to left layout
        self.leftLayout.addWidget(self.groupLogin)
        self.leftLayout.addWidget(self.groupProject)
        self.leftLayout.addWidget(self.groupTC)
        self.leftLayout.addWidget(self.groupLinks)
        self.leftLayout.addStretch()

        # ===== Right column (requirements table) =====
        self.rightPanel = QtWidgets.QFrame(parent=self.centralwidget)
        self.rightPanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightPanel)
        self.rightLayout.setSpacing(10)

        # Search in Requirements
        self.searchRow = QtWidgets.QHBoxLayout()
        self.lineEdit_userName_2 = QtWidgets.QLineEdit(parent=self.rightPanel)
        self.lineEdit_userName_2.setObjectName("lineEdit_userName_2")
        self.searchRow.addWidget(self.lineEdit_userName_2)
        self.rightLayout.addLayout(self.searchRow)

        # Requirements table
        self.tableWidget_ReqInfo = QtWidgets.QTableWidget(parent=self.rightPanel)
        self.tableWidget_ReqInfo.setObjectName("tableWidget_ReqInfo")
        self.tableWidget_ReqInfo.setColumnCount(0)
        self.tableWidget_ReqInfo.setRowCount(0)
        self.tableWidget_ReqInfo.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_ReqInfo.setAlternatingRowColors(True)
        self.tableWidget_ReqInfo.setWordWrap(True)
        self.tableWidget_ReqInfo.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ReqInfo.verticalHeader().setVisible(False)
        self.rightLayout.addWidget(self.tableWidget_ReqInfo)

        # Add left and right panels to master layout
        self.masterLayout.addWidget(self.leftPanel)
        self.masterLayout.addWidget(self.rightPanel, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        # Menu/Status bars
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Retranslate
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """
        Set UI text and translations.
        
        Args:
            MainWindow: The main window widget
        """
        _t = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_t("MainWindow", "TC_ReqLinker"))
        self.lineEdit_userName.setPlaceholderText(_t("MainWindow", "Enter Your Helix User Name"))
        self.lineEdit_password.setPlaceholderText(_t("MainWindow", "Enter Your Password"))
        self.lineEdit_testCaseNumber.setPlaceholderText(_t("MainWindow", "Enter Helix Test Case Number"))
        self.lineEdit_userName_2.setPlaceholderText(_t("MainWindow", "Search In Requirements"))
