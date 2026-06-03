import telebot
from telebot import types
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN
from datetime import datetime
import time
import requests

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def is_allowed(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER_IDs:
        bot.send_message(message.chat.id, "У вас нет доступа!")
        return False
    return True


@bot.message_handler(func=lambda message: message.text == "ИБП")
def ups(message):
    if not is_allowed(message):
        return
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(10)
    bot.send_message(message.chat.id, "test message")


@bot.message_handler(func=lambda message: message.text == "Сервер")
def server(message):
    if not is_allowed(message):
        return
    now = datetime.now()
    bot.send_chat_action(message.chat.id, "печатает")
    time = f"Московское время: {now.hour} часов, {now.minute} минут."
    bot.send_message(message.chat.id, time)


@bot.message_handler(func=lambda message: message.text == "Диски")
def disks(message):
    if not is_allowed(message):
        return
    bot.send_chat_action(message.chat.id, "test")
    time.sleep(5)
    bot.send_message(message.chat.id, "disks info")


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton("Сервер")
    button2 = types.KeyboardButton("Диски")
    button3 = types.KeyboardButton("ИБП")

    markup.add(button1, button2, button3)
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message):
        return
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=main_keyboard())


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
