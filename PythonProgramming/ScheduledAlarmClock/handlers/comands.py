
from .file_handler import userCsv
from config import CONFIG
path = CONFIG["path"]
greatings = CONFIG["message"]["greatings"]
remembered = CONFIG["message"]["remembered"]



def command_start(message):
    user = {
        "chat_id": message["chat"]["id"],
        "username": message["chat"].get("username", ""),
        "first_name": message["chat"]["first_name"]
    }
    new_user = userCsv(user)
    if new_user:
        return greatings.format(name=user["first_name"])
    else:
        return greatings.format(name=user["first_name"])
        

