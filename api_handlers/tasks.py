from dotenv import load_dotenv
import os


load_dotenv()

api = os.getenv("WEBSOCKET_URL")

def get_websocket_tasks(room_id=None):
    base_url = f"{api}/tasks_ws/ws"
    if room_id is not None:
        return f"{base_url}?room_id={room_id}"
    return base_url