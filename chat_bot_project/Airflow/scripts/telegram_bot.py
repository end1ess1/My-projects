import asyncio
import click
import functools
import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from rich.traceback import install

from connection import connect_to_databases

load_dotenv()
install(show_locals=True)
sys.path.append(os.getenv('LIBS_PATH'))
from chatting import get_model_answer
from log_lib import Log
from milvus_lib import MilvusDBClient
from private_file import API_TOKEN


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


@click.command()
@click.option("--model_version", default=os.getenv("MODEL_VERSION"), help="Имя пользователя")
@handle_errors
async def log_message(message: Message, answer: str, question_date: datetime, answer_date: datetime, model_version: str):
        __dicting__ = {
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
            'chat_id': message.chat.id,
            'question': message.text,
            'answer': answer,
            'question_date': question_date,
            'answer_date': answer_date,
            'language_code': message.from_user.language_code,
            'model_version': model_version,
            'log_table_name': os.getenv("LOG_TABLE_NAME")
        }
        
        logging.chat_history(__dicting__)
        logging.success("Inserting logs success")


@handle_errors
async def send_welcome(message: Message):
    logging.log('Приветствие бота')
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь с любыми вопросами!")


@handle_errors
async def handle_message(message: Message):

    question_date = datetime.now()
    answers = client.search_answer(message.text)
    #await message.answer(answers[0]['text'])
    await message.answer(f'''
                         \nРезультат #1:
                         \nТекст: {answers[0]['text']}
                         \nРаздел: {answers[0]['section']}
                         \nСтатья: {answers[0]['article']}
                         \nСхожесть: {1 - answers[0]['distance']:.2%}

                         \nРезультат #2:
                         \nТекст: {answers[1]['text']}
                         \nРаздел: {answers[1]['section']}
                         \nСтатья: {answers[1]['article']}
                         \nСхожесть: {1 - answers[1]['distance']:.2%}

                         \nРезультат #3:
                         \nТекст: {answers[2]['text']}
                         \nРаздел: {answers[2]['section']}
                         \nСтатья: {answers[2]['article']}
                         \nСхожесть: {1 - answers[2]['distance']:.2%}
                         ''')

    #message.answer(answers[0]['text'])
    answer_date = datetime.now()

    await log_message(message, answers[0]['text'], question_date, answer_date)


async def main(DP, BOT):
    @DP.message(Command("start"))
    async def on_start(message: Message):
        await send_welcome(message)

    @DP.message()
    async def on_message(message: Message):
        await handle_message(message)

    await DP.start_polling(BOT)


if __name__ == '__main__':

    logging = Log(*connect_to_databases(), script_name='test_postgre_sql.py')
    logging.success('Подключение к БД успешно!')
    
    client = MilvusDBClient(model_url=MODEL_URL, LibLog=logging)
    client.connect()
    client.create_collection()
    client.create_index()
    
    logging.log('Инициализация Бота')

    BOT = Bot(token=API_TOKEN)
    DP = Dispatcher()

    logging.success('Инициализация Бота успешна')

    asyncio.run(main(DP, BOT))
