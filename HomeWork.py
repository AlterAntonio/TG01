import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import OPENWEATHER, TELETOKEN
import requests


def get_weather(city):
    api_key = OPENWEATHER
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    weather = response.json()
    if response.status_code != 200:
        return f"Погоду в {city} узнать не удалось. Проверьте название города."
    place = weather['name']
    tC = weather['main']['temp']
    description = weather['weather'][0]['description']
    return f'Погода в {place}\nТемпература: {tC}°C\nПогода: {description}'


bot = Bot(token=TELETOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Очень приятно, бот!")


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather")


@dp.message(Command('weather'))
async def ask_city(message: Message):
    await message.answer("Пожалуйста, введите название города:")

@dp.message()
async def weather_info(message: Message):
    city = message.text
    await message.answer(get_weather(city))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())