import sys
from PyQt5.QtWidgets import QApplication
from main_window.main_window import MainWindow
from exam_window.exam_window import ExamWindow
from waiting_for_window.waiting_for_window import WaitingForWindow


class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow(self)
        self.exam_window = ExamWindow(self)
        self.waiting_window = WaitingForWindow(self)
        self.token = None
        self.websocket = None

    def set_token(self, token):
        self.token = token
        print(f"Token stored in ApplicationManager: {self.token}")

    def get_token(self):
        return self.token
    
    def set_websocket(self, websocket):
        self.websocket = websocket

    def get_websocket(self):
        return self.websocket

    def show_main_window(self):
        self.main_window.show()
        self.exam_window.hide()
        self.waiting_window.hide()

    def show_exam_window(self):
        self.exam_window.show()
        self.main_window.hide()
        self.waiting_window.hide()

    def show_waiting_window(self):
        self.waiting_window.show()
        self.main_window.hide()
        self.exam_window.hide()

    def run(self):
        self.show_main_window()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_manager = ApplicationManager()
    app_manager.run()