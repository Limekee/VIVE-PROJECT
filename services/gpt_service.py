from openai import OpenAI
from config import key

client = OpenAI(
    api_key=key,
    base_url="https://api.proxyapi.ru/openai/v1"
)

def get_gpt_analysis(str_of_user_messages, user_level_name):
    """
    Запрашивает аналитику у chat-gpt

    Возвращает текст аналитики
    """
    prompt_for_gpt = (
        f"Твоя задача проанализировать предложения на наличие ошибок и вывести выявленные ошибки по пунктам,"
        f"Учитывая уровень пользователя: {user_level_name} "
        f"Анализ должен быть на русском, но цитируемые слова и предложения переводить на русский не нужно. "
        f"Проводи анализ даже если предложение состоит только из 1 слова. Если анализ состоит из 1 пункта, то его не нужно нумеровать. "
        f"Пунктуационные ошибки в анализ включать не нужно "
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=
        [
            {
                "role": "system",
                "content": prompt_for_gpt
            },
            {
                "role": "user",
                "content": str_of_user_messages
            },
        ]
        )

    bot_text = completion.choices[0].message.content
    return bot_text


def get_gpt_message(user_level_name, all_chat):
    """
    Отправляет chat-gpt запрос на получение сообщения, подходящего под контекст

    Возвращает текст сообщения
    """
    prompt_for_gpt = (f"You are human. "
                      f"You are the user's friend. "
                      f"Your task is to engage in a dialogue in English at the {user_level_name} level. "
                      f"You understand only English and must formulate your responses exclusively in English. "
                      f"Match the user's tone and style of communication. "
                      f"Avoid lecturing or instructing the user on how to behave. "
                      f"If something bothers you, express your opinion naturally, as a human would.")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=
        [
            {
                "role": "system",
                "content": prompt_for_gpt
            },

        ] + all_chat
    )

    bot_text = completion.choices[0].message.content
    return bot_text