import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Вопросы для опроса
QUESTIONS = [
    {"text": "Ваш пол?", "options": ["Мужчина", "Женщина"]},
    {"text": "Количество тренировочных дней в неделю?", "options": ["Два дня", "Три дня"]},
    {"text": "Ваш опыт тренировок?", "options": ["До 1 года", "От 1 до 3 лет", "Более 3 лет"]},
    {"text": "Травмы и ограничения?", "options": ["Плоскостопие", "Сколиоз", "Без особенностей"]}
]

# Ответы пользователя
user_answers = {}

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Приветственное сообщение
    welcome_message = (
        "Привет! 👋\n"
        "Меня зовут Сергей, и я дипломированный фитнес-тренер с 5-летним опытом. "
        "Уже более **70 клиентов** достигли своей цели 💪 — от снижения веса 🏋️‍♂️ до исправления осанки 🧘.\n\n"
        "Напишите мне, чтобы:\n"
        "- сформулировать вашу задачу (похудение, набор мышечной массы, осанка и т.д.);\n"
        "- получить индивидуальную программу тренировок 📋 или онлайн-сопровождение 🌐.\n\n"
        "Выберите один из вариантов ниже, чтобы начать! 😊"
    )

    # Кнопки
    keyboard = [
        [InlineKeyboardButton("Купить программу тренировок", callback_data="buy_program")],
        [InlineKeyboardButton("Онлайн ведение", callback_data="online_guidance")],
        [InlineKeyboardButton("Составить индивидуальную программу", callback_data="custom_program")],
        [InlineKeyboardButton("Хочу задать вопрос тренеру", callback_data="ask_trainer")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ["online_guidance", "custom_program", "ask_trainer"]:
        # Ответ на кнопки 2, 3, 4
        response = (
            "Ваш запрос принят! 🕒\n"
            "Тренер ответит в самое ближайшее время. Спасибо за терпение! 😊"
        )
        await query.edit_message_text(text=response)

    elif query.data == "buy_program":
        # Начало опроса
        user_id = query.from_user.id
        user_answers[user_id] = []  # Инициализация ответов пользователя
        await send_question(query, context, 0)

# Отправка вопроса
async def send_question(query, context, question_index):
    question = QUESTIONS[question_index]
    keyboard = [[InlineKeyboardButton(option, callback_data=f"q_{question_index}_{option}")] for option in question["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=question["text"], reply_markup=reply_markup)

# Обработчик ответов на вопросы
async def question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получение данных
    data = query.data
    user_id = query.from_user.id
    _, question_index, answer = data.split("_")
    question_index = int(question_index)

    # Сохранение ответа
    user_answers[user_id].append(answer)

    # Переход к следующему вопросу
    if question_index + 1 < len(QUESTIONS):
        await send_question(query, context, question_index + 1)
    else:
        # Завершение опроса и отправка файла
        await query.edit_message_text(text="Спасибо за ответы! Сейчас подберу для вас программу...")

        # Генерация имени файла на основе ответов
        file_name = "_".join(user_answers[user_id]) + ".xlsx"

        # Путь к файлу (предполагается, что файлы хранятся локально)
        file_path = f"./programs/{file_name}"

        # Проверка существования файла и отправка
        if os.path.exists(file_path):
            await query.message.reply_document(document=open(file_path, "rb"))
        else:
            await query.message.reply_text("Извините, подходящей программы пока нет. Пожалуйста, свяжитесь с тренером!")

# Основной блок
if __name__ == "__main__":
    # Получение токена
    TOKEN = os.getenv("TOKEN")

    # Проверка токена
    if not TOKEN:
        print("Ошибка: Токен не найден. Убедитесь, что переменная окружения 'TOKEN' задана.")
        exit(1)

    # Создание приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(buy_program|online_guidance|custom_program|ask_trainer)$"))
    app.add_handler(CallbackQueryHandler(question_handler, pattern="^q_"))

    # Запуск бота
    app.run_polling()
