import os
import soundfile as sf
import speech_recognition as sr
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

    bot.register_next_step_handler(message, detect_content_type, returned_main_menu=returned_main_menu)


def detect_content_type(message, returned_main_menu):
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем файл временно
        ogg_filename = "voice.ogg"
        with open(ogg_filename, "wb") as f:
            f.write(downloaded_file)

        # Конвертация в WAV
        wav_filename = "voice.wav"
        data, samplerate = sf.read(ogg_filename)
        sf.write(wav_filename, data, samplerate)

        # Распознавание речи
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            audio = recognizer.record(source)

        try:
            # Используем Google Web Speech API для распознавания
            text = recognizer.recognize_google(audio, language='en-EN')  # Замените на нужный язык

            chat(message, returned_main_menu, text)
        except sr.UnknownValueError:
            bot.reply_to(message, 'Не удалось распознать аудио.')
        except sr.RequestError as e:
            bot.reply_to(message, f'Ошибка сервиса распознавания: {e}')

        # Удаляем временные файлы
        os.remove(ogg_filename)
        os.remove(wav_filename)

    elif message.content_type == 'text':
        text = message.text

        chat(message, returned_main_menu, text)

    else:
        bot.send_message(message.chat.id, 'Неккоректный ввод')


def chat(message, returned_main_menu, text):
    # Данный блок "if" отправляет пользователю аналитику по чату
    if text.lower() == 'аналитика':
        user_id = message.from_user.id
        user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
        user_level_name = working_with_SQL.get_level_name(DB_NAME,
                                                          user_level_id)
        str_of_user_messages = working_with_SQL.get_all_user_messages(DB_NAME,
                                                                      user_id)

        if str_of_user_messages:
            bot_text = gpt_service.get_gpt_analysis(str_of_user_messages, user_level_name)
            bot.send_message(message.chat.id, bot_text)

            working_with_SQL.clear_table(DB_NAME, user_id)

            returned_main_menu(message)

        else:
            bot.send_message(message.chat.id,'Диалог только начался! Нечего анализировать')

            returned_main_menu(message)


    #Блок 'else' отправляет сообщения chat-gpt в роли собеседника
    else:
        markup = types.InlineKeyboardMarkup()
        button_translate = types.InlineKeyboardButton('Перевод', callback_data='translate')
        markup.add(button_translate)

        user_id = message.from_user.id
        user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
        user_level_name = working_with_SQL.get_level_name(DB_NAME, user_level_id)

        user_text = text
        working_with_SQL.save_user_message(DB_NAME, user_id, user_text)
        all_chat = working_with_SQL.get_all_chat(DB_NAME, user_id)

        bot_text = gpt_service.get_gpt_message(user_level_name, all_chat)
        working_with_SQL.save_bot_message(DB_NAME, user_id, bot_text)

        bot.send_message(message.chat.id, bot_text, reply_markup=markup)

        bot.register_next_step_handler(message, detect_content_type, returned_main_menu=returned_main_menu)
