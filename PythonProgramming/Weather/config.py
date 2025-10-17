import tomllib
from decouple import config

with open("config.toml" , mode = "rb") as tomlConfig:
    configurate = tomllib.load(tomlConfig)



WEATHER_BASE_URL = configurate["weather_url"]
WEATHER_API_KEY = config("WEATHER_KEY")