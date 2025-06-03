import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dashscope import Generation
import dashscope

# === ВАЖНО: замени на свои токены ===
TELEGRAM_BOT_TOKEN = '7581031642:AAGe4Msn9E96TtydoL6yPG0p53Vpsml2N4A'  # <-- ЗДЕСЬ вставь свой Telegram Bot Token
DASHSCOPE_API_KEY = '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'

# Установка ключа для DashScope
dashscope.api_key = DASHSCOPE_API_KEY

# === Логика Qwen3 с выводом полного ответа ===
async def ask_qwen(prompt: str) -> str:
    try:
        response = Generation.call(
            model="qwen-turbo",  # можно попробовать qwen-plus или qwen-max
            prompt=prompt
        )

        print("📊 Полный ответ от Qwen:", response)  # Отладка: посмотри это в консоли

        if hasattr(response, 'output') and hasattr(response.output, 'text'):
            return response.output.text.strip()
        else:
            return "❌ Не удалось получить ответ от модели. Проверь консоль для деталей."
    except Exception as e:
        return f"⚠️ Ошибка при обращении к Qwen3: {e}"

# === Обработчики команд ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Привет! Я подключен к Qwen3. Задавай свои вопросы!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = await ask_qwen(user_input)
    await update.message.reply_text(reply)

# === Запуск бота ===
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print("🚀 Бот успешно запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling()
# === Основная функция запуска ===
if __name__ == '__main__':
    # Включение логирования
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling()