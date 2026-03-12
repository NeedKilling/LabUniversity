# import tomllib
# from decouple import configur

# # with open("config.toml" , mode = "rb") as file:
# #     fileConfig = tomllib.load(file)

# TELEGRAM_BOT_KEY = configur("TELEGRAM_BOT_KEY")
# # GROUP = fileConfig["group"]
# # TYPE = fileConfig["type"]
# # ID = fileConfig["id"]




from dotenv import load_dotenv
import os
import json
load_dotenv()
TELEGRAM_BOT_KEY  = os.getenv("TELEGRAM_BOT_KEY")
with open("config.json", encoding="utf-8") as file:
    CONFIG = json.load(file)