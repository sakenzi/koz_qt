from api_handlers.auth import login
from models.models import AuthData
from system.system_info import SystemInfo
import websockets


class MainWindowController:
    def __init__(self, view):
        self.view = view
        self.access_token = None

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
        print(f"{type(response)}, мәні: {response}")
        if response:  
            json_response = response.json()  
            print(f"JSON response: {json_response}")
            if "access_token" in json_response:  
                self.token = json_response["access_token"]
                print(f"Token saved: {self.token}")
                return True, "Сәтті"
            else:
                return False, "Аутентификация қате: токен жоқ"
        else:
            return False, "Аутентификация қате: серверден жауап жоө"

    def get_token(self):
        return self.token
    