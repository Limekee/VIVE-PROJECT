import telebot
from pathlib import Path

key = "sk-KVD8VYoze5Ivy8BFwfV9KnCzdMvhnnyp"

DB_NAME = 'database.db'
current_path = Path.cwd()
theory_files_dir = current_path / 'datafiles' / 'theory_files'

token = '8095942189:AAFx6uZ5Gi-UF6IRChlfnYv9JIF4r9Lf0T8'
# Обьект для взаимодействия с TelegramAPI
bot = telebot.TeleBot(token)