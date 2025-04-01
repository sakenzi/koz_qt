import socket
import uuid
import platform


class SystemInfo:
    @staticmethod
    def get_mac_address():
        mac = uuid.getnode()
        mac_address = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        print(mac_address)
        return mac_address

    @staticmethod
    def get_ip_address():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(ip_address)
        return ip_address
        
    @staticmethod
    def get_pc_name():
        print(platform.node())
        return platform.node()

