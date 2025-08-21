import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(1700, 800)
    window.show()
    sys.exit(app.exec())
