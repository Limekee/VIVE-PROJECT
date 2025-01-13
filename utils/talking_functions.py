from config import bot, DB_NAME
from telebot import types
from services import working_with_SQL
from services import gpt_service


def talking_output(message, returned_main_menu):
    """Создает таблицу для чата с пользователем, ждет сообщения от пользователя"""
    user_id = message.from_user.id
    working_with_SQL.initialization_chat(DB_NAME, user_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_analytics = types.KeyboardButton('Аналитика')
    markup.add(button_analytics)

    bot.send_message(message.chat.id, "Можете начинать общение!", reply_markup=markup)

    bot.register_next_step_handler(message, chat, returned_main_menu=returned_main_menu)


def chat(message, returned_main_menu):
    # Данный блок "if" отправляет пользователю аналитику по чату
    if message.text.lower() == 'аналитика':
        user_id = message.from_user.id
        user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
        user_level_name = working_with_SQL.get_level_name(DB_NAME,
                                                          user_level_id)
        str_of_user_messages = working_with_SQL.get_all_user_messages(DB_NAME,
                                                                      user_id)

        if str_of_user_messages:
            bot_text = gpt_service.get_gpt_analysis(str_of_user_messages,
                                                    user_level_name)
            bot.send_message(message.chat.id, bot_text)

            working_with_SQL.clear_table(DB_NAME, user_id)

            returned_main_menu(message)

        else:
            bot.send_message(message.chat.id,
                             'Диалог только начался! Нечего анализировать')

            returned_main_menu(message)

    #Блок 'else' отправляет сообщения chat-gpt в роли собеседника
    else:
        user_id = message.from_user.id
        user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
        user_level_name = working_with_SQL.get_level_name(DB_NAME, user_level_id)

        user_text = message.text
        working_with_SQL.save_user_message(DB_NAME, user_id, user_text)
        all_chat = working_with_SQL.get_all_chat(DB_NAME, user_id)

        bot_text = gpt_service.get_gpt_message(user_level_name, all_chat)
        working_with_SQL.save_bot_message(DB_NAME, user_id, bot_text)

        bot.send_message(message.chat.id, bot_text)

        bot.register_next_step_handler(message, chat, returned_main_menu=returned_main_menu)
