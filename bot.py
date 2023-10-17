import asyncio
import logging
import os
import sys

import dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import openai_connector
import openai
import db

dotenv.load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv('OPENAI_API_KEY')
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command_hander(message: types.Message):
    await message.answer("Добро пожаловать в Fine! 😊\n\nЗдесь ты сможешь с легкостью контролировать свои финансы "
                         "и поднимать свои накопления на новый уровень. 💰🚀\n\nВот что ты можешь сделать:"
                         "\n- Добавить или удалить доход 💵💸\n- Добавить или удалить расход "
                         "💳💰\n\nПриятного использования! 🌟")


@dp.message()
async def all_messages_handler(message: types.Message):
    detection_status, operation = openai_connector.detect_variables(message.text)
    if not detection_status:
        return await message.answer("Не удалось распознать сообщение. 😕\n\nПожалуйста, повторите попытку! 🔄")
    db.save_obj(operation)
    await message.answer(f'Спасибо. 😃 Данные успешно учтены!')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
