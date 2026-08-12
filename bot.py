import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🚛 Code 95 Training Bot працює!\n\n"
        "Готуємось до тесту Code 95 🇵🇱"
    )

@bot.message_handler(commands=["test"])
def test(message):
    bot.reply_to(message, "✅ Тестовий режим працює.")

print("Bot started...")
bot.infinity_polling()
