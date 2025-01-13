from services import working_with_SQL
from config import bot, DB_NAME
from utils import main_function


def register_level_selection_handler():
    @bot.callback_query_handler(func=lambda callback: 'level' in callback.data)
    def callback_level_selection(callback):
        """
        Обрабатывает выбор уровня языка пользователя

        Регистрирует пользователя в БД

        Возвращает пользователя в главное меню
        """
        callback.data = callback.data[-1]
        user_id = callback.from_user.id
        user_level_id = int(callback.data)

        bot.delete_message(callback.message.chat.id, callback.message.message_id)

        working_with_SQL.write_or_replace_level_id(DB_NAME, user_id, user_level_id)

        main_function.main_menu_markup(callback.message)