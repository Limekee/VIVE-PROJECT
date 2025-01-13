from config import bot
from telebot import types


def level_selection(message):
    """Отправляет сообщение с выбором уровня"""
    markup = types.InlineKeyboardMarkup()
    button_A1 = types.InlineKeyboardButton('A1', callback_data='level1')
    button_A2 = types.InlineKeyboardButton('A2', callback_data='level2')
    markup.row(button_A1, button_A2)
    button_B1 = types.InlineKeyboardButton('B1', callback_data='level3')
    button_B2 = types.InlineKeyboardButton('B2', callback_data='level4')
    markup.row(button_B1, button_B2)
    button_C1 = types.InlineKeyboardButton('C1', callback_data='level5')
    markup.row(button_C1)
    bot.send_message(message.chat.id, "Выбери свой уровень:", reply_markup=markup)




