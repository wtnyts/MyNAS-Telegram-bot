import telebot
from telebot import types
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN
from modules.Classes import Disk, Server, UPS, home_todo


bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_state = {}


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
    button2 = types.KeyboardButton("Дела")

    markup.add(button1, button2)
    return markup

def todo_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton("Выбор")
    button2 = types.KeyboardButton("Добавить")
    button3 = types.KeyboardButton("Удалить")
    button4 = types.KeyboardButton("Назад")

    markup.add(button1, button2, button3, button4)
    return markup


def server_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = types.KeyboardButton("CPU/RAM")
    button2 = types.KeyboardButton("Диски")
    button3 = types.KeyboardButton("ИБП")
    button4 = types.KeyboardButton("Назад")

    markup.add(button1, button2, button3, button4)
    return markup

@bot.message_handler(commands=["start"])
@restricted
def start(message):
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "Сервер")
@restricted
def server_keyboard_message(message):
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=server_keyboard())

@bot.message_handler(func=lambda message: message.text == "Дела")
@restricted
def todo_keyboard_message(message):
    user_state[message.from_user.id] = None
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=todo_keyboard())

@bot.message_handler(func=lambda message: message.text == "Назад")
@restricted
def back_to_main_keyboard(message):
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "Выбор")
@restricted
def todo(message):
    bot.send_chat_action(message.chat.id, "typing")

    text = home_todo("random_todo")
    total = text.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "Добавить")
@restricted
def add_todo_start(message):
    user_state[message.from_user.id] = "adding"
    print(f"DEBUG set adding for {message.from_user.id}")
    bot.send_message(message.chat.id, "Введи текст:")


@bot.message_handler(func=lambda message: message.text == "Удалить")
@restricted
def delete_todo_start(message):
    todo_obj = home_todo("random_todo")
    items = todo_obj.all()
    if not items:
        bot.send_message(message.chat.id, "Список дел пуст.")
        return
    lines = ["Выбери номер дела для удаления:\n"]
    for i, item in enumerate(items, start=1):
        lines.append(f"{i}. {item}")
    user_state[message.from_user.id] = "deleting"
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(func=lambda message: message.text == "CPU/RAM")
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
#   toshiba_650 = Disk("Toshiba 650 Gb", '/media/toshiba_650')
    wd_6tb = Disk('WD 6 Tb', "/media/wd_6tb")
    wd_1tb_media = Disk('WD 1 Tb Media', "/media/wd1tb_media")

    total = "Статус дисков: \n\nSSD:\n"
    total += root.format()
    total += docker.format()
    total += "\nHDD:\n"
#    total += toshiba_650.format()
    total += wd_6tb.format()
    total += wd_1tb_media.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "ИБП")
@restricted
def ups(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ups_1 = UPS("CyberPower")
    total = ups_1.format()

    bot.send_message(message.chat.id, total, parse_mode="HTML")


@bot.message_handler(func=lambda message: True, content_types=["text"])
@restricted
def handle_text_input(message):
    state = user_state.get(message.from_user.id)
    print(f"DEBUG state={state} text={message.text}") 
    if state == "adding":
        text = message.text.strip()
        if not text:
            bot.send_message(message.chat.id, "Пустое сообщение.")
            return
        todo_obj = home_todo("random_todo")
        todo_obj.add(text)
        user_state[message.from_user.id] = None
        bot.send_message(message.chat.id, f"Добавлено: {text}", reply_markup=todo_keyboard())

    elif state == "deleting":
        text = message.text.strip()
        if not text.isdigit():
            bot.send_message(message.chat.id, "Введи номер из списка.")
            return
        index = int(text) - 1
        todo_obj = home_todo("random_todo")
        removed = todo_obj.delete(index)
        user_state[message.from_user.id] = None
        if removed is None:
            bot.send_message(message.chat.id, "Нет дела с таким номером.")
        else:
            bot.send_message(message.chat.id, f"Удалено: {removed}", reply_markup=todo_keyboard())



if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
