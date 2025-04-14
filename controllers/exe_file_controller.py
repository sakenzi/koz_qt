import os
import requests
import logging
import re
from urllib.parse import urlparse

async def download_and_save_files(files_data, save_dir):
    downloaded_files = []
    
    api_url = os.getenv("API_URL")
    if not api_url:
        return downloaded_files

    parsed_url = urlparse(api_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}".rstrip('/')

    for file_data in files_data:
        file_path = file_data.get("exe_file_path")
        if not file_path:
            continue

        if not file_path.lower().endswith('.exe'):
            continue

        file_name = os.path.basename(file_path)
        file_name = re.sub(r'[^\w\-\.]', '_', file_name)
        local_path = os.path.join(save_dir, file_name)

        
        file_url = f"{base_url}/{file_path.lstrip('/')}"
        response = requests.get(file_url)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            f.write(response.content)

        downloaded_files.append(local_path)

    return downloaded_files