class AuthData:
    def __init__(self, code, ip_address, mac_address, username, device_info, desk_number):
        self.code = code
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.username = username
        self.device_info = device_info  
        self.desk_number = desk_number  

    def to_dict(self):
        return {
            "code": self.code,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "username": self.username,
            "device_info": self.device_info,  
            "desk_number": self.desk_number
        }
    

class TaskData:
    def __init__(self, task_option_id, room_id, ):
        pass