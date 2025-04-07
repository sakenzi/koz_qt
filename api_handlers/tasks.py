from dotenv import load_dotenv
import os


load_dotenv()

def get_websocket_tasks(room_id=None):
    base_url = os.getenv("WEBSOCKET_URL")
    if room_id is not None:
        return f"{base_url}?room_id={room_id}"
    return base_url