from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1136, 913)
        MainWindow.setStyleSheet("background-color: #1e1e1e; color: #ffffff; font-size: 12px; font-family: Arial;")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_projectList = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_projectList.setGeometry(QtCore.QRect(10, 160, 261, 31))
        self.comboBox_projectList.setStyleSheet(
            "background-color: #333333; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.comboBox_projectList.setObjectName("comboBox_projectList")

        self.pushButton_GetProjects = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_GetProjects.setGeometry(QtCore.QRect(280, 160, 101, 31))
        self.pushButton_GetProjects.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.pushButton_GetProjects.setObjectName("pushButton_GetProjects")

        self.lineEdit_testCaseNumber = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_testCaseNumber.setGeometry(QtCore.QRect(10, 210, 261, 31))
        self.lineEdit_testCaseNumber.setStyleSheet(
            "background-color: #333333; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.lineEdit_testCaseNumber.setObjectName("lineEdit_testCaseNumber")

        self.pushButton_getTCLinks = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_getTCLinks.setGeometry(QtCore.QRect(280, 210, 101, 31))
        self.pushButton_getTCLinks.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.pushButton_getTCLinks.setObjectName("pushButton_getTCLinks")

        self.tableWidget_existingTCLinks = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget_existingTCLinks.setGeometry(QtCore.QRect(10, 370, 256, 192))
        self.tableWidget_existingTCLinks.setStyleSheet("""
            QTableWidget {
                background-color: #333333;
                color: white;
                border-radius: 5px;
                gridline-color: #555555;
            }
            QHeaderView::section {
                background-color: #444444;
                color: #a0a0a0;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #555555;
            }
            QTableWidget::item:selected {
                background-color: #5677a0;
                color: white;
            }
        """)

        # Adjust row height for readability
        self.tableWidget_existingTCLinks.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_existingTCLinks.horizontalHeader().setStretchLastSection(True)

        self.tableWidget_existingTCLinks.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_existingTCLinks.setObjectName("tableWidget_existingTCLinks")
        self.tableWidget_existingTCLinks.setColumnCount(1)
        self.tableWidget_existingTCLinks.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_existingTCLinks.setHorizontalHeaderItem(0, item)

        self.label_existingTestCases = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_existingTestCases.setGeometry(QtCore.QRect(10, 340, 251, 31))
        self.label_existingTestCases.setStyleSheet("font-weight: bold; color: #ffffff;")
        self.label_existingTestCases.setObjectName("label_existingTestCases")

        self.pushButton_LinkSelectedItems = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_LinkSelectedItems.setGeometry(QtCore.QRect(280, 570, 111, 31))
        self.pushButton_LinkSelectedItems.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.pushButton_LinkSelectedItems.setObjectName("pushButton_LinkSelectedItems")

        self.label_userName = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_userName.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.label_userName.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.label_userName.setObjectName("label_userName")

        self.label_Password = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_Password.setGeometry(QtCore.QRect(10, 60, 131, 31))
        self.label_Password.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.label_Password.setObjectName("label_Password")

        self.lineEdit_userName = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_userName.setGeometry(QtCore.QRect(80, 20, 211, 31))
        self.lineEdit_userName.setStyleSheet(
            "background-color: #333333; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.lineEdit_userName.setObjectName("lineEdit_userName")

        self.lineEdit_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(80, 60, 211, 31))
        self.lineEdit_password.setStyleSheet(
            "background-color: #333333; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")

        self.pushButton_connectToHelixServer = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_connectToHelixServer.setGeometry(QtCore.QRect(80, 100, 111, 31))
        self.pushButton_connectToHelixServer.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 5px;")
        self.pushButton_connectToHelixServer.setObjectName("pushButton_connectToHelixServer")

        self.listWidget_reqNumbers = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_reqNumbers.setGeometry(QtCore.QRect(280, 370, 256, 192))
        self.listWidget_reqNumbers.setStyleSheet("background-color: #333333; color: white; border-radius: 5px;")
        self.listWidget_reqNumbers.setObjectName("listWidget_reqNumbers")

        self.pushButton_addReqToList = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_addReqToList.setGeometry(QtCore.QRect(280, 270, 101, 31))
        self.pushButton_addReqToList.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.pushButton_addReqToList.setObjectName("pushButton_addReqToList")

        self.lineEdit_reqNumber = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_reqNumber.setGeometry(QtCore.QRect(10, 270, 261, 31))
        self.lineEdit_reqNumber.setStyleSheet(
            "background-color: #333333; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.lineEdit_reqNumber.setObjectName("lineEdit_reqNumber")

        self.pushButton_removeSelected = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_removeSelected.setGeometry(QtCore.QRect(400, 570, 111, 31))
        self.pushButton_removeSelected.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px;")
        self.pushButton_removeSelected.setObjectName("pushButton_removeSelected")

        self.progress_bar_projects = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_projects.setGeometry(QtCore.QRect(390, 160, 131, 31))
        self.progress_bar_projects.setStyleSheet("background-color: #555555; border-radius: 5px;")
        self.progress_bar_projects.setProperty("value", 24)
        self.progress_bar_projects.setObjectName("progress_bar_projects")

        self.progress_bar_get_tc_links = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_get_tc_links.setGeometry(QtCore.QRect(390, 210, 131, 31))
        self.progress_bar_get_tc_links.setStyleSheet("background-color: #555555; border-radius: 5px;")
        self.progress_bar_get_tc_links.setProperty("value", 24)
        self.progress_bar_get_tc_links.setObjectName("progress_bar_get_tc_links")

        self.progress_bar_link_reqs = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_link_reqs.setGeometry(QtCore.QRect(350, 440, 131, 31))
        self.progress_bar_link_reqs.setStyleSheet("background-color: #555555; border-radius: 5px;")
        self.progress_bar_link_reqs.setProperty("value", 24)
        self.progress_bar_link_reqs.setObjectName("progress_bar_link_reqs")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TC_ReqLinker"))
        self.pushButton_GetProjects.setText(_translate("MainWindow", "Get Projects"))
        self.lineEdit_testCaseNumber.setText(_translate("MainWindow", "Enter Helix Test Case Number "))
        self.pushButton_getTCLinks.setText(_translate("MainWindow", "Get TC Links"))
        item = self.tableWidget_existingTCLinks.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Linked Reqs"))
        self.label_existingTestCases.setText(_translate("MainWindow", "EXISTING TEST CASE LINKS"))
        self.pushButton_LinkSelectedItems.setText(_translate("MainWindow", "Link Selected "))
        self.label_userName.setText(_translate("MainWindow", "USER NAME"))
        self.label_Password.setText(_translate("MainWindow", "PASSWORD"))
        self.lineEdit_userName.setText(_translate("MainWindow", "Enter Your Helix User Name"))
        self.lineEdit_password.setText(_translate("MainWindow", "Enter Your Password"))
        self.pushButton_connectToHelixServer.setText(_translate("MainWindow", "Connect"))
        self.pushButton_addReqToList.setText(_translate("MainWindow", "Add Req To List"))
        self.lineEdit_reqNumber.setText(_translate("MainWindow", "Enter Req Number"))
        self.pushButton_removeSelected.setText(_translate("MainWindow", "Remove Selected"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
