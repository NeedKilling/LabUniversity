import csv
import os
import json
from config import CONFIG
from utils.schedule_parser import get_schedule 
path = CONFIG["path"]

def userCsv(data):
    if os.path.exists(path["user_csv"]):
        user_exists = False

        with open(path["user_csv"], 'r', encoding='utf-8') as f:
            for line in f:
                if str(data["chat_id"]) in line:
                    user_exists = True
                    break

        if(not user_exists):
            with open(path["user_csv"], "a",newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data.values())
                return True
        else: 
            return False
        
    else:
        with open(path["user_csv"], "w",newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())

def groupJson(GROUP,metod):
    if(metod == "w"):
        group_json = get_schedule(GROUP)
        if(group_json):
            with open(f"{path["groups"]}/{GROUP}.json", metod, encoding="utf-8") as file:
                file.write(group_json)
            return "расписание получено"
        else:
            return "что-то пошло не так"
    else:
        with open(f"{path["groups"]}/{GROUP}.json", metod, encoding="utf-8") as file:
            return json.load(file)