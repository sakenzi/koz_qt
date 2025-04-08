import sys
from PyQt5.QtWidgets import QApplication
from main_window.main_window import MainWindow
from exam_window.exam_window import ExamWindow
from waiting_for_window.waiting_for_window import WaitingForWindow


class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow(self)
        self.exam_window = None  
        self.waiting_window = None  
        self.token = None
        self.websocket = None
        self.controller = None  

    def set_token(self, token):
        self.token = token
        print(f"Token stored in ApplicationManager: {self.token}")

    def get_token(self):
        return self.token
    
    def set_websocket(self, websocket):
        self.websocket = websocket

    def get_websocket(self):
        return self.websocket

    def set_controller(self, controller):
        self.controller = controller
        print("Controller установлен в ApplicationManager")

    def get_controller(self):
        return self.controller

    def show_main_window(self):
        self.main_window.show()
        if self.exam_window:
            self.exam_window.hide()
        if self.waiting_window:
            self.waiting_window.hide()

    def show_exam_window(self):
        if not self.exam_window:
            self.exam_window = ExamWindow(self)
        self.exam_window.show()
        self.main_window.hide()
        if self.waiting_window:
            self.waiting_window.hide()

    def show_waiting_window(self):
        if not self.waiting_window:
            self.waiting_window = WaitingForWindow(self)
        self.waiting_window.show()
        self.main_window.hide()
        if self.exam_window:
            self.exam_window.hide()

    def run(self):
        self.show_main_window()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_manager = ApplicationManager()
    app_manager.run()