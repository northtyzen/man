import asyncio import logging from aiogram import Bot, Dispatcher, types from aiogram.filters import CommandStart from aiogram.client.default import DefaultBotProperties

# Конфигурация

BOT\_TOKEN = "ВАШ\_ТОКЕН\_БОТА"

# Инициализация

bot = Bot(token=BOT\_TOKEN) dp = Dispatcher() logging.basicConfig(level=logging.INFO)

# Стартовый хэндлер

@dp.message(CommandStart()) async def start\_cmd(message: types.Message): await message.answer("Бот запущен и готов к работе!")

# Запуск

async def main(): await dp.start\_polling(bot)

if **name** == "**main**": asyncio.run(main())
