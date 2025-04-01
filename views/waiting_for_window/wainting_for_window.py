import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow)


class WaitingForWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Күту зонасы")
        self.setGeometry(250, 50, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #a3c0f0;
                border: thick double #32a1ce;
                border-radius: 20px;
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

app = QApplication(sys.argv)

window = WaitingForWindow()
window.show()

app.exec()