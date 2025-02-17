import asyncio
import functools
import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from rich.traceback import install

from connection import connect_to_databases

load_dotenv()
install(show_locals=True)
sys.path.append(os.getenv('LIBS_PATH'))
from log_lib import Log, ChatHistory
from milvus_lib import MilvusDBClient
from model_lib import Model


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
            'model_version': os.getenv("MODEL_VERSION"),
            'log_table_name': os.getenv("LOG_TABLE_NAME")
        }

        ChatHistory.load_logs(__dicting__)
        logging.success("Inserting logs success")


@handle_errors
async def send_welcome(message: Message):
    logging.log('Приветствие бота')
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь с любыми вопросами!")


@handle_errors
async def handle_message(message: Message):
    question_date = datetime.now()

    answers = client.search_answer(message.text)
    logging.log("Получили похожие тексты из БД")
    
    final_answer = Model().get_answer(message.text, answers[0]['text'])
    logging.success("Модель ответила на основе них")

    await message.answer(final_answer)

    # Для вывода в консоль
    pprint(f'''
                Результат #1:
                Текст: {answers[0]['text']}
                Раздел: {answers[0]['section']}
                Статья: {answers[0]['article']}
                Схожесть: {1 - answers[0]['distance']:.2%}

                Результат #2:
                Текст: {answers[1]['text']}
                Раздел: {answers[1]['section']}
                Статья: {answers[1]['article']}
                Схожесть: {1 - answers[1]['distance']:.2%}

                Результат #3:
                Текст: {answers[2]['text']}
                Раздел: {answers[2]['section']}
                Статья: {answers[2]['article']}
                Схожесть: {1 - answers[2]['distance']:.2%}
                
                ----
                
                Ответ: {final_answer}
                ''')
    
    answer_date = datetime.now()
    
    await log_message(message, final_answer, question_date, answer_date)


async def main(DP, BOT):
    @DP.message(Command("start"))
    async def on_start(message: Message):
        await send_welcome(message)

    @DP.message()
    async def on_message(message: Message):
        await handle_message(message)

    await DP.start_polling(BOT)


if __name__ == '__main__':

    SCRIPT_NAME = 'test_postgre_sql.py'

    logging = Log(*connect_to_databases(), SCRIPT_NAME)
    ChatHistory = ChatHistory(*connect_to_databases(), SCRIPT_NAME)
    logging.success('Подключение к БД успешно!')

    client = MilvusDBClient(LibLog=logging)
    client.connect()
    client.create_collection(name='test', dimension=3072)
    client.create_index()

    logging.log('Инициализация Бота')

    BOT = Bot(token=os.getenv('API_TOKEN'))
    DP = Dispatcher()

    logging.success('Инициализация Бота успешна')

    asyncio.run(main(DP, BOT))
