from api_handlers.auth import login
from models.models import AuthData
from views.main_window.system.system_info import SystemInfo


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
            desk_number=int(option or "0")
        )

        response = login(auth_data.to_dict())
        if response and "token" in response:
            self.token = response["token"]
            print(self.token)
            return True, "Successfully"
        else:
            return False, "Authenticate Error"
        
    def get_token(self):
        return self.token
