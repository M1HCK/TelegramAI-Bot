# 🤖 TelegramAI-Bot

Простой Telegram-бот, который использует мощные языковые модели через [OpenRouter](https://openrouter.ai/), чтобы отвечать на вопросы пользователей. Поддерживает переключение между двумя моделями: **Qwen** и **Gemini**.

---

## 🚀 Функции

- Общение с ИИ через команды или обычные сообщения
- Выбор одной из двух языковых моделей:
  - **Qwen 30B-A3B** — мощная модель для сложных задач
  - **Gemini 1.5 Flash** — легковесная и быстрая модель
- Информация о моделях прямо в боте
- Поддержка потоковой передачи (streaming) ответов от API

---

## 🔧 Техническая информация

- **Фреймворк:** [aiogram 3.x](https://github.com/aiogram/aiogram)
- **API:** OpenRouter
- **Асинхронность:** `aiohttp`, `asyncio`
- **Конфигурация:** переменные окружения через `.env`

---

## 📦 Установка и запуск

### 1. Клонируй репозиторий:

```bash
git clone https://github.com/M1HCK/TelegramAI-Bot.git
cd TelegramAI-Bot
```

### 2. Установи зависимости:

```bash
pip install aiogram aiohttp python-dotenv
```

### 3. Создай `.env` файл:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 4. Запусти бота:

```bash
python bot.py
```

---

## ☁️ Деплой на Render

Этот бот готов к деплою на [Render](https://render.com). Просто укажи:

- Репозиторий
- Переменные окружения:
  - `TELEGRAM_BOT_TOKEN`
  - `OPENROUTER_API_KEY`

Render сам соберёт проект и запустит его.

---

> 🌟 Приятного использования! Если понравилось — звёздочка не помешает 😄  
> Автор: [@M1HCK](https://github.com/M1HCK)
