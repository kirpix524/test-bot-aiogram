import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import config
import findb as db

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

db.init_db()


# ---------- Клавиатура ----------
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сделать расчет")],
        [KeyboardButton(text="История расчетов")]
    ],
    resize_keyboard=True
)


# ---------- Состояния ----------
class FinanceState(StatesGroup):
    income = State()
    expenses = State()


# ---------- Старт ----------
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я помогу распределить ваш доход.",
        reply_markup=main_keyboard
    )


# ---------- Выбор расчета ----------
@dp.message(lambda message: message.text == "Сделать расчет")
async def calc_start(message: Message, state: FSMContext):
    await message.answer("Введите ваш ежемесячный доход:")
    await state.set_state(FinanceState.income)


# ---------- Доход ----------
@dp.message(FinanceState.income)
async def get_income(message: Message, state: FSMContext):
    try:
        income = float(message.text)

        if income <= 0:
            await message.answer("Введите число больше 0")
            return

        await state.update_data(income=income)
        await message.answer("Введите обязательные расходы:")
        await state.set_state(FinanceState.expenses)

    except ValueError:
        await message.answer("Введите корректное число")


# ---------- Расходы ----------
@dp.message(FinanceState.expenses)
async def get_expenses(message: Message, state: FSMContext):
    try:
        expenses = float(message.text)

        data = await state.get_data()
        income = data["income"]

        balance = income - expenses

        if balance <= 0:
            await message.answer("Свободных средств нет", reply_markup=main_keyboard)
            await state.clear()
            return

        emergency = balance * 0.5
        fun = balance * 0.25
        invest = balance * 0.25

        user_id = message.from_user.id

        db.save_calculation(
            user_id=user_id,
            income=income,
            expenses=expenses,
            invest=invest
        )

        await message.answer(
            f"Свободный остаток: {balance:.2f}\n\n"
            f"Непредвиденные расходы: {emergency:.2f}\n"
            f"Развлечения: {fun:.2f}\n"
            f"Инвестиции: {invest:.2f}",
            reply_markup=main_keyboard
        )

        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число")


# ---------- История ----------
@dp.message(lambda message: message.text == "История расчетов")
async def show_history(message: Message):
    user_id = message.from_user.id
    rows = db.get_history(user_id)

    if not rows:
        await message.answer("История пуста")
        return

    text = "Ваши последние расчеты:\n\n"

    for row in rows:
        text += (
            f"Доход: {row[0]}\n"
            f"Расходы: {row[1]}\n"
            f"Инвестиции: {row[2]}\n"
            f"---\n"
        )

    await message.answer(text)