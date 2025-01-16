from telebot import types
from config import bot, DB_NAME, theory_files_dir
from services import working_with_SQL
from utils import main_function


def register_theory_handler():
    @bot.callback_query_handler(func=lambda callback: 'theory' in callback.data)
    def callback_theory(callback):
        """
        Обрабатывает выбор темы у пользователя

        Получает данные из БД по данной теме

        Изменяет сообщение с темами на описание конкретной темы
        Отправляет файл с теорией
        """
        theory_id = int(callback.data[6:])
        theory = working_with_SQL.get_theory_by_id(DB_NAME, theory_id)
        description = theory[3]
        url = theory[-2]
        text = (f"{description}\n"
                f"\n"
                f"{url}")
        file = theory[-1]
        file_path = theory_files_dir / file

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_practice = types.KeyboardButton('Практика')
        button_main_menu = types.KeyboardButton("Главное меню")
        markup.add(button_practice)
        markup.add(button_main_menu)

        bot.edit_message_text(text, callback.message.chat.id, callback.message.message_id, reply_markup=None)
        bot.send_document(callback.message.chat.id, types.InputFile(file_path), reply_markup=markup)

        bot.register_next_step_handler(callback.message, separation_in_practice, theory_id=theory_id)


def register_explanation_handler():
    @bot.callback_query_handler(func=lambda callback: 'explanation' in callback.data)
    def callback_explanation(callback):
        LENGTH_OF_EXPLANATION = len('explanation')
        practice_id = callback.data[LENGTH_OF_EXPLANATION:]

        practice = working_with_SQL.get_practice_by_practice_id(DB_NAME, practice_id)
        explanation = practice[-2]
        answer = practice[2]

        text = (f"Вы ответили неверно\n"
                f"Правильный ответ: *{answer}*\n"
                f"----------------------------------\n"
                f"*Обьяснение*\n"
                f"{explanation}")
        bot.edit_message_text(text, callback.message.chat.id, callback.message.message_id, parse_mode='Markdown')

def separation_in_practice(message, theory_id):
    if message.text.lower() == "главное меню":
        main_function.main_menu_markup(message)

    elif message.text.lower() == 'практика':
        all_test = working_with_SQL.get_practice_by_theory_id(DB_NAME, theory_id)
        all_test = iter(all_test)
        test(message, all_test)


def test(message, all_test):
    try:
        test_info = next(all_test)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_a = types.KeyboardButton('a')
        button_b = types.KeyboardButton('b')
        button_c = types.KeyboardButton('c')
        button_d = types.KeyboardButton('d')
        button_main_menu = types.KeyboardButton('Главное меню')
        markup.row(button_a, button_b)
        markup.row(button_c, button_d)
        markup.add(button_main_menu)

        test = test_info[1].split("%")
        text = '\n'.join(test)

        bot.send_message(message.chat.id, text, reply_markup=markup)
        practice_id = test_info[0]
        answer = test_info[2]
        bot.register_next_step_handler(message, answer_processing, all_test=all_test, answer=answer, practice_id=practice_id)
    except StopIteration:
        text = "Тест по данной теме окончен! Можешь переходить к следующей!"
        bot.send_message(message.chat.id, text)
        main_function.main_menu_markup(message)


def answer_processing(message, all_test, answer, practice_id):
    if message.text.lower() == answer:
        text = "Вы выбрали правильный ответ"
        bot.send_message(message.chat.id, text)

        test(message, all_test)

    elif message.text.lower() == "главное меню":
        main_function.main_menu_markup(message)

    else:
        markup = types.InlineKeyboardMarkup()
        button_explanation = types.InlineKeyboardButton('Объяснение', callback_data=f'explanation{practice_id}')
        markup.add(button_explanation)

        text = (f"Вы ответили неверно\n"
                f"Правильный ответ: *{answer}*")
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

        test(message, all_test)