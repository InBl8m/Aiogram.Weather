import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=groq_api_key)


async def get_advice(advice_message) -> str:
    """Получает совет на основе информации о погоде."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": advice_message + 'Что посовутуешь, кратко, на русском',
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Ошибка при обращении к Groq API: {e}"
