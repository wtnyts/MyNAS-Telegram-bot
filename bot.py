import telebot
from telebot import types
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN
from modules.Classes import Disk, Server, UPS


bot = telebot.TeleBot(TELEGRAM_TOKEN)


def restricted(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id not in ALLOWED_USER_IDs:
            bot.send_message(message.chat.id, "У вас нет доступа к этому боту!")
            return
        return func(message, *args, **kwargs)

    return wrapper


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton("Сервер")
    button2 = types.KeyboardButton("Диски")
    button3 = types.KeyboardButton("ИБП")

    markup.add(button1, button2, button3)
    return markup


@bot.message_handler(commands=["start"])
@restricted
def start(message):
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=main_keyboard())



@bot.message_handler(func=lambda message: message.text == "Сервер")
@restricted
def server(message):
    bot.send_chat_action(message.chat.id, "typing")

    server_1 = Server("MyNAS")
    total = server_1.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")



@bot.message_handler(func=lambda message: message.text == "Диски")
@restricted
def disks(message):
    bot.send_chat_action(message.chat.id, "typing")

#SSD
    root = Disk('Root', '/')
    docker = Disk('Docker', '/var/lib/docker')

#HDD
    toshiba_650 = Disk("Toshiba 650 Gb", '/media/toshiba_650')
    wd_6tb = Disk('WD 6 Tb', "/media/wd_6tb")

    total = "Статус дисков: \n\nSSD:\n"
    total += root.format()
    total += docker.format()
    total += "\n\nHDD:\n"
    total += toshiba_650.format()
    total += wd_6tb.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "ИБП")
@restricted
def ups(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ups_1 = UPS("CyberPower")
    total = ups_1.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")



if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
