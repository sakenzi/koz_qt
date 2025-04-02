import requests


def login(data):
    url = "http://localhost:8000/auth/client/login"
    print(data)
    try: 
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправке запроса: {e}")
        return None