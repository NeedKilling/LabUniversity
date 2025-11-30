import requests
import json
from time import sleep
import csv
from datetime import date, datetime
import os


TELEGRAM_BOT_KEY = "8492816044:AAFdtW6dBJhUfo5DCmnTwgcO2s2V0RkETHE"
# CHAT_ID = 583730174
base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/"
active_user = set()
last_save_date = None 

users = []

def save_step_to_file(id, date,step: int = 0):
    if os.path.isfile(f"{id}.csv"):
        with open(f"{id}.csv", "a",newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, step])
    else:
        with open(f"{id}.csv", "w",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "steps"])



def get_week_stats(user_id):
    """Минимальная статистика за неделю"""
    filename = f"{user_id}.csv"
    if not os.path.isfile(filename):
        return "Нет данных"
    steps = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) >= 2:
                steps.append(int(row[1]))
    last_week = steps[-7:] if len(steps) >= 7 else steps
    total = sum(last_week)
    
    return f"Неделя: {total} шагов"

def get_month_stats(user_id):
    """Минимальная статистика за месяц"""
    filename = f"{user_id}.csv"
    if not os.path.isfile(filename):
        return "Нет данных"
    
    steps = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                steps.append(int(row[1]))
    last_month = steps[-30:] if len(steps) >= 30 else steps
    total = sum(last_month)
    
    return f"Месяц: {total} шагов"

def get_quarter_stats(user_id):
    """Минимальная статистика за квартал"""
    filename = f"{user_id}.csv"
    if not os.path.isfile(filename):
        return "Нет данных" 
    steps = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                steps.append(int(row[1]))
    last_quarter = steps[-90:] if len(steps) >= 90 else steps
    total = sum(last_quarter)
    return f"Квартал: {total} шагов"


def save_last_steps():
    """Сохраняет последние шаги всех пользователей в 23:59"""
    global last_save_date
    now = datetime.now()
    today = date.today()
    if now.hour == 23 and now.minute == 59:
        if last_save_date != today:
            print("Время 23:59! Сохраняем данные всех пользователей...")
            for user in users:
                if user.get('steps') and len(user['steps']) > 0:
                    user_id = user["id"]
                    last_step = user['steps'][-1] 
                    save_step_to_file(user_id, today, last_step)
                    print(f"Сохранено для {user['first_name']}: {last_step} шагов")
            last_save_date = today
            print("Все данные сохранены!")
            return True
        else:
            if now.second % 30 == 0:
                print("Время 23:59 - данные уже сохранены сегодня")
    else:
        if last_save_date == today and (now.hour != 23 or now.minute != 59):
            last_save_date = None
            print("Флаг сохранения сброшен на следующий день")
    
    return False

def send_message(text: str, chat_id: int):
    params = {
        "chat_id": int(chat_id),
        "text": text,
        "parse_mode": "MarkdownV2"
    }
    message_responce = requests.get(f"{base_url}{"sendMessage"}", params=params)
    print(message_responce.text)

def messageHandler():

    updates_response = requests.get(f"{base_url}{"getUpdates"}").json()

    if "result" not in updates_response or len(updates_response["result"]) == 0:
        print(updates_response)
    else:

        message = updates_response["result"][-1]["message"]
        
        if("text" in message):
            userId = message["chat"]["id"]

            if(message["text"].isdigit()):

                for item in users:
                    if item["id"] == userId:
                        step = int(message["text"])
                        item["steps"].append(step)
                dateNow = date.today()
                
                
                # save_step(userId,dateNow,step)
                print("Засчитано")
            else:
                print("""*Вы прислали что-то не то* 
                        > напишите общеее количество шагов
                      """)

            match  message["text"]:
                case "/start":
                    if userId not in active_user:
                        active_user.add(userId)
                        userName = message["chat"]["first_name"]
                        
                        user = {}
                        user["id"] = message["chat"]["id"]
                        user["first_name"] = message["chat"]["first_name"]
                        user["steps"] = []
                        users.append(user)

                        text = f"""
            *Здравствуй, {userName}\\!* 👋
            *Это телеграмм бот для сбора статистики шагов*
            📊 _Бот принимает сообщение \\- число шагов_
            🔼 *У бота есть команды для статистики шагов:*
                • *Среднее за неделю*  ```/week```
                • *Среднее за месяц*   ```/month``` 
                • *Среднее за квартал* ```/quarter```
            _Просто отправляйте количество шагов каждый день, а бот позаботится о статистике\\!_ 🚶‍♂️
            """         
                        # dateNow = date.today()
                        # save_step(userId,dateNow,"w")
                        send_message(text, userId)
                    else:
                        send_message("Отправляйте количество шагов", userId)
                        print(f"Пользователь уже в active_user: {userId}")
                case "/week":
                        stats = get_week_stats(userId)
                        send_message(stats, userId)
                    
                case "/month":
                        stats = get_month_stats(userId)
                        send_message(stats, userId)
                    
                case "/quarter":
                        stats = get_quarter_stats(userId)
                        send_message(stats, userId)    
           

            


        # elif("document" in message):
        #     send_message(message["document"]["file_name"])
        #     print(message["document"]["file_name"])
        # elif("photo" in message):
        #     send_message("audio" in message)
        #     print(message["photo"])
        # elif("audio" in message):
        #     send_message()
        #     print(message["audio"])
        # elif("voice" in message):
        #     send_message()
        #     print(message["voice"])
        # elif("video" in message):
        #     send_message()
        #     print(message["video"])
        # elif("location" in message):
        #     send_message(f"{message["location"]["latitude"]} {message["location"]["longitude"]}")
        #     print(message["location"]["latitude"],message["location"]["longitude"])
        # elif("sticker" in message):
        #     send_message(message["sticker"]["emoji"])
        #     print(message["sticker"]["emoji"])    
        # elif("reply_to_message" in message):
        #     send_message()
        #     print(message["reply_to_message"])
        # if("edited_message" in updates_response["result"][-1]):
        #     print(json.dumps(updates_response["result"][-1]["edited_message"], indent = 4, ensure_ascii = False))
        print(json.dumps(message, indent = 4, ensure_ascii= False))
        print(userId)


        requests.get(f"{base_url}getUpdates", params={"offset": updates_response["result"][-1]["update_id"] + 1})
        print(users)

while(True):
    messageHandler()
    save_last_steps()
    sleep(5)

