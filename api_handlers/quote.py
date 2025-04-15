import os
from dotenv import load_dotenv
import requests


load_dotenv()

api = os.getenv("API_BASE_URL")

def get_quote():
    data = requests.get(f"{api}/quotes/all/quotes")
    return data

