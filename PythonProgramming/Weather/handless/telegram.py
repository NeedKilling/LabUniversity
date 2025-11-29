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


def get_updates():
    pass
# def get_updates()->tuple[float,float]:

#     updates_response = requests.get(f"{base_url}{"getUpdates"}").json()

#     # latitude = updates_response["result"][-1]["message"]["location"]["latitude"]
#     # longitude = updates_response["result"][-1]["message"]["location"]["longitude"]
#      # return latitude, longitude
#     print(json.dumps(updates_response, indent=4, ensure_ascii=False))
#     filename = updates_response["result"][-1]["message"]["document"]["file_name"]
#     fileid = updates_response["result"][-1]["message"]["document"]["file_id"]
#     print(filename,fileid)
#     return fileid

# def getFilePath(file_id:str):
#         params = {
#             "file_id": file_id

#         }
#         file_response = requests.get(f"{base_url}{"getFile"}", params=params).json()
#         file_path  = file_response["result"]["file_path"]
#         print(json.dumps(file_response , indent=4, ensure_ascii=False))
#         print(json.dumps(file_path , indent=4, ensure_ascii=False))
#         return file_path
    
#     #getFilePath(get_updates())

# def save_file(file_name,file_path):
#         responce = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_KEY}/{file_path}")

#         with open(f"{file_name}", "wb") as file:
#             file.write(responce.content)

# save_file("name.pdf",getFilePath(get_updates()))



def messageHandler():
    updates_response = requests.get(f"{base_url}{"getUpdates"}").json()
    message = updates_response["result"][-1]["message"]

    if("text" in message):
        send_message(message["text"])
        print(message["text"])
    elif("document" in message):
        send_message(message["document"]["file_name"])
        print(message["document"]["file_name"])
    elif("photo" in message):
        send_message("audio" in message)
        print(message["photo"])
    elif("audio" in message):
        send_message()
        print(message["audio"])
    elif("voice" in message):
        send_message()
        print(message["voice"])
    elif("video" in message):
        send_message()
        print(message["video"])
    elif("location" in message):
        send_message(f"{message["location"]["latitude"]} {message["location"]["longitude"]}")
        print(message["location"]["latitude"],message["location"]["longitude"])
    elif("sticker" in message):
        send_message(message["sticker"]["emoji"])
        print(message["sticker"]["emoji"])    
    elif("reply_to_message" in message):
        send_message()
        print(message["reply_to_message"])
    # if("edited_message" in updates_response["result"][-1]):
    #     print(json.dumps(updates_response["result"][-1]["edited_message"], indent = 4, ensure_ascii = False))
    print(json.dumps(updates_response, indent = 4, ensure_ascii= False))
