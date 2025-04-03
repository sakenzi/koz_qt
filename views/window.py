from PyQt5.QtCore import Qt
import time
from main_window.main_window import MainWindow
from main_window.system.system_info import SystemInfo
from waiting_for_window.wainting_for_window import WaitingForWindow


class Window(MainWindow):
    def __init__(self):
        super().__init__()

        self.sys_info = SystemInfo()

    def open_waiting_for_window(self):
        self.waiting_for_window = WaitingForWindow()
        self.waiting_for_window.show()
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()