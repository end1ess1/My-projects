import asyncio
import functools
import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from rich.traceback import install
from pymilvus.model.reranker import CrossEncoderRerankFunction

from connection import connect_to_databases

load_dotenv()
install(show_locals=True)
sys.path.append(os.getenv("LIBS_PATH"))
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
async def log_message(
    message: Message, answer: str, question_date: datetime, answer_date: datetime
):
    __dicting__ = {
        "user_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username,
        "chat_id": message.chat.id,
        "question": message.text,
        "answer": answer,
        "question_date": question_date,
        "answer_date": answer_date,
        "language_code": message.from_user.language_code,
        "model_version": os.getenv("MODEL_VERSION"),
        "log_table_name": os.getenv("LOG_TABLE_NAME"),
    }

    ChatHistory.load_logs(__dicting__)
    logging.success("Inserting logs success")


@handle_errors
async def send_welcome(message: Message):
    logging.log("Приветствие бота")
    await message.answer(
        "Привет! Я бот-помощник Гисик. Могу помочь с любыми вопросами!"
    )


@handle_errors
async def handle_message(message: Message):
    print(f"Вопрос пользователя: {message.text}")  # Для отображения в логах
    question_date = datetime.now()
    answers = client.search_answer(question=message.text, reranker=reranker)
    # answers = client.search_answer(question=message.text)
    logging.log("Получили похожие тексты из БД")

    if answers:
        final_answer = Model().get_answer(
            message.text,
            "\n".join(answer["text"] for answer in answers[:3] if answer.get("text")),
        )
    else:
        final_answer = "Данные по вашему вопросу, к сожалению, не найдены.\nПопробуйте переформулировать вопрос или задать другой."

    logging.success("Модель ответила на вопрос пользователя")

    await message.answer(final_answer)

    # keyboard = InlineKeyboardMarkup().add(
    #     InlineKeyboardButton("Да", callback_data="feedback_yes"),
    #     InlineKeyboardButton("Нет", callback_data="feedback_no"),
    # )
    # await message.answer(final_answer, reply_markup=keyboard)

    result = []
    for i, answer in enumerate(answers[:3], start=1):
        result.append(
            f"""
            Результат #{i}:
            Текст: {answer.get('text', 'Нет данных')}
            Раздел: {answer.get('section', 'Нет данных')}
            Статья: {answer.get('article', 'Нет данных')}
            Схожесть: {1 - answer.get('distance', 1):.2%}
            """
        )

    result.append(f"----\n\nОтвет: {final_answer}")

    pprint("".join(result))

    answer_date = datetime.now()

    await log_message(message, final_answer, question_date, answer_date)


# @DP.callback_query_handler(lambda c: c.data.startswith("feedback_"))
# async def handle_feedback(callback_query: types.CallbackQuery):
#     feedback = (
#         "Спасибо за ваш отзыв!"
#         if callback_query.data == "feedback_yes"
#         else "Жаль, что ответ не помог. Мы улучшимся!"
#     )
#     await BOT.answer_callback_query(callback_query.id, feedback)


async def main(DP, BOT):
    @DP.message(Command("start"))
    async def on_start(message: Message):
        await send_welcome(message)

    @DP.message()
    async def on_message(message: Message):
        await handle_message(message)

    await DP.start_polling(BOT)


if __name__ == "__main__":
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

    SCRIPT_NAME = "telegram_bot.py"

    logging = Log(*connect_to_databases(), SCRIPT_NAME)
    ChatHistory = ChatHistory(*connect_to_databases(), SCRIPT_NAME)
    logging.success("Подключение к БД успешно!")

    client = MilvusDBClient(LibLog=logging)
    client.connect()
    client.create_collection(name="MiigaikDocsInfo", dimension=3072)
    client.create_index()

    reranker = CrossEncoderRerankFunction(
        model_name=os.getenv("RERANKER_MODEL"),
        device="cpu",
    )

    logging.log("Инициализация Бота")

    BOT = Bot(token=os.getenv("API_TOKEN"))
    DP = Dispatcher()

    logging.success("Инициализация Бота успешна")

    asyncio.run(main(DP, BOT))
