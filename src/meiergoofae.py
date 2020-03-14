import sys
import time
import random
import datetime
import logging
import configparser
import json
import telepot
import quickstart as qs
from drinks import CocktailHandler


class MeiergoofaBot(object):

    def __init__(self, config: configparser.RawConfigParser, api_config: configparser.RawConfigParser):
        self.id_to_name = dict()
        self.name_to_id = dict()
        self.config = config
        self.api_config = api_config

        self.bot = telepot.Bot(self.api_config["API"]["key"])

        self.cocktail_handler = CocktailHandler(self.config["Cocktails"], self.bot)

    def handle(self, msg: dict):
        # Get fields from message
        chat_id = msg['chat']['id']
        command = msg['text']
        command = command.lower()

        logging.info(
            f"Got command: {command} from {self.id_to_name[chat_id] if chat_id in self.id_to_name else chat_id}")

        # First adding of bot
        if command == '/start':
            firstname = msg['from']['first_name']
            if chat_id not in self.id_to_name:
                self.id_to_name[chat_id] = firstname
                self.name_to_id[firstname] = chat_id
            self.bot.sendMessage(chat_id, f"Hi {firstname}")

        # Greeting
        elif command == 'hello':
            self.bot.sendMessage(chat_id, 'hello back')

        # Time
        elif command == 'time':
            self.bot.sendMessage(chat_id, str(datetime.datetime.now()))

        # Who is connected
        elif command == 'dict':
            self.bot.sendMessage(chat_id, 
                f"Everybody that is currently connected: \n" + ", ".join(self.name_to_id.keys()) 
                if self.name_to_id else "Nobody connected"
            )

        # Send random stuff
        elif command == 'send':
            zahl = random.randint(1, 10)
            for _ in range(1, zahl):
                self.bot.sendMessage(chat_id, 'Hello Domi')
                time.sleep(1)

        # Get events
        elif command == 'events':
            self.bot.sendMessage(chat_id, qs.getCalendarEntries())

        elif command == "cocktail":
            self.cocktail_handler.handle(msg)

        # Send back same message
        else:
            self.bot.sendMessage(chat_id, f'{command} yourself')

    def start(self):
        self.bot.message_loop(self.handle)
        logging.info("Bot started")


def main():
    # Config file
    config = configparser.RawConfigParser()
    config.read('config.ini', encoding="utf8")

    api_config = configparser.RawConfigParser()
    api_config.read('api.ini', encoding="utf8")

    # Logging
    logging_arguments = dict()
    logging_arguments["format"] = config["Logging"]["format"]
    logging_arguments["level"] = logging.getLevelName(
        config["Logging"]["level"])
    if config["Logging"].getboolean("to_file"):
        logging_arguments["filename"] = config["Logging"]['logfile']
    logging.basicConfig(**logging_arguments)

    # Start botting
    bot = MeiergoofaBot(config, api_config)
    bot.start()

    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
