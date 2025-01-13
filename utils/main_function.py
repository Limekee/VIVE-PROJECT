from config import bot
from telebot import types
from .level_selection_functions import level_selection
from .plan_functions import plan_output
from .talking_functions import talking_output
from .vocabulary_functions import vocabulary_output


def main_menu_processing(message):
    if message.text.lower() == "уровень языка":
        level_selection(message)

    elif message.text.lower() == 'план':
        plan_output(message)

    elif message.text.lower() == 'общение':
        talking_output(message, main_menu_markup)

    elif message.text.lower() == 'словарь':
        vocabulary_output(message, main_menu_markup)


def main_menu_markup(message):
    """Отправляет макет главного меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_plan = types.KeyboardButton('План')
    button_vocabulary = types.KeyboardButton('Словарь')
    button_dialogue = types.KeyboardButton('Общение')
    markup.row(button_plan, button_vocabulary, button_dialogue)
    button_level = types.KeyboardButton("Уровень языка")
    markup.add(button_level)
    bot.send_message(message.chat.id,"Выбери один из трёх режимов обучения:", reply_markup=markup)
    bot.register_next_step_handler(message, main_menu_processing)