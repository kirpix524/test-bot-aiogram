import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()


async def get_weather(city: str) -> str:
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={config.WEATHER_TOKEN}&units=metric&lang=ru"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    # обработка ошибок
    if data.get("cod") != 200:
        return "Город не найден 😢"

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    description = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    return (
        f"🌆 {city}\n"
        f"🌡 Температура: {temp}°C\n"
        f"🤔 Ощущается как: {feels}°C\n"
        f"☁️ {description}\n"
        f"💨 Ветер: {wind} м/с"
    )

def cities_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Саратов", callback_data="city_Saratov"),
            InlineKeyboardButton(text="Москва", callback_data="city_Moscow")
        ]
    ])
    return keyboard

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        config.START_MESSAGE,
        reply_markup=cities_keyboard()
    )

@dp.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(config.HELP_MESSAGE)

@dp.callback_query()
async def process_callback(callback_query):
    city = callback_query.data.replace("city_", "")

    weather = await get_weather(city)

    await callback_query.message.answer(weather)
    await callback_query.answer()  # обязательно!