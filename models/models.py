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
    def __init__(self, task_option_id, task_id, option_file, duration, room_id=None):
        self.task_option_id = task_option_id
        self.task_id = task_id
        self.option_file = option_file
        self.duration = duration
        self.room_id = room_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_option_id=data.get("task_option_id"),
            task_id=data.get("task_id"),
            option_file=data.get("option_file", []),
            duration=data.get("duration"),
            room_id=data.get("room_id")
        )
    
    def to_dict(self):
        return {
            "task_option_id": self.task_option_id,
            "task_id": self.task_id,
            "option_file": self.option_file,
            "duration": self.duration,
            "room_id": self.room_id
        }
    

class Answer:
    def __init__(self, order, text):
        self.order = order
        self.text = text

    def to_dict(self):
        return {
            "order": self.order,
            "text": self.text
        }
    
    
class ExamResult:
    def __init__(self, room_id, task_option_id, answers, logs):
        self.room_id = room_id
        self.logs = logs

    def to_dict(self):
        return {
            "room_id": int(self.room_id) if self.room_id is not None else None,
            "logs": self.logs
        }
    
    
class Quote:
    def __init__(self, description):
        self.description = description

    def to_dict(self):
        return {
            "description": self.description
        }