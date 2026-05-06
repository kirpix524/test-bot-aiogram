from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

# =========================
# ЗАДАНИЕ 1 — Reply кнопки
# =========================

@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Привет")
    kb.button(text="Пока")
    kb.adjust(2)

    await message.answer(
        "Выберите действие:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )


@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(F.text == "Пока")
async def say_bye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# =========================
# ЗАДАНИЕ 2 — URL кнопки
# =========================

@dp.message(Command("links"))
async def cmd_links(message: Message):
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="Новости", url="https://news.google.com"),
        InlineKeyboardButton(text="Музыка", url="https://spotify.com"),
        InlineKeyboardButton(text="Видео", url="https://youtube.com")
    )

    await message.answer("Полезные ссылки:", reply_markup=kb.as_markup())


# =========================
# ЗАДАНИЕ 3 — Динамика
# =========================

@dp.message(Command("dynamic"))
async def cmd_dynamic(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Показать больше", callback_data="show_more")

    await message.answer(
        "Нажмите кнопку:",
        reply_markup=kb.as_markup()
    )


@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="Опция 1", callback_data="opt1")
    kb.button(text="Опция 2", callback_data="opt2")
    kb.adjust(2)

    # заменяем клавиатуру
    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())


@dp.callback_query(F.data == "opt1")
async def option_1(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали: Опция 1")
    await callback.answer()


@dp.callback_query(F.data == "opt2")
async def option_2(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали: Опция 2")
    await callback.answer()


