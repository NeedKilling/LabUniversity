from dotenv import load_dotenv
import os

load_dotenv()

telegram_bot_key = os.getenv("TELEGRAB_BOT_KEY")

print(telegram_bot_key)