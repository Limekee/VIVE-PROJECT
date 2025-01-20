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
        f"Your task is to analyze sentences for errors and list the identified errors point by point. "
        f"The analysis should be in Russian, considering that the user's language proficiency level is {user_level_name}, but quoted words and sentences should not be translated into Russian. "
        f"Perform the analysis even if the sentence consists of only one word. If the analysis contains only one error, do not number it as a point. Do not include punctuation errors in the analysis. "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
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
    prompt_for_gpt = (f"You are an Englishman who is having a dialogue with your friend at the {user_level_name} level. "
                      f"You don't understand languages other than English.")

    completion = client.chat.completions.create(
        model="gpt-4o",
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