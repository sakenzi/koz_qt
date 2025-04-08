import requests
from dotenv import load_dotenv
import os


load_dotenv()

api = os.getenv("API_BASE_URL")

def login(data):
    url = f"{api}/auth/client/login"
    print(data)
    try: 
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"қате: {e}")