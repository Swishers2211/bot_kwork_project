import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command

API_TOKEN = os.environ.get('TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def send_web_app_button(message: types.Message):
    # Ссылка на веб-приложение
    web_app_url = 'https://ifutures.ru'

    # Создаем кнопку с веб-приложением
    web_app_button = KeyboardButton(
        text="Открыть приложение",
        web_app=WebAppInfo(url=web_app_url)
    )

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[web_app_button]],  # Оборачиваем кнопку в список списков
        resize_keyboard=True
    )

    # Отправляем сообщение с клавиатурой
    await message.answer("Нажмите на кнопку, чтобы открыть приложение:", reply_markup=keyboard)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
