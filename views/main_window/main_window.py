import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QLabel, 
                             QLineEdit, QVBoxLayout, QMessageBox, QFormLayout, QComboBox, QApplication)
from PyQt5.QtCore import Qt, QTranslator, QEvent
from system.system_info import SystemInfo
from controllers.main_window_controller import MainWindowController
from system.tray_manager import TrayManager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.translator = QTranslator()
        self.app_manager.set_translator(self.translator)

        self.tray_manager = TrayManager(self)

        self.setWindowTitle("kӨz")
        self.setGeometry(700, 250, 500, 100)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
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

        self.controller = MainWindowController(self)

        self.language_combo = QComboBox()
        self.language_combo.addItem("Қазақша", "kz")
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.addItem("English", "en")
        self.setStyleSheet("""
            QComboBox {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_combo)

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

        auth_layout = QFormLayout()

        self.username_label = QLabel("Қолданушы аты-жөні:")
        self.username_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        auth_layout.addWidget(self.username_label)

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
            QLineEdit:focus {
                border: 1px solid #1E90FF;
            }
        """)
        auth_layout.addWidget(self.username_input)

        self.code_label = QLabel("Код:")
        self.code_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        auth_layout.addWidget(self.code_label)

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
            QLineEdit:focus {
                border: 1px solid #1E90FF;
            }
        """)
        auth_layout.addWidget(self.code_input)

        self.option_label = QLabel("Нұсқа:")
        self.option_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        auth_layout.addWidget(self.option_label)

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
            QLineEdit:focus {
                border: 1px solid #1E90FF;               
            }
        """)
        auth_layout.addWidget(self.option_input)

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
            QPushButton:hover {
                background-color: #195c1c;
            }
            QPushButton:pressed {
                background-color: #166e1a;
            }
        """)

        self.start_button.clicked.connect(self.on_start_button_clicked)
        auth_layout.addWidget(self.start_button)

        self.layout.addLayout(auth_layout)

    def change_language(self):
        language = self.language_combo.currentData()
        self.app_manager.set_language(language)
        base_path = os.path.dirname(os.path.abspath(__file__))
        translation_path = os.path.join(base_path, "translations", f"{language}.qm")
        success = self.translator.load(translation_path)

        if not success:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить перевод для языка {language}")
            return

        QApplication.instance().installTranslator(self.translator)
        self.update_ui_texts()
        self.app_manager.update_all_windows()
        self.event(QEvent(QEvent.LanguageChange))

    def update_ui_texts(self):
        self.title_label.setText(self.tr("Сынақ алаңына өту"))
        self.username_label.setText(self.tr("Қолданушы аты-жөні:"))
        self.username_input.setPlaceholderText(self.tr("Аты-жөніңізді жазыңыз"))
        self.code_label.setText(self.tr("Код:"))
        self.code_input.setPlaceholderText(self.tr("Кодты енгізіңіз"))
        self.option_label.setText(self.tr("Нұсқа:"))
        self.option_input.setPlaceholderText(self.tr("Нұсқаны енгізіңіз"))
        self.start_button.setText(self.tr("Бастау"))
        self.setWindowTitle(self.tr("kӨz"))

    def on_start_button_clicked(self):
        success, message = self.controller.authenticate(
            self.code_input.text(),
            self.username_input.text(),
            self.option_input.text(),
            self.sys_info
        )
        if success:
            token = self.controller.get_token()
            websocket = self.controller.get_websocket()
            self.app_manager.set_token(token)
            self.app_manager.set_websocket(websocket)
            self.app_manager.set_controller(self.controller)
            QMessageBox.information(self, "Сәтті", message)
            self.app_manager.show_waiting_window()
            self.hide()
        else:
            QMessageBox.critical(self, "Сәтті емес", message)