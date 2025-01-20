from config import bot
from translate import Translator


def register_translate_handler():
    @bot.callback_query_handler(func=lambda callback: callback.data == 'translate')
    def callback_translate(callback):
        gpt_message = callback.message.text
        translator = Translator(from_lang='en', to_lang='ru')
        translated_last_gpt_message = translator.translate(gpt_message)

        changed_text = f'{gpt_message}\n' + '-' * 20 + '\n' + translated_last_gpt_message

        bot.edit_message_text(changed_text, callback.message.chat.id, callback.message.message_id, reply_markup=None)
