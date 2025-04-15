from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import os
from controllers.quote_controller import QuoteController

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class WaitingForWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.controller = self.app_manager.get_controller()
        if self.controller is None:
            print("Ошибка: контроллер не передан в WaitingForWindow")

        self.quote_controller = QuoteController()
        self.list_quotes = self.quote_controller.fetch_quotes()
        if not self.list_quotes:
            self.list_quotes = [Quote("Цитаты недоступны")]
        self.current_quote_index = 0

        self.setWindowTitle("Күту зонасы")
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setGeometry(50, 50, 1850, 950)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0c1214;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        loading_layout = QVBoxLayout(self.central_widget)
        loading_layout.setContentsMargins(10, 100, 10, 800)

        loading = QHBoxLayout()
        quote = QHBoxLayout()
        quote.setContentsMargins(100, 250, 100, 100)

        self.loading_label = QLabel(self.central_widget)
        self.loading_gif_path = resource_path("views/waiting_for_window/images/ZZ5H.gif")
        self.loading_gif = QtGui.QMovie(self.loading_gif_path)
        if not self.loading_gif.isValid():
            self.loading_label.setText("Ошибка: GIF не найден или поврежден")
        else:
            self.loading_gif.setScaledSize(QtCore.QSize(100, 100))
            self.loading_label.setMovie(self.loading_gif)
            self.loading_gif.start()

        self.loading_label.setAlignment(Qt.AlignCenter)

        self.quote_label = QLabel(self.list_quotes[self.current_quote_index].description)
        self.quote_label.setStyleSheet("""
            QLabel { color: #868b8f; font-size: 30px; font-weight: bold; }
        """)
        quote.addWidget(self.quote_label)
        
        loading.addWidget(self.loading_label)
        loading_layout.setAlignment(Qt.AlignCenter)
        loading_layout.addLayout(loading)
        loading_layout.addLayout(quote)

        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_for_message)
        self.check_timer.start(1000)

        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.start_quote_fade)
        self.quote_timer.start(4000)

    def start_quote_fade(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.quote_label.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(3000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InBack)
        self.fade_animation.finished.connect(self.change_quote)
        self.fade_animation.start()

    def change_quote(self):
        self.current_quote_index = (self.current_quote_index + 1) % len(self.list_quotes)
        self.quote_label.setText(self.list_quotes[self.current_quote_index].description)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutBack)
        self.fade_animation.start()

    def check_for_message(self):
        if self.controller and self.controller.has_message():
            print("Сообщение с заданиями получено, переключаемся на ExamWindow")
            self.check_timer.stop()
            self.quote_timer.stop()
            self.switch_to_exam()
            self.controller.clear_message()

    def switch_to_exam(self):
        print("Переход на ExamWindow")
        self.app_manager.show_exam_window()
        self.hide()