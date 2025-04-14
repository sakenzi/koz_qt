import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

API_URL = os.getenv("API_URL")  # Add your API URL to .env, e.g., "https://api.example.com/files"

async def fetch_exe_files():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        return []