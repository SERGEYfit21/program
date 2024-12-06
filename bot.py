import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Функция обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text("Добро пожаловать в моего бота! Напишите мне, чтобы узнать больше.")

# Основной блок
if __name__ == "__main__":
    # Получение токена из переменной окружения
    TOKEN = os.getenv("TOKEN")

    # Проверяем, задан ли токен
    if not TOKEN:
        print("Ошибка: Токен не найден. Убедитесь, что переменная окружения 'TOKEN' задана.")
        exit(1)

    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    app.run_polling()
