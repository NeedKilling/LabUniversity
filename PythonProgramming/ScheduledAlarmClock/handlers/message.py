import requests
import json
from config import TELEGRAM_BOT_KEY
from .comands import command_start
from utils.schedule_parser import get_schedule 
from .file_handler import groupJson
from .schedule_group import buttons
import os


from config import CONFIG
path = CONFIG["path"]




base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/"

def send_message(chat_id, text: str = "",with_buttons=False):
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if with_buttons:
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "📅 Сегодня", "callback_data": "today"},
                    {"text": "📆 Завтра", "callback_data": "tomorrow"}
                ],
                [
                    {"text": "📊 Неделя", "callback_data": "week"}
                ]
            ]
        }
        params["reply_markup"] = json.dumps(keyboard)
    message_responce = requests.get(f"{base_url}{"sendMessage"}", params=params)
    print(message_responce.text)

users = {}
def messageHandler():
    


    updates_response = requests.get(f"{base_url}{"getUpdates"}").json()
    if "result" not in updates_response or len(updates_response["result"]) == 0:
        print(updates_response)
    else:
        requests.get(f"{base_url}getUpdates", params={"offset": updates_response["result"][-1]["update_id"] + 1})
        message = {}
        userId = None

        if("message" in updates_response["result"][-1]):   
            message = updates_response["result"][-1]["message"]
            userId = message["chat"]["id"]
        else: 
            # print(json.dumps(updates_response, indent = 4, ensure_ascii= False))
            callback_query = updates_response["result"][-1]["callback_query"]
            message = callback_query["message"]
            userId = message["chat"]["id"]
            
        
        
        



        if("text" in message):
            
            match message["text"]:
                case "/start":
                    send_message(userId,command_start(message))
                case _:

                    
                    if("-" in message["text"]):

                        GROUP = message["text"]
                        users["userId"] = userId
                        users["GROUP"] = GROUP
                        

                        if(not os.path.exists(f"{path["groups"]}/{GROUP}.json")):
                            
                            send_message(userId,"Идет загрузка расписания")
                            # вот тут меняй вынеси отсюда 
                            # group_json = get_schedule(GROUP)
                            # if(group_json):
                            #     groupJson(GROUP,group_json, "w")
                            send_message(userId,groupJson(GROUP, "w"), True)
                        

                            # else:
                            #     send_message(userId,"что-то не так")
                        else:
                            send_message(userId,f"расписание групы есть.", True)
                        


                        
                          
                    else:
                        send_message(userId,message["text"])











        elif("document" in message):
            send_message(userId,message["document"]["file_name"])
            print(userId,message["document"]["file_name"])
        elif("photo" in message):
            send_message(userId, "audio" in message)
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
            send_message(userId, f"{message["location"]["latitude"]} {message["location"]["longitude"]}")
            print(message["location"]["latitude"],message["location"]["longitude"])
        elif("sticker" in message):
            send_message(userId, message["sticker"]["emoji"])
            print(message["sticker"]["emoji"])    

        print(json.dumps(updates_response, indent = 4, ensure_ascii= False))

        if("callback_query" in updates_response["result"][-1]):
            callback_data = callback_query["data"]
            user_id = callback_query["from"]["id"]

            
            response = buttons(callback_data, users["GROUP"],"r")

            send_message(userId,f"Нажата кнопка: {callback_data} пользователем {user_id}")
            send_message(userId,response)