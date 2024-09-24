import logging
import torch
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from data import word2idx, max_len, idx2word
from private_file import API
from funcs import generate_response
from my_model import model

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = API

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Маршруты сайта
routes = {
    'schedule': '/schedule',
    'contacts': '/contacts',
    'library': '/library',
}

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот-помощник Гисик. Могу помочь найти расписание, контакты или доступ к библиотеке. Задавай вопрос!")

# Обработчик пользовательских сообщений
@dp.message()
async def handle_message(message: Message):
    text = message.text.lower()

    if "расписание" in text:
        await message.answer(f"Расписание можно найти здесь: {routes['schedule']}")
    elif "контакты" in text:
        await message.answer(f"Контакты можно найти здесь: {routes['contacts']}")
    elif "библиотека" in text:
        await message.answer(f"Доступ к библиотеке здесь: {routes['library']}")
    else:
        await message.answer(generate_response(torch, word2idx, max_len, idx2word, model, text))

# Запуск polling
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
