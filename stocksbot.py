import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Введите тикер компании.\n"
        "Например: AAPL, TSLA, BTI"
    )


@dp.message()
async def get_company_info(message: Message):
    ticker = message.text.upper()

    url = (
        f"https://api.massive.com/v3/reference/tickers/"
        f"{ticker}?apiKey={config.STOCKS_API_KEY}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                if response.status != 200:
                    await message.answer(
                        f"Ошибка API: {response.status}"
                    )
                    return

                data = await response.json()

        if "results" not in data:
            await message.answer(
                f"Тикер {ticker} не найден"
            )
            return

        company = data["results"]

        name = company.get("name", "Нет данных")
        market = company.get("market", "Нет данных")
        exchange = company.get("primary_exchange", "Нет данных")
        company_type = company.get("type", "Нет данных")
        currency = company.get("currency_name", "Нет данных")
        employees = company.get("total_employees", "Нет данных")
        list_date = company.get("list_date", "Нет данных")
        homepage = company.get("homepage_url", "Нет данных")
        description = company.get("description", "Нет данных")

        market_cap = company.get("market_cap")

        if market_cap:
            market_cap = f"{market_cap:,.0f}$"
        else:
            market_cap = "Нет данных"

        text = (
            f"📈 Тикер: {ticker}\n\n"
            f"🏢 Компания: {name}\n"
            f"🏦 Биржа: {exchange}\n"
            f"📊 Рынок: {market}\n"
            f"📁 Тип: {company_type}\n"
            f"💵 Валюта: {currency}\n"
            f"👥 Сотрудников: {employees}\n"
            f"💰 Капитализация: {market_cap}\n"
            f"📅 Дата листинга: {list_date}\n"
            f"🌐 Сайт: {homepage}\n\n"
            f"📝 Описание:\n{description}"
        )

        await message.answer(text)

    except Exception as e:
        await message.answer(
            f"Произошла ошибка:\n{e}"
        )