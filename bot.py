import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Функция обработки команды /start
async def start(update: Update, context):
    # URL картинки из вашего репозитория
    image_url = "https://raw.githubusercontent.com/SERGEYfit21/program/main/welcome.jpg"
    
    # Отправка картинки по URL
    await update.message.reply_photo(photo=image_url)

    # Текст приветственного сообщения
    welcome_message = (
        "Привет! 👋\n"
        "Меня зовут Сергей, и я дипломированный фитнес-тренер с 5-летним опытом. "
        "Уже более **70 клиентов** достигли своей цели 💪 — от снижения веса 🏋️‍♂️ до исправления осанки 🧘.\n\n"
        "Напишите мне, чтобы:\n"
        "- сформулировать вашу задачу (похудение, набор мышечной массы, осанка и т.д.);\n"
        "- получить индивидуальную программу тренировок 📋 или онлайн-сопровождение 🌐.\n\n"
        "**Пожалуйста, подождите немного, я скоро отвечу! 😊**"
    )
    
    # Отправка текстового сообщения
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

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
