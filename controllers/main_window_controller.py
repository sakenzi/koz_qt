from api_handlers.auth import login
from models.models import AuthData, TaskData
from system.system_info import SystemInfo
from websocket import create_connection
import threading
from threading import Event
import json

from pathlib import Path
import os


class MainWindowController:
    def __init__(self, view):
        self.view = view
        self.token = None
        self.websocket = None
        self.ws_thread = None
        self.message_received = Event()
        self.room_id = None
        self.task_data = None
        self.last_message = None
        self.message_count = 0

    def websocket_thread(self, websocket_url, token):
        full_url = f"{websocket_url}&access_token={token}"
        print(f"Подключение к WebSocket по адресу: {full_url}")

        try:
            ws = create_connection(full_url)
        except Exception as e:
            print(f"Ошибка подключения к WebSocket: {e}")
            return

        self.websocket = ws

        while True:
            try:
                message = ws.recv()
                self.last_message = message
                self.message_count += 1

                home_dir = Path.home()
                project_folder = home_dir / "koz_project"
                
                try:
                    project_folder.mkdir(exist_ok=True)
                    print(f"Папка жасалды немесе бұндай папка бар: {project_folder}")

                    python_file = project_folder / "1.py"
                    if not python_file.exists():
                        python_file.touch()
                        print(f"Файл жасалды: {python_file}")
                    else:
                        print(f"Файл уже бар: {python_file}")
                except Exception as e:
                    print(f"Ошибка: {e}")

                if self.message_count == 1 and message == "You are connected as client.":
                    print("Первое сообщение — подключение, ждем следующее")
                    continue

                try:
                    message_data = json.loads(message)
                    self.task_data = TaskData.from_dict(message_data)
                    self.message_received.set()
                except json.JSONDecodeError as e:
                    print(f"Ошибка парсинга сообщения: {e}")

            except Exception as e:
                print(f"Ошибка при получении сообщения: {e}")
                break

    def connect_to_websocket(self, token, websocket_url):
        if not websocket_url:
            return

        self.ws_thread = threading.Thread(target=self.websocket_thread, args=(websocket_url, token))
        self.ws_thread.start()


    def authenticate(self, code, username, option, sys_info=SystemInfo()):
        if not all([code, username]):
            return False, "Барлық поляны толтырыңыз"

        auth_data = AuthData(
            code=code,
            ip_address=sys_info.ip_address,
            mac_address=sys_info.mac_address,
            username=username,
            device_info=sys_info.pc_name,
            desk_number=int(option or 0)
        )

        response = login(auth_data.to_dict())

        if response:
            json_response = response.json()
            if "access_token" in json_response:
                self.token = json_response["access_token"]

                self.room_id = json_response.get("room_id")
                if self.room_id is None:
                    return False, "room_id жоқ"

                from api_handlers.tasks import get_websocket_tasks
                websocket_url = get_websocket_tasks(self.room_id)
                self.connect_to_websocket(self.token, websocket_url)

                return True, "Сәтті"
            else:
                return False, "Аутентификация қате: токен жоқ"
        else:
            return False, "Аутентификация қате: серверден жауап жоқ"

    def get_token(self):
        return self.token

    def get_websocket(self):
        return self.websocket

    def has_message(self):
        is_set = self.message_received.is_set()
        return is_set

    def clear_message(self):
        self.message_received.clear()

    def get_task_data(self):
        return self.task_data
    
    def get_room_id(self):
        return self.room_id
