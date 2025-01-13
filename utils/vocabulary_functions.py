import random
from telebot import types
from services import working_with_SQL
from config import bot, DB_NAME


def vocabulary_output(message, returned_main_menu):
    """Отправляет сообщение с английским словом пользовалтелю, добавляет разметку"""
    user_id = message.from_user.id
    user_level_id = working_with_SQL.get_level_id(DB_NAME, user_id)
    vocabulary = working_with_SQL.get_list_of_unknown_words(DB_NAME, user_level_id)
    sample = random.sample(vocabulary, 3)
    task_word_set = random.choice(sample)
    right_answer = task_word_set[3]

    answers = [i[3] for i in sample]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_a = types.KeyboardButton(answers[0])
    button_b = types.KeyboardButton(answers[1])
    button_c = types.KeyboardButton(answers[2])
    button_main_menu = types.KeyboardButton("Главная страница")
    markup.row(button_a, button_b, button_c)
    markup.row(button_main_menu)

    question_text = f"Выбери правильный перевод\n{task_word_set[2]}"
    bot.send_message(message.chat.id, question_text, reply_markup=markup)

    bot.register_next_step_handler(message, vocabulary_answer_processing, answer=right_answer, returned_main_menu=returned_main_menu)


def vocabulary_answer_processing(message, answer, returned_main_menu):
    if message.text.lower() == answer.lower():
        bot_text = "Вы выбрали правильный ответ"
        bot.send_message(message.chat.id, bot_text)
        working_with_SQL.update_word_status(DB_NAME, answer)

        vocabulary_output(message, returned_main_menu)

    elif message.text.lower() == "главная страница":
        returned_main_menu(message)

    else:
        bot_reply = (f"Вы ответили неверно\n"
                f"Правильный ответ: {answer}")
        bot.send_message(message.chat.id, bot_reply)

        vocabulary_output(message, returned_main_menu)
