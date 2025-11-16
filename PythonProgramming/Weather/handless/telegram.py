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

    # latitude = updates_response["result"][-1]["message"]["location"]["latitude"]
    # longitude = updates_response["result"][-1]["message"]["location"]["longitude"]
     # return latitude, longitude
    print(json.dumps(updates_response, indent=4, ensure_ascii=False))
    filename = updates_response["result"][-1]["message"]["document"]["file_name"]
    fileid = updates_response["result"][-1]["message"]["document"]["file_id"]
    print(filename,fileid)
    return fileid

def getFilePath(file_id:str):
        params = {
            "file_id": file_id

        }
        file_response = requests.get(f"{base_url}{"getFile"}", params=params).json()
        file_path  = file_response["result"]["file_path"]
        print(json.dumps(file_response , indent=4, ensure_ascii=False))
        print(json.dumps(file_path , indent=4, ensure_ascii=False))
        return file_path
    
    #getFilePath(get_updates())

def save_file(file_name,file_path):
        responce = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_KEY}/{file_path}")

        with open(f"{file_name}", "wb") as file:
            file.write(responce.content)

save_file("name.pdf",getFilePath(get_updates()))