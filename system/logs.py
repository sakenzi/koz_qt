import time
import psutil
from threading import Thread
import pygetwindow as gw

class Logs:
    def __init__(self):
        self.running = False
        self.processes = set()
        self.last_site = None

    def log_action(self, message):
        print(f"{time.ctime()}: {message}")

    def monitor_browser_activity(self):
        while self.running:
            try:
                active_window = gw.getActiveWindow()
                if active_window:
                    window_title = active_window.title.strip()  
                    
                    # for proc in psutil.process_iter(['name']):
                    #     proc_name = proc.info['name'].lower()
                    #     if "chrome" in proc_name:
                    #         browser = "Google Chrome"
                    #     elif "msedge" in proc_name:
                    #         browser = "Microsoft Edge"
                    #     elif "firefox" in proc_name:
                    #         browser = "Firefox"
                    #     else:
                    #         continue

                    #     if window_title and window_title != self.last_site and window_title != "":
                    #         self.log_action(f"Зашёл: {window_title}")
                    #         self.last_site = window_title
                    #     break
                    self.log_action(f"Зашёл: {window_title}")
                else:
                    self.last_site = None  
            except Exception as e:
                self.log_action(f"Ошибка при мониторинге: {e}")
            
            time.sleep(1)  

    def start(self):
        if not self.running:
            self.running = True
            self.processes = {p.info["name"] for p in psutil.process_iter(['name'])}
            
            self.log_action("Тестовый вывод: мониторинг начат")

            browser_thread = Thread(target=self.monitor_browser_activity)
            browser_thread.daemon = True
            browser_thread.start()

            self.log_action("Мониторинг активности начат")

    def stop(self):
        if self.running:
            self.running = False
            self.log_action("Мониторинг остановлен")