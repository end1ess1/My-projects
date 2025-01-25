import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from private_file import API
from chatting import get_model_answer
from rich.traceback import install

install(show_locals=True)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = API

# Инициализируем бота и диспетчер
BOT = Bot(token=API_TOKEN)
DP = Dispatcher()

# Маршруты сайта
routes = {
    'schedule': '/schedule',
    'contacts': '/contacts',
    'library': '/library',
}

# Обработчик команды /start
@DP.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь найти расписание, контакты или доступ к библиотеке. Задавай вопрос!")

# Обработчик пользовательских сообщений
@DP.message()
async def handle_message(message: Message):
    text = message.text.lower()

    if "расписание" in text:
        await message.answer(f"Расписание можно найти здесь: {routes['schedule']}")
    elif "контакты" in text:
        await message.answer(f"Контакты можно найти здесь: {routes['contacts']}")
    elif "библиотека" in text:
        await message.answer(f"Доступ к библиотеке здесь: {routes['library']}")
    else:
        await message.answer(get_model_answer(text))

# Запуск polling
async def main():
    await DP.start_polling(BOT)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
