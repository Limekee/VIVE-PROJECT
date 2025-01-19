import sqlite3


import sqlite3
import enum


class Levels(enum.Enum):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4
    C1 = 5


def initialization_db(name):
    with sqlite3.connect(name) as connection:
        cursor = connection.cursor()

        # Создание таблицы users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            level_id INTEGER,
            FOREIGN KEY (level_id) REFERENCES levels(id)
        )
        ''')

        # Создание таблицы chat
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            role TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')

        # Создание таблицы levels
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')

        # Создание таблицы theory
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS theory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_id INTEGER NOT NULL,
            topic_name TEXT NOT NULL,
            description TEXT,
            url TEXT,
            file TEXT,
            FOREIGN KEY (level_id) REFERENCES levels (id)
        )
        ''')

        # Создание таблицы vocabulary
        # cursor.execute('''
        # CREATE TABLE IF NOT EXISTS `vocabulary` (
        #     `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        #     `level_id` INTEGER NOT NULL,
        #     `english_word` TEXT NOT NULL,
        #     `russian_word` TEXT NOT NULL,
        #     `is_the_word_known` BOOL DEFAULT False,
        #     FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`)
        # )
        # ''')

        # Создание таблицы practice
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            answer TEXT,
            explanation TEXT,
            theory_id INTEGER,
            FOREIGN KEY (theory_id) REFERENCES theory(id)
        )
        ''')


def prepare_file_for_db(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    rows = content.split('\n')
    list_strings = [tuple(row.split(';')) for row in rows]
    return list_strings


# def words_filling(level, level_file):
#     with open(level_file, 'r', encoding='utf-8') as file:
#         data = []
#         for set_of_words in file:
#             for j in set_of_words:
#                 if j != ' ' and (not j.isalpha()):
#                     i = i.replace(j, '', 1)
#             word = i.split()
#             data.append((level.value, word[0], word[1]))
#         return data


def prepare_file_for_vocabulary(level, level_file):
    with open(level_file, 'r', encoding='utf-8') as file:
        list_of_all_words = []
        for line in file:
            line = line.strip().split(' - ')
            russian = line[0].split()[1]
            english = line[1]
            tuple_of_words = (level.value, russian, english)
            list_of_all_words.append(tuple_of_words)
        return list_of_all_words


def fill_db(name):
    with sqlite3.connect(name) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM levels')
        if cursor.fetchone()[0] == 0:
            # Заполнение таблицы levels
            cursor.executemany('''
            INSERT INTO levels (name) 
            VALUES (?)
            ''', [('A1',), ('A2',), ('B1',), ('B2',), ('C1',)])

        # Заполнение таблицы theory
        cursor.execute('SELECT COUNT(*) FROM theory')
        if cursor.fetchone()[0] == 0:
            theory_path = './text_files/theory.txt'
            list_strings = prepare_file_for_db(theory_path)
            formatted_rows = [(int(row[0]), *row[1:]) for row in list_strings]

            cursor.executemany('''
            INSERT INTO theory (level_id, topic_name, description, url, file)
            VALUES (?, ?, ?, ?, ?)
            ''', formatted_rows)

        # Заполнение таблицы practice
        cursor.execute('SELECT COUNT(*) FROM practice')
        if cursor.fetchone()[0] == 0:
            practice_path = './text_files/practice.txt'
            list_strings = prepare_file_for_db(practice_path)
            formatted_rows = [(*row[:-1], int(row[-1])) for row in list_strings]
            cursor.executemany('''
            INSERT INTO practice (task, answer, explanation, theory_id)
            VALUES (?, ?, ?, ?)
            ''', formatted_rows)

        connection.commit()


def initialization_chat(name, user_id):
    """Создает таблицу чата по айди пользователя"""
    with sqlite3.connect(name) as connection:
        cursor = connection.cursor()
        table_name = f"chat_{user_id}"
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            role TEXT
        )
        """)


def initialization_vocabulary(name, user_id):
    """Создает таблицу со словарём по айди пользователя"""
    with sqlite3.connect(name) as connection:
        cursor = connection.cursor()
        table_name = f"vocabulary_{user_id}"
        # Создание таблицы vocabulary
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id` INTEGER NOT NULL,
            `level_id` INTEGER NOT NULL,
            `english_word` TEXT NOT NULL,
            `russian_word` TEXT NOT NULL,
            `is_the_word_known` BOOL DEFAULT False,
            FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`),
            FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
        )
        """)


def filling_vocabulary(name, user_id):
    # Заполнение таблицы vocabulary
    with sqlite3.connect(name) as db:
        table_name = f"vocabulary_{user_id}"
        cursor = db.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        if not cursor.fetchone()[0]:
            vocabulary = [*prepare_file_for_vocabulary(Levels.A1, 'a1_words'),
                          *prepare_file_for_vocabulary(Levels.A2, 'a2_words'),
                          *prepare_file_for_vocabulary(Levels.B1, 'b1_words'),
                          *prepare_file_for_vocabulary(Levels.B2, 'b2_words'),
                          *prepare_file_for_vocabulary(Levels.C1, 'c1_words')]
            # Данные для vocabulary
            cursor.executemany(f"""
                    INSERT INTO {table_name} (`user_id`, `level_id`, `english_word`, `russian_word`, `is_the_word_known`)
                    VALUES ({user_id}, ?, ?, ?, False)
                    """, vocabulary)


def write_or_replace_level_id(name, user_id, level_id):
    """Записывает или изменяет уровень языка пользователя"""
    with sqlite3.connect(name) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT OR REPLACE 
        INTO users (user_id, level_id) 
        VALUES (?, ?)
        """,(user_id, level_id))
        connection.commit()


def get_level_id(name, user_id):
    """Получает по айди пользователя его айди уровня владения языком и возвращает его"""

    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT level_id 
        FROM users 
        WHERE user_id = ?
        """, (user_id,))
        user_level_id = cursor.fetchone()[0]
        return user_level_id


def get_level_name(name, level_id):
    """
    Получает по айди(1,2,...) уровня владения языка название данного уровня (A1,A2,...)

    Возвращает название данного уровня
    """
    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT name
        FROM levels 
        WHERE id == ?
        """, (level_id,))
        level_name = cursor.fetchone()[0]
        return level_name


def get_all_theory(name, level_id):
    """Получает всю теорию по айди уровня владения языком и возвращает ее"""
    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT * 
        FROM theory
        WHERE level_id == ?
        """, (level_id,))
        all_theory = cursor.fetchall()
        return all_theory


def get_theory_by_id(name, theory_id):
    """Получает ОДНУ полную информацию о конретной теории по айди данной теории и возвращает ее"""
    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT * 
        FROM theory
        WHERE id == ?
        """, (theory_id,))
        theory = cursor.fetchone()
        return theory


def get_practice_by_theory_id(name, theory_id):
    """
    Получает все практические задания по указанному айди теории

    Возвращает писок всех практических заданий для данной теории
    """
    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT *
        FROM practice
        WHERE theory_id == ?
        """, (theory_id,))
        practice = cursor.fetchall()
        return practice


def get_practice_by_practice_id(name, practice_id):
    with sqlite3.connect(name) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT *
        FROM practice
        WHERE id == ?
        """, (practice_id,))
        practice = cursor.fetchone()
        return practice


def save_user_message(name, user_id, user_text):
    """Сохраняет сообщение пользователя в таблицу чата"""
    with sqlite3.connect(name) as db:
        table_name = f"chat_{user_id}"
        cursor = db.cursor()
        cursor.execute(f'''
        INSERT 
        INTO {table_name} (text, role) 
        VALUES (?, 'user')
        ''', (user_text,))
        db.commit()


def save_bot_message(name, user_id, bot_text):
    """Сохраняет сообщение бота в таблицу чата"""
    with sqlite3.connect(name) as db:
        table_name = f"chat_{user_id}"
        cursor = db.cursor()
        cursor.execute(f'''
        INSERT 
        INTO {table_name} (text, role) 
        VALUES (?, 'assistant')
        ''', (bot_text,))
        db.commit()


def get_all_chat(name, user_id):
    """
    Получает полный список сообщений из чата пользователя

    Возвращает список всех сообщений с ролями ('user', 'assistant')
    """
    with sqlite3.connect(name) as db:
        table_name = f"chat_{user_id}"
        cursor = db.cursor()
        cursor.execute(f'''
        SELECT * FROM {table_name}
        ''')
        # Не оптимизировано
        all_chat = [{'role': i[2], 'content': i[1]} for i in cursor.fetchall()]
        return all_chat


def get_all_user_messages(name, user_id):
    """
    Получает все сообщения пользователя из чата

    Возвращает строку со всеми сообщениями пользователя
    """
    with sqlite3.connect(name) as db:
        table_name = f"chat_{user_id}"
        cursor = db.cursor()
        cursor.execute(f'''
        SELECT text 
        FROM {table_name} 
        WHERE role='user' ''')
        list_of_user_messages = cursor.fetchall()
        str_of_user_messages = '. '.join(list(map(lambda x: x[0], list_of_user_messages)))
        return str_of_user_messages


def clear_table(name, user_id):
    """Удаляет все данные из таблицы чата для указанного пользователя"""
    with sqlite3.connect(name) as db:
        table_name = f"chat_{user_id}"
        cursor = db.cursor()
        cursor.execute(f"""
        DELETE FROM {table_name}
        """)
        db.commit()


def get_list_of_unknown_words(name, level_id, user_id):
    """
    Получает список незнакомых слов для указанного уровня языка,
    возвращает список незнакомых слов с их данными
    """
    with sqlite3.connect(name) as connect:
        table_name = f"vocabulary_{user_id}"
        cursor = connect.cursor()
        cursor.execute(f"""
            SELECT `english_word`, `russian_word`
            FROM {table_name}
            WHERE `level_id` = ? AND `is_the_word_known` = ? 
            """, (level_id, False))
        rows = cursor.fetchall()
        list_of_words = [list(row) for row in rows]
        return list_of_words


def update_word_status(name, russian_word, user_id):
    """Обновляет статус слова в словаре, помечая его как знакомое"""
    with sqlite3.connect(name) as connection:
        table_name = f"vocabulary_{user_id}"
        cursor = connection.cursor()
        cursor.execute(f"""
                UPDATE {table_name}
                SET `is_the_word_known` = ?
                WHERE `russian_word` = ?
                """, (True, russian_word,))
        connection.commit()