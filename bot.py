import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(config.START_MESSAGE)

@dp.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(config.HELP_MESSAGE)