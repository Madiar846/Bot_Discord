import discord
from openai import OpenAI

# === МОИ API КЛЮЧИ ===
DISCORD_TOKEN = ""
OPENAI_API_KEY = ""

# === ИНИЦИАЛИЗАЦИЯ ===
client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# === СИСТЕМНЫЙ ПРОМПТ ===
SYSTEM_PROMPT = """
Ты аналитический ИИ.

Отвечай строго по структуре:

1. Причины
2. Контекст
3. Вывод

Без лишней воды.
Всегда подписывай, что ты ИИ и можешь ошибаться, что нужно проверять важную информацию самому.
"""

# === ОБРАБОТКА СООБЩЕНИЙ ===
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!analyze"):
        query = message.content.replace("!analyze", "").strip()

        if not query:
            await message.channel.send("Напиши вопрос после !analyze")
            return

        # сообщение о загрузке
        msg = await message.channel.send("Думаю...")

        try:
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ]
            )

            answer = response.choices[0].message.content

            await msg.edit(content=answer)

        except Exception as e:
            await msg.edit(content=f"Ошибка: {e}")

# === ЗАПУСК ===
client.run(DISCORD_TOKEN)
