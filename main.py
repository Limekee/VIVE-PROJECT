from handlers import register_handlers
from config import bot, DB_NAME
from services import working_with_SQL

if __name__ == "__main__":
    working_with_SQL.initialization_db(DB_NAME)
    working_with_SQL.fill_db(DB_NAME)
    register_handlers()
    bot.polling(none_stop=True)