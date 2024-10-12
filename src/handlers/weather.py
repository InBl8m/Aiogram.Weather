import os
import aiohttp
from aiogram import Router
from aiogram.types import Message
from dotenv import load_dotenv
from src.services.groq import get_advice


router: Router = Router()
load_dotenv()
API_KEY = os.environ.get("OPENWEATHERMAP_TOKEN")


async def get_weather(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


@router.message()
async def weather_handler(message: Message):
    city = message.text.strip()
    weather_data = await get_weather(city)

    if weather_data:
        city_name = weather_data['name']
        temperature = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']

        response_text = (f"Погода в городе {city_name}:\n"
                         f"Температура: {temperature}°C\n"
                         f"Описание: {weather_desc}\n"
                         f"Скорость ветра: {wind_speed} м/с")

        await message.answer(response_text)
        # После получения погоды, вызываем хэндлер для совета
        advice = await get_advice(response_text)
        await message.answer(f"Совет: {advice}")

    else:
        await message.answer("Не удалось найти город. Попробуйте снова.")

