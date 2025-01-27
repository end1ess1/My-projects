import traceback
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
import asyncio

from private_file import API_TOKEN
from chatting import get_model_answer
from connection import connect_to_databases
from lib import Log
from rich.traceback import install

install(show_locals=True)

import functools
import traceback

# Обработка исключений
def handle_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            logging.error(f"Error in {func.__name__}: {e}")
            traceback.print_exc()
    return wrapper


MODEL_VERSION = 'model'
LOG_TABLE_NAME = 'llm_logs'

POSTGRES_CONN, REDIS_CONN = connect_to_databases()

logging = Log(postgresql_conn=POSTGRES_CONN,
              redis_conn=REDIS_CONN,
              script_name='test_postgre_sql.py')

logging.log('Инициализация Бота')

BOT = Bot(token=API_TOKEN)
DP = Dispatcher()

@handle_errors
async def log_message(message: Message, answer: str, question_date: datetime, answer_date: datetime):
        logging.insert_llm_log(
            user_id=message.from_user.user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            chat_id=message.chat.id,
            question=message.text,
            answer=answer,
            question_date=question_date,
            answer_date=answer_date,
            language_code=message.from_user.language_code,
            model_version=MODEL_VERSION,
            log_table_name=LOG_TABLE_NAME
        )

        logging.success("Inserting logs success")

@DP.message(Command("start"))
@handle_errors
async def send_welcome(message: Message):
    logging.log('Приветствие бота')
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь с любыми вопросами!")


@DP.message()
@handle_errors
async def handle_message(message: Message):

    question_date = datetime.now()
    answer = get_model_answer(message.text)
    await message.answer(answer)
    answer_date = datetime.now()

    await log_message(message, answer, question_date, answer_date)

@handle_errors
async def main():
    await DP.start_polling(BOT)

if __name__ == '__main__':
    asyncio.run(main())
