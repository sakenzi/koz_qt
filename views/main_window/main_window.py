import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLabel, 
                             QLineEdit, QVBoxLayout)
from PyQt6.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("kӨz")
        self.setGeometry(250, 50, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #856c9e;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        # self.layout.setSpacing()
        # self.layout.setContentsMargins(30, 30, 30, 30)

        self.username_label = QLabel("Қолданушы аты-жөні:")
        self.username_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #555555;
                padding-bottom: 5px;
            }
        """)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Аты-жөніңізді жазыңыз")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit: focus {
                border: 1px solid #1E90FF;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.3);
            }
        """)
        self.layout.addWidget(self.username_input)

        self.code_label = QLabel("Код")
        self.code_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #555555;
                padding-bottom: 5px;
            }
        """)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Кодты енгізіңіз")
        self.code_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit: focus {
                border: 1px solid #1E90FF;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.3);
            }
        """)
        self.layout.addWidget(self.code_input)

        self.start_button = QPushButton("Бастау")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #7ccf80;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
            QPushButton: hover {
                background-color: #195c1c;
            }
            QPushButton: pressed {
                background-color: #166e1a;
            }
        """)

        self.layout.addWidget(self.start_button)
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()