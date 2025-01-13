from config import bot, DB_NAME
from telebot import types
from services import working_with_SQL


def plan_output(message):
    """Выводит список всех тем для конкретного уроня языка"""
    user_id = message.from_user.id
    user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
    user_level_name = working_with_SQL.get_level_name(DB_NAME, user_level_id)

    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    next_level = levels[user_level_id]

    all_theory = working_with_SQL.get_all_theory(DB_NAME, user_level_id)
    markup = types.InlineKeyboardMarkup()
    for theory in all_theory:
        id = 'theory' + str(theory[0])
        topic_name = theory[2]

        topic_name_button = types.InlineKeyboardButton(f'{topic_name}', callback_data=id)
        markup.add(topic_name_button)

    text = f"Чтобы вам перейти с {user_level_name} на {next_level} вам нужно изучить:"
    bot.send_message(message.chat.id, text, reply_markup=markup)