import telebot
from telebot import types
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN
from datetime import datetime
import time
import request

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def is_allowed(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER_IDs:
        bot.send_message(message.chat.id, "У вас нет доступа!")
        return False
    return True


@bot.message_handler(func=lambda message: message.text == "UPS Info")
def test(message):
    if not is_allowed(message):
        return
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(10)
    bot.send_message(message.chat.id, "test message")


@bot.message_handler(func=lambda message: message.text == "Время")
def test(message):
    if not is_allowed(message):
        return
    now = datetime.now()
    time = f"Московское время: {now.hour} часов, {now.minute} минут."
    bot.send_message(message.chat.id, time)


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton("UPS Info")
    button2 = types.KeyboardButton("Время")

    markup.add(button1, button2)
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message):
        return
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=main_keyboard())


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
