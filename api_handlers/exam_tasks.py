import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("API_BASE_URL")
def submit_exam_result(exam_result, token):
    exam_submit_url = f"{api}/tasks/end_task"
    if not exam_submit_url:
        print("Ошибка: EXAM_SUBMIT_URL не найден в переменных окружения")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = json.dumps(exam_result.to_dict(), ensure_ascii=False)
    print(f"Отправляемые данные в JSON: {data}")  
    try:
        response = requests.post(exam_submit_url, data=data, headers=headers)
        print(f"Ответ сервера: {response.status_code}, {response.text}")
        if response.status_code == 200:
            print("Тамаша: Результаты успешно отправлены")
            return True
        else:
            print(f"Ошибка: Сервер вернул код {response.status_code}. Тело ответа: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return False