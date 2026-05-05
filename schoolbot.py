import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import config
import db

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db.init_db()

# --- FSM состояния ---
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


# --- Старт ---
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Введи имя ученика:")
    await state.set_state(Form.name)


# --- Имя ---
@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введи возраст:")
    await state.set_state(Form.age)


# --- Возраст ---
@dp.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуй снова:")
        return

    await state.update_data(age=int(message.text))
    await message.answer("В каком классе учится?")
    await state.set_state(Form.grade)


# --- Класс ---
@dp.message(Form.grade)
async def get_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)

    data = await state.get_data()

    db.add_student(
        name=data["name"],
        age=data["age"],
        grade=data["grade"]
    )

    await message.answer("Данные сохранены ✅")
    await state.clear()