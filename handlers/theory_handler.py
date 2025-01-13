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
        markup.row(button_a, button_b)
        markup.row(button_c, button_d)

        test = test_info[1].split("%")
        text = '\n'.join(test)

        bot.send_message(message.chat.id, text, reply_markup=markup)
        answer = test_info[2]
        bot.register_next_step_handler(message, answer_processing, all_test=all_test, answer=answer)
    except StopIteration:
        text = "Тест по данной теме окончен! Можешь переходить к следующей!"
        bot.send_message(message.chat.id, text)
        main_function.main_menu_markup(message)


def answer_processing(message, all_test, answer):
    if message.text.lower() == answer:
        text = "Вы выбрали правильный ответ"
        bot.send_message(message.chat.id, text)

        test(message, all_test)

    else:
        text = (f"Вы ответили неверно\n"
                f"Правильный ответ: {answer}")
        bot.send_message(message.chat.id, text)

        test(message, all_test)