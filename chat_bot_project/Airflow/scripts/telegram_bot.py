import traceback
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
import asyncio
import functools

from private_file import API_TOKEN
from chatting import get_model_answer
from connection import connect_to_databases
from lib import Log
from rich.traceback import install
from dotenv import load_dotenv
import os


# Обработка исключений и логирование в БДшки
def handle_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            traceback.print_exc()
    return wrapper


@handle_errors
async def log_message(message: Message, answer: str, question_date: datetime, answer_date: datetime):
        logging.insert_llm_log(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            chat_id=message.chat.id,
            question=message.text,
            answer=answer,
            question_date=question_date,
            answer_date=answer_date,
            language_code=message.from_user.language_code,
            model_version=os.getenv("MODEL_VERSION"),
            log_table_name=os.getenv("LOG_TABLE_NAME")
        )

        logging.success("Inserting logs success")


@handle_errors
async def send_welcome(message: Message):
    logging.log('Приветствие бота')
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь с любыми вопросами!")


@handle_errors
async def handle_message(message: Message):

    question_date = datetime.now()
    answer = get_model_answer(message.text)
    await message.answer(answer)
    answer_date = datetime.now()

    await log_message(message, answer, question_date, answer_date)


async def main(DP, BOT):
    @DP.message(Command("start"))
    async def on_start(message: Message):
        await send_welcome(message)

    @DP.message()
    async def on_message(message: Message):
        await handle_message(message)

    await DP.start_polling(BOT)


if __name__ == '__main__':
    
    load_dotenv()
    install(show_locals=True)

    logging = Log(*connect_to_databases(), script_name='test_postgre_sql.py')
    logging.success('Подключение к БД успешно!')

    logging.log('Инициализация Бота')

    BOT = Bot(token=API_TOKEN)
    DP = Dispatcher()

    logging.success('Инициализация Бота успешна')

    asyncio.run(main(DP, BOT))
