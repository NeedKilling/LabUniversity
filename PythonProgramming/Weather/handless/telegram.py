import requests
import json
from config import TELEGRAM_BOT_KEY

base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/"

def send_message(text: str = "ЧУВАААААААААААААААААААААААК"):
    params = {
        "chat_id": 583730174,
        "text": text
    }
    message_responce = requests.get(f"{base_url}{"sendMessage"}", params=params)
    print(message_responce.text)



# def send_photo():
#     with open("media/ghostGif.gif",mode = "rb") as fileImg:
#         #img = fileImg.read()

#         data = {
#             "animation": fileImg
#         }

#         params = {
#             "chat_id": 583730174

#         }

#         message_responce = requests.get(f"{base_url}{"sendAnimation"}", files = data, params=params)
#         print(message_responce.text)

# send_photo()

def get_updates()->tuple[float,float]:

    updates_response = requests.get(f"{base_url}{"getUpdates"}").json()

    latitude = updates_response["result"][-1]["message"]["location"]["latitude"]
    longitude = updates_response["result"][-1]["message"]["location"]["longitude"]

    #print(json.dumps(updates_response, indent=4, ensure_ascii=False))
    return latitude, longitude