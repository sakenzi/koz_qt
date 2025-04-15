from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5 import QtGui
from PyQt5 import QtCore
from pathlib import Path
import sys
import os
import random


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

        self.list_quotes = [
            "Сабыр түбі сары алтын",
            "Терпение и время дают больше, чем сила или страсть.",
            "На дне терпения оседает золото."
        ]
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

        self.quote_label = QLabel(self.list_quotes[self.current_quote_index])
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

        # Timer for quote fading
        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.start_quote_fade)
        self.quote_timer.start(5000)  # Change quote every 5 seconds

    def start_quote_fade(self):
        # Fade out
        self.fade_out_animation = QPropertyAnimation(self.quote_label, b"windowOpacity")
        self.fade_out_animation.setDuration(1000)  # 1 second fade out
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve()
        self.fade_out_animation.finished.connect(self.change_quote)
        self.fade_out_animation.start()

    def change_quote(self):
        # Select a random quote different from the current one
        available_quotes = [q for q in self.list_quotes if q != self.quote_label.text()]
        new_quote = random.choice(available_quotes)
        self.quote_label.setText(new_quote)

        # Fade in
        self.fade_in_animation = QPropertyAnimation(self.quote_label, b"windowOpacity")
        self.fade_in_animation.setDuration(1000)  # 1 second fade in
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in_animation.start()

    def check_for_message(self):
        if self.controller and self.controller.has_message():
            print("Сообщение с заданиями получено, переключаемся на ExamWindow")
            self.check_timer.stop()
            self.quote_timer.stop()  # Stop quote timer
            self.switch_to_exam()
            self.controller.clear_message()

    def switch_to_exam(self):
        print("Переход на ExamWindow")
        self.app_manager.show_exam_window()
        self.hide()