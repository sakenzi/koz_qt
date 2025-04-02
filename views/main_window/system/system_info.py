import socket
import uuid
import platform


class SystemInfo:
    def __init__(self):
        self.mac_address = self.get_mac_address()
        self.ip_address = self.get_ip_address()
        self.pc_name = self.get_pc_name()

    @staticmethod
    def get_mac_address():
        mac = uuid.getnode()
        mac_address = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        return mac_address

    @staticmethod
    def get_ip_address():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
        
    @staticmethod
    def get_pc_name():
        return platform.node()
    
    def __str__(self):
        return (f"{self.mac_address}\n"
                f"{self.ip_address}\n"
                f"{self.pc_name}")

