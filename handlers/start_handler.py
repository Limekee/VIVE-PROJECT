from config import bot
from utils import level_selection_functions


def register_start_handler():
    @bot.message_handler(commands=['start'])
    def welcome(message):
        text = "Этот чат-бот создан для обучения английскому!"
        bot.send_message(message.chat.id, text)
        level_selection_functions.level_selection(message)


