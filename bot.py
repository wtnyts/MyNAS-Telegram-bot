import telebot
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def is_allowed(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER_IDs:
        bot.send_message(message.chat.id, "У вас нет доступа!")
        return False
    return True


@bot.message_handler(commands=["test"])
def test(message):
    if not is_allowed(message):
        return
    bot.send_message(message.chat.id, "test message")


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
