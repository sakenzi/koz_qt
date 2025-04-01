from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow)
import sys


class ExamWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Экзамен алаңы")
        self.setGeometry(250, 50, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #a3c0f0;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        
app = QApplication(sys.argv)

window = ExamWindow()
window.show()

app.exec()