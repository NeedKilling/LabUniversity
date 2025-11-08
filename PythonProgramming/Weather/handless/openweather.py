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
   
    
# def get_weather_by_location(latitude: float, longitude: float)->str:
     
#      params = {
#         "lat": latitude ,
#         "lon": longitude,

#         "appid": WEATHER_API_KEY,
#         "units":"metric",
#         "lang":"ru"
#     }
#         weather = requests.get(WEATHER_BASE_URL,params = params)

def get_weather_by_location(latitude:float, longitude:float)->str:
    params = {"lat": latitude,
              "long": longitude,
              "appid": WEATHER_API_KEY,
              "units": "metric",
              "lang": "ru"
    }
    weather = requests.get(WEATHER_BASE_URL, params=params)

    if weather.status_code == 200:
        temp = weather.json()["main"]["temp"]
        description = weather.json()["weather"][0]["description"]

        return f"temp: {temp} \n decs: {description}"
    
