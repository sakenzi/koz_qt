import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLabel, 
                             QLineEdit, QVBoxLayout)
from PyQt5.QtCore import QSize, Qt
from system.system_info import SystemInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("kӨz")
        self.setGeometry(500, 250, 500, 100)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #a3c0f0;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)
        self.sys_info = SystemInfo()
        print(self.sys_info)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        # self.layout.setSpacing()
        # self.layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel("Сынақ алаңына өту")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.title_label)

        self.username_label = QLabel("Қолданушы аты-жөні:")
        self.username_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.username_label)

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

        self.code_label = QLabel("Код:")
        self.code_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.code_label)

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

        self.option_label = QLabel("Нұсқа:")
        self.option_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.option_label)

        self.option_input = QLineEdit()
        self.option_input.setPlaceholderText("Нұсқаны енгізіңіз")
        self.option_input.setStyleSheet("""
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
        self.layout.addWidget(self.option_input)

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