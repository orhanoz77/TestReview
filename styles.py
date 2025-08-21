# styles.py

BACKGROUND_COLOR = "#1e1e1e"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#4CAF50"
BUTTON_REMOVE_COLOR = "#f44336"
INPUT_BG_COLOR = "#333333"
INPUT_BORDER_RADIUS = "5px"
INPUT_PADDING = "5px"
TABLE_BG_COLOR = "#333333"
TABLE_HEADER_COLOR = "#444444"
TABLE_HEADER_TEXT_COLOR = "#a0a0a0"
TABLE_SELECTED_ITEM_BG_COLOR = "#5677a0"
PROGRESS_BAR_BG_COLOR = "#555555"

APP_BACKGROUND_STYLE = f"""
background-color: {BACKGROUND_COLOR};
"""

COMBOBOX_STYLE = f"""
background-color: {INPUT_BG_COLOR};
color: {TEXT_COLOR};
border-radius: {INPUT_BORDER_RADIUS};
padding: {INPUT_PADDING};
"""

BUTTON_STYLE = f"""
background-color: {BUTTON_COLOR};
color: {TEXT_COLOR};
border-radius: {INPUT_BORDER_RADIUS};
"""

BUTTON_REMOVE_STYLE = f"""
background-color: {BUTTON_REMOVE_COLOR};
color: {TEXT_COLOR};
border-radius: {INPUT_BORDER_RADIUS};
"""

INPUT_STYLE = f"""
background-color: {INPUT_BG_COLOR};
color: {TEXT_COLOR};
border-radius: {INPUT_BORDER_RADIUS};
padding: {INPUT_PADDING};
"""


TABLE_STYLE = f"""
QTableWidget {{
    background-color: {TABLE_BG_COLOR};
    color: {TEXT_COLOR};
    border: none;
    gridline-color: #555555;
    border-radius: {INPUT_BORDER_RADIUS};
}}
QTableCornerButton::section {{
    background-color: {TABLE_BG_COLOR};  /* Fix the white top-left corner */
    border: none;
}}
QHeaderView::section {{
    background-color: {TABLE_BG_COLOR};
    color: {TABLE_HEADER_TEXT_COLOR};
    padding: 8px;
    font-weight: bold;
    border: none;
}}
QTableWidget::item {{
    background-color: {TABLE_BG_COLOR};
    border: none;
    padding: 8px;
}}
QTableWidget::item:selected {{
    background-color: {TABLE_SELECTED_ITEM_BG_COLOR};
    color: {TEXT_COLOR};
    border-radius: 6px;
}}
"""




PROGRESS_BAR_STYLE = f"""
background-color: {PROGRESS_BAR_BG_COLOR};
border-radius: {INPUT_BORDER_RADIUS};
"""

LISTWIDGET_STYLE = f"""
QListWidget {{
    background-color: {INPUT_BG_COLOR};
    color: {TEXT_COLOR};
    border-radius: {INPUT_BORDER_RADIUS};
    padding: {INPUT_PADDING};
}}

QListWidget::item:selected {{
    background-color: #5677a0;
    color: white;
}}
"""


LABEL_STYLE = f"""
color: {TEXT_COLOR};
font-weight: bold;
"""

# self.comboBox_projectList.setStyleSheet(styles.COMBOBOX_STYLE)
# self.lineEdit_testCaseNumber.setStyleSheet(styles.INPUT_STYLE)
# self.lineEdit_userName.setStyleSheet(styles.INPUT_STYLE)
# self.lineEdit_password.setStyleSheet(styles.INPUT_STYLE)
# self.lineEdit_reqNumber.setStyleSheet(styles.INPUT_STYLE)
# self.pushButton_GetProjects.setStyleSheet(styles.BUTTON_STYLE)
# self.pushButton_getTCLinks.setStyleSheet(styles.BUTTON_STYLE)
# self.pushButton_connectToHelixServer.setStyleSheet(styles.BUTTON_STYLE)
# self.pushButton_addReqToList.setStyleSheet(styles.BUTTON_STYLE)
# self.pushButton_LinkSelectedItems.setStyleSheet(styles.BUTTON_STYLE)
# self.pushButton_removeSelected.setStyleSheet(styles.BUTTON_REMOVE_STYLE)
# self.tableWidget_existingTCLinks.setStyleSheet(styles.TABLE_STYLE)
# self.progress_bar_projects.setStyleSheet(styles.PROGRESS_BAR_STYLE)
# self.progress_bar_get_tc_links.setStyleSheet(styles.PROGRESS_BAR_STYLE)
# self.progress_bar_link_reqs.setStyleSheet(styles.PROGRESS_BAR_STYLE)
# self.listWidget_reqNumbers.setStyleSheet(styles.LISTWIDGET_STYLE)
# self.label_Password.setStyleSheet(styles.LABEL_STYLE)
# self.label_userName.setStyleSheet(styles.LABEL_STYLE)
# self.label_newLinks.setStyleSheet(styles.LABEL_STYLE)
# self.label_existingTestCases.setStyleSheet(styles.LABEL_STYLE)
# MainWindow.setStyleSheet(styles.APP_BACKGROUND_STYLE)