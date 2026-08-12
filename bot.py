import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

questions = [
    {
        "question": "Что является одним из условий получения разрешения на осуществление профессии дорожного перевозчика в области дорожной перевозки вещей?",
        "answers": [
            "A) Отсутствие судимости за серьёзное нарушение правил дорожного движения.",
            "B) Учреждение торгового общества.",
            "C) Наличие водительских прав категории C1."
        ],
        "correct": "A"
    },
    {
        "question": "Оказывает ли какое-либо влияние на прибыль либо убытки предприятия работающий в нём водитель?",
        "answers": [
            "A) Нет, ни в коем случае.",
            "B) Да, но только если он причастен к ДТП.",
            "C) Да, например путём неумелой эксплуатации транспортного средства."
        ],
        "correct": "C"
    },
    {
        "question": "Какой документ является основным, уполномочивающим на осуществление международного дорожного транспорта товаров?",
        "answers": [
            "A) Лицензия Сообщества.",
            "B) Разрешение на выполнение профессии международного автодорожного перевозчика.",
            "C) Справка о выполнении международных перевозок для личных нужд."
        ],
        "correct": "B"
    }
]

user_progress = {}


def send_question(chat_id):
    index = user_progress.get(chat_id, 0)

    if index >= len(questions):
        bot.send_message(
            chat_id,
            "🏁 Тест завершено!\n\nНапиши /test, щоб пройти ще раз."
        )
        user_progress[chat_id] = 0
        return

    q = questions[index]

    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        types.InlineKeyboardButton("A", callback_data="answer_A"),
        types.InlineKeyboardButton("B", callback_data="answer_B"),
        types.InlineKeyboardButton("C", callback_data="answer_C")
    )

    text = f"❓ Питання {index + 1}/{len(questions)}\n\n{q['question']}\n\n"
    text += "\n\n".join(q["answers"])

    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🚛 Code 95 Training Bot працює!\n\n"
        "Для початку тесту натисни /test"
    )


@bot.message_handler(commands=["test"])
def test(message):
    user_progress[message.chat.id] = 0
    send_question(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def answer(call):
    chat_id = call.message.chat.id
    index = user_progress.get(chat_id, 0)

    if index >= len(questions):
        return

    selected = call.data.split("_")[1]
    correct = questions[index]["correct"]

    if selected == correct:
        result = "✅ Правильно!"
    else:
        result = f"❌ Неправильно.\nПравильна відповідь: {correct}"

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, result)

    user_progress[chat_id] = index + 1
    send_question(chat_id)


print("Bot started...")
bot.infinity_polling()
