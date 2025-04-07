import requests
from dotenv import load_dotenv
import os


load_dotenv()

def login(data):
    url = os.getenv("API_AUTH_URL")
    print(data)
    try: 
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"қате: {e}")