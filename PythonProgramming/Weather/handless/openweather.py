import json
from typing import Any
import requests
from config import WEATHER_BASE_URL, WEATHER_API_KEY


def get_weather_by_query(city: str) -> None | tuple[Any]:

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units":"metric",
        "lang":"ru"
    }

    weather_response = requests.get(WEATHER_BASE_URL,params = params)
    print(json.dumps(weather_response.json(), indent=4, ensure_ascii=False))
    # try:
    #     # Добавляем таймаут 10 секунд
    #     weather_response = requests.get(WEATHER_BASE_URL, timeout=10,params = params)
    #     weather_response.raise_for_status()  # Проверяем HTTP ошибки
    #     return json.dumps(weather_response.json(), indent = 4, ensure_ascii = False)
    # except requests.exceptions.Timeout:
    #     print(f"Таймаут: не удалось подключиться к API за 10 секунд")
    #     return None
    # except requests.exceptions.ConnectionError:
    #     print("Ошибка соединения. Проверьте интернет.")
    #     return None
    # except requests.exceptions.RequestException as e:
    #     print(f"Ошибка запроса: {e}")
    #     return None
    
   # print(json.dumps(weather_response.json(), indent = 4, ensure_ascii = False))
