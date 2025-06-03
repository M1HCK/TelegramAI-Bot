import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiohttp
from aiogram import F
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# === Токены и модели ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SUPPORTED_MODELS = {
    "qwen": "qwen/qwen3-30b-a3b:free",
    "gemini": "google/gemini-flash-1.5"
}

# === Хранилище моделей пользователей ===
user_models = {}

# === Инициализация бота ===
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# === Клавиатуры ===
def get_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧠 О моделях")],
            [KeyboardButton(text="🔄 Сменить модель")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_model_selection_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡️ Qwen")],
            [KeyboardButton(text="✨ Gemini")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# === Сообщение при старте ===
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_models[user_id] = user_models.get(user_id, "qwen")
    await message.answer("Добро пожаловать!", reply_markup=get_menu_keyboard())
    await update_menu(message)


async def update_menu(message: types.Message):
    # Обновляем меню без нового текстового сообщения
    try:
        # Попробуем отредактировать последнее сообщение
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.message_id - 1,  # Предыдущее сообщение
            reply_markup=get_menu_keyboard()
        )
    except Exception as e:
        # Если не получилось — просто игнорируем или можно отправить новое сообщение
        pass

# === Обработка кнопки "О моделях" ===
@dp.message(F.text == "🧠 О моделях")
async def about_models(message: types.Message):
    text = (
        "🤖 *Доступные модели:*\n\n"
        "⚡️ *Qwen 30B-A3B* — мощная, точная, качественная модель.\n"
        "✨ *Gemini 1.5 flash* — быстрая, для повседневных задач."
    )
    await message.reply(text, parse_mode="Markdown")


# === Обработка кнопки "Сменить модель" ===
@dp.message(F.text == "🔄 Сменить модель")
async def change_model_button(message: types.Message):
    keyboard = get_model_selection_keyboard()
    await message.reply("Выберите новую модель:", reply_markup=keyboard)


@dp.message(F.text.in_(["⚡️ Qwen", "✨ Gemini"]))
async def handle_model_choice(message: types.Message):
    user_id = message.from_user.id
    if "Qwen" in message.text:
        user_models[user_id] = "qwen"
        await message.reply("✅ Модель изменена на *Qwen*", parse_mode="Markdown")
    else:
        user_models[user_id] = "gemini"
        await message.reply("✅ Модель изменена на *Gemini*", parse_mode="Markdown")
    await update_menu(message)


# === Вызов LLM через OpenRouter ===
async def invoke_llm_api(user_content: str, model_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://my-telegram-bot.com",
        "X-Title": "Qwen3 + Gemini Bot"
    }

    body = {
        "model": SUPPORTED_MODELS[model_key],
        "messages": [
            {"role": "system", "content": "Отвечай кратко и понятно, как в чате."},
            {"role": "user", "content": user_content}
        ],
        "stream": True,
        "max_tokens": 1024,
        "temperature": 0.7
    }

    full_response = ""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://openrouter.ai/api/v1/chat/completions",  headers=headers, json=body) as response:
                if response.status != 200:
                    return f"Ошибка API: HTTP {response.status}"
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            if chunk.get("choices") and chunk["choices"][0].get("delta"):
                                content = chunk["choices"][0]["delta"].get("content")
                                if content:
                                    full_response += content
                        except Exception as e:
                            print(f"Ошибка обработки чанка: {e}")
    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        return f"Ошибка: {e}"

    return full_response.strip()


# === Обработка текстовых сообщений ===
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    model_key = user_models.get(user_id, "qwen")

    processing_msg = await message.reply("🧠 Думаю...")

    response = await invoke_llm_api(message.text, model_key)

    await bot.delete_message(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id)

    if response:
        for i in range(0, len(response), 4096):
            await message.reply(response[i:i + 4096])
    else:
        await message.reply("⚠️ Не удалось получить ответ от модели.")


# === Запуск бота ===
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())