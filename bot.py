import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
import aiohttp
import time
from googletrans import Translator
from gtts import gTTS

import config

class VoiceState(StatesGroup):
    waiting_for_text_to_voice = State()
    waiting_for_text_to_translate = State()



bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

translator = Translator()

# создаем папку img если нет
if not os.path.exists("img"):
    os.makedirs("img")

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

# =========================
# 📸 СОХРАНЕНИЕ ФОТО
# =========================
@dp.message(lambda message: message.photo)
async def save_photo(message: Message):
    photo = message.photo[-1]  # самое большое фото
    file = await bot.get_file(photo.file_id)

    file_path = file.file_path
    file_name = f"img/{photo.file_id}.jpg"

    await bot.download_file(file_path, file_name)

    await message.answer("Фото сохранено 📸")

@dp.message(Command("voice"))
async def voice_start(message: Message, state: FSMContext):
    await message.answer("Напиши текст, и я озвучу его 🎤")
    await state.set_state(VoiceState.waiting_for_text_to_voice)

@dp.message(VoiceState.waiting_for_text_to_voice)
async def generate_voice(message: Message, state: FSMContext):
    text = message.text

    # создаем папку если нет
    if not os.path.exists("voice"):
        os.makedirs("voice")

    # уникальное имя файла
    filename = f"voice/{message.chat.id}_{int(time.time())}.mp3"

    # генерация речи
    tts = gTTS(text=text, lang='ru')
    tts.save(filename)

    # отправка
    voice = FSInputFile(filename)
    await message.answer_voice(voice)

    # сброс состояния
    await state.clear()

# =========================
# 🌍 ПЕРЕВОД ТЕКСТА
# =========================
@dp.message(Command("translate"))
async def voice_start(message: Message, state: FSMContext):
    await message.answer("Напиши текст, и я переведу его")
    await state.set_state(VoiceState.waiting_for_text_to_translate)

@dp.message(VoiceState.waiting_for_text_to_translate)
async def translate_text(message: Message):
    translated = await translator.translate(message.text, dest='en')

    await message.answer(
        f"🇬🇧 Перевод:\n{translated.text}"
    )