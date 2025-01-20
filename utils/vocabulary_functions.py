import random
from telebot import types
from services import working_with_SQL
from config import bot, DB_NAME


def selecting_mode(message, returned_main_menu):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Eng-Рус')
    button_2 = types.KeyboardButton('Рус-Eng')
    markup.add(button_1, button_2)
    bot.send_message(message.chat.id, "Выбери один из 2 режимов:", reply_markup=markup)
    bot.register_next_step_handler(message, processing_mode, returned_main_menu=returned_main_menu)


def processing_mode(message, returned_main_menu):
    mode = None

    if message.text == 'Eng-Рус':
        mode = 'Eng-Рус'
    elif message.text == 'Рус-Eng':
        mode = 'Рус-Eng'

    vocabulary_output(message, mode, returned_main_menu)


def vocabulary_output(message, mode, returned_main_menu):
    """Отправляет сообщение с английским словом пользователю, добавляет разметку"""
    answers = []
    right_answer = ''
    user_id = message.from_user.id
    working_with_SQL.initialization_vocabulary(DB_NAME, user_id)
    working_with_SQL.filling_vocabulary(DB_NAME, user_id)
    user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
    vocabulary = working_with_SQL.get_list_of_unknown_words(DB_NAME, user_level_id, user_id)
    sample = random.sample(vocabulary, 3)
    task_word_set = random.choice(sample)
    original_word = None
    if mode == 'Eng-Рус':
        right_answer = task_word_set[1]
        original_word = task_word_set[0]
        answers = [i[1] for i in sample]
    elif mode == 'Рус-Eng':
        right_answer = task_word_set[0]
        original_word = task_word_set[1]
        answers = [i[0] for i in sample]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_a = types.KeyboardButton(answers[0])
    button_b = types.KeyboardButton(answers[1])
    button_c = types.KeyboardButton(answers[2])
    button_main_menu = types.KeyboardButton("Главная страница")
    markup.row(button_a, button_b, button_c)
    markup.row(button_main_menu)

    question_text = f"Выбери правильный перевод\n{original_word}"
    bot.send_message(message.chat.id, question_text, reply_markup=markup)

    bot.register_next_step_handler(message, vocabulary_answer_processing, mode=mode, answer=right_answer, returned_main_menu=returned_main_menu)


def vocabulary_answer_processing(message, answer, mode, returned_main_menu):
    user_id = message.from_user.id
    if message.text.lower() == answer.lower():
        bot_text = "Вы выбрали правильный ответ"
        bot.send_message(message.chat.id, bot_text)
        working_with_SQL.update_word_status(DB_NAME, answer, user_id)
        vocabulary_output(message, mode, returned_main_menu)

    elif message.text.lower() == "главная страница":
        returned_main_menu(message)

    else:
        bot_reply = (f"Вы ответили неверно\n"
                f"Правильный ответ: {answer}")
        bot.send_message(message.chat.id, bot_reply)

        vocabulary_output(message, mode, returned_main_menu)
