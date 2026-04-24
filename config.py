import os
import json
from dotenv import load_dotenv
from pydantic import ConfigDict


def load_config():
    #Загружаем конфиг из файла
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    load_dotenv(".env")
    config["tg_bot_token"] = os.getenv("BOT_TOKEN")
    config["weather_token"] = os.getenv("WEATHER_TOKEN")
    return config

config = load_config()
BOT_TOKEN = config["tg_bot_token"]
WEATHER_TOKEN = config["weather_token"]
HELP_MESSAGE = config["help_message"]
START_MESSAGE = config["start_message"]