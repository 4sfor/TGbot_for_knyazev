import asyncio

import logging
import sys
from bot_create import dp, bot
from handlers import hand
from data_base import sql_db


# функция для запуска бота, при удачном запуске в консоль выводится сообщение, что бот работает
async def main():
    print("Бот работает")
    sql_db.sql_db_start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
