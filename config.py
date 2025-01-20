import telebot
from pathlib import Path

key = "sk-KVD8VYoze5Ivy8BFwfV9KnCzdMvhnnyp"

DB_NAME = 'database.db'
current_path = Path.cwd()
theory_files_dir = current_path / 'datafiles' / 'theory_files'

token = '7827928589:AAG1DfVLUTr7b99smaUCPF6hrO_3ASXN6ck'
# Обьект для взаимодействия с TelegramAPI
bot = telebot.TeleBot(token)