import requests
from settings import telegram_bot_key

base_url = f"https://api.telegram.org/bot{telegram_bot_key}/"

def send_message(text: str = "niggers"):
    text = "ЧУВАААААААААААААААААААААААК"
    params = {
        "chat_id": 583730174,
        "text": text
    }
    message_responce = requests.get(f"{base_url}{"sendMessage"}", params=params)
    print(message_responce.text)



def send_photo():
    with open("media/ghostGif.gif",mode = "rb") as fileImg:
        #img = fileImg.read()

        data = {
            "animation": fileImg
        }

        params = {
            "chat_id": 583730174

        }

        message_responce = requests.get(f"{base_url}{"sendAnimation"}", files = data, params=params)
        print(message_responce.text)

send_photo()

