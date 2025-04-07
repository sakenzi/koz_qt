import time
import psutil
# from threading import Thread
# import pygetwindow as gw


class Logs:
    def __init__(self):
        self.running = False
        self.processes = set()
        self.last_site = None

    def log_action(self, message):
        print(f"{time.ctime()}: {message}")

    def start(self):
        if not self.running:
            self.running = True
            self.processes = {p.info['name'] for p in psutil.process_iter(['name'])}

            self.log_action("Мониторинг басталды")

    def stop(self):
        if self.running:
            self.running = False
            self.log_action("Мониторинг біттң")