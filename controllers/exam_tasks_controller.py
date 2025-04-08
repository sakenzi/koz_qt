import time
import psutil
from threading import Thread
import pygetwindow as gw
from models.models import ExamResult, Answer
from api_handlers.exam_tasks import submit_exam_result
import jwt

class Logs:
    def __init__(self):
        self.running = False
        self.processes = set()
        self.last_site = None
        self.log_entries = []

    def log_action(self, message):
        timestamp = time.ctime()
        log_entry = f"{timestamp}: {message}"
        self.log_entries.append(log_entry)
        print(log_entry)

    def monitor_browser_activity(self):
        while self.running:
            try:
                active_window = gw.getActiveWindow()
                if active_window:
                    window_title = active_window.title.strip()
                    for proc in psutil.process_iter(['name']):
                        proc_name = proc.info['name'].lower()
                        if "chrome" in proc_name:
                            browser = "Google Chrome"
                        elif "msedge" in proc_name:
                            browser = "Microsoft Edge"
                        elif "firefox" in proc_name:
                            browser = "Firefox"
                        else:
                            continue
                        if window_title and window_title != self.last_site and window_title != "":
                            self.log_action(f"Зашёл в {browser}: {window_title}")
                            self.last_site = window_title
                        break
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

    def get_logs(self):
        return "\n".join(self.log_entries)

class ExamTasksController:
    def __init__(self, auth_controller=None):
        self.logs = Logs()
        self.room_id = None
        self.task_option_id = None
        self.answers = {}  
        self.auth_controller = auth_controller

    def start_monitoring(self):
        self.logs.start()

    def stop_monitoring(self):
        self.logs.stop()

    def set_task_data(self, task_data):
        self.task_option_id = task_data.task_option_id
        self.room_id = task_data.room_id if task_data.room_id is not None else self.get_room_id_from_auth()
        if self.room_id is None:
            print("Ошибка: room_id не найден ни в task_data, ни в auth_controller")
        print(f"Set room_id: {self.room_id}, task_option_id: {self.task_option_id}")

    def get_room_id_from_auth(self):
        if self.auth_controller:
            # Проверяем наличие метода get_room_id
            get_room_id_method = getattr(self.auth_controller, 'get_room_id', None)
            if get_room_id_method:
                room_id = get_room_id_method()
                if room_id is not None:
                    print(f"Room ID from auth_controller.get_room_id: {room_id}")
                    return room_id
            
            # Пробуем из auth_data
            auth_data = getattr(self.auth_controller, 'get_auth_data', None)
            if auth_data:
                auth_data_result = auth_data()
                room_id = auth_data_result.get("room_id") if auth_data_result else None
                if room_id is not None:
                    print(f"Room ID from auth_data: {room_id}")
                    return room_id
            
            # Пробуем из токена
            token = self.auth_controller.get_token()
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
                room_id = decoded.get("room_id")
                print(f"Room ID from token: {room_id}")
                return room_id
            except Exception as e:
                print(f"Ошибка декодирования токена: {e}")
        print("Room ID не найден в аутентификации")
        return None

    def add_answer(self, order, text):
        # Обновляем или создаём ответ для данного order
        self.answers[order] = Answer(order, text)

    def get_exam_result(self):
        logs = self.logs.get_logs()
        if self.room_id is None:
            print("Предупреждение: room_id is None")
        return ExamResult(
            room_id=self.room_id,
            task_option_id=self.task_option_id,
            answers=list(self.answers.values()),  # Преобразуем словарь в список
            logs=logs
        )

    def submit_result(self, token):
        exam_result = self.get_exam_result()
        return submit_exam_result(exam_result, token)