import sqlite3 as sq
from bot_create import bot
import bot_text


def sql_db_start():
    global base, cur
    base = sq.connect('BaseQ.sqlite')
    cur = base.cursor()
    if base:
        print("SQL DB STARTED")
        base.execute("CREATE TABLE IF NOT EXISTS questions( question TEXT, answer TEXT, number INTEGER NOT NULL)")
        base.execute("CREATE TABLE IF NOT EXISTS admins( id TEXT)")
        base.commit()


# запись данных в таблицу вопросов
async def sql_add_question(data):
    cur.execute("INSERT INTO questions VALUES (?, ?, ?)", tuple(data.values()))
    base.commit()


# вывод данных их таблицы вопросов
async def sql_read_questions(message):
    for data in cur.execute("SELECT * FROM questions").fetchall():
        await bot.send_message(message.from_user.id, f"{data[2]}. {data[0]}")


async def sql_read_answer(message):
    text=message.text
    for data in cur.execute("SELECT * FROM questions WHERE number = ?", (text,)).fetchall():
        await bot.send_message(message.from_user.id, f"{data[1]}")


async def sql_add_admin(data):
    cur.execute("INSERT INTO admins VALUES (?)", (data,))
    base.commit()


async def is_admin():
    cur.execute("SELECT * FROM admins")

    return cur.fetchall()


async def count():
    cur.execute("SELECT COUNT(*) FROM questions")
    count = cur.fetchall()[0][0]
    print(count)
    return count


async def delete_question(message):
    text=message.text
    cur.execute("DELETE FROM questions WHERE number=?", (text,))
    await bot.send_message(message.from_user.id, bot_text.delete_question_completed)