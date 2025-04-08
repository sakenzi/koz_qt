from api_handlers.auth import login
from models.models import AuthData, TaskData
from system.system_info import SystemInfo
import websocket
import threading
from threading import Event 
import json

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
        ws = websocket.WebSocket()
        print(f"Подключение к WebSocket по адресу: {websocket_url}")
        ws.connect(websocket_url, header={"Authorization": f"{token}"})
        self.websocket = ws
        print(f"WebSocket успешно подключен с токеном: {token}")
        while True:
            message = ws.recv()
            # print(f"Сообщение получено: {message}")
            self.last_message = message
            self.message_count += 1
            if self.message_count == 1 and message == "You are connected as client.":
                print("Первое сообщение — подключение, ждем следующее")
                continue
            try:
                message_data = json.loads(message)
                self.task_data = TaskData.from_dict(message_data)
                self.message_received.set()  
            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга сообщения: {e}")

    def connect_to_websocket(self, token, websocket_url):
        if not websocket_url:
            print("WebSocket URL не указан")
            return
        print("Создание потока WebSocket...")
        self.ws_thread = threading.Thread(
            target=self.websocket_thread,
            args=(websocket_url, token),
            daemon=True
        )
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

        print(f"Данные для аутентификации: {auth_data.to_dict()}")
        response = login(auth_data.to_dict())
        print(f"Тип ответа: {type(response)}, значение: {response}")

        if response:
            json_response = response.json()
            print(f"JSON ответ: {json_response}")
            if "access_token" in json_response:
                self.token = json_response["access_token"]
                print(f"Токен сохранен: {self.token}")

                self.room_id = json_response.get("room_id")
                if self.room_id is None:
                    print("Ошибка: room_id не найден")
                    return False, "room_id жоқ"

                print(f"Получен room_id: {self.room_id}")

                from api_handlers.tasks import get_websocket_tasks
                websocket_url = get_websocket_tasks(self.room_id)
                print(f"Подключение к WebSocket URL: {websocket_url}")
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
        print(f"Проверка сообщения: {is_set}, Количество сообщений: {self.message_count}")
        return is_set

    def clear_message(self):
        self.message_received.clear()
        print("Событие сообщения сброшено")

    def get_task_data(self):
        return self.task_data
    
    def get_room_id(self):
        return self.room_id