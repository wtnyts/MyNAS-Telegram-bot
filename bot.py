import telebot
from telebot import types
from config import ALLOWED_USER_IDs, TELEGRAM_TOKEN
from datetime import datetime
import time
import requests

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def restricted(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id not in ALLOWED_USER_IDs:
            bot.send_message(message.chat.id, "У вас нет доступа к этому боту!")
            return
        return func(message, *args, **kwargs)

    return wrapper


def get_prometheus_metric(query):
    try:
        response = requests.get(
            "http://192.168.1.45:9090/api/v1/query", params={"query": query}, timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data["data"]["result"]:
                value = data["data"]["result"][0]["value"][1]
                return float(value)
    except:
        pass


@bot.message_handler(func=lambda message: message.text == "ИБП")
@restricted
def ups(message):
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(10)
    bot.send_message(message.chat.id, "test message")


@bot.message_handler(func=lambda message: message.text == "Сервер")
@restricted
def server(message):
    bot.send_chat_action(message.chat.id, "typing")

    cpu_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    cpu_temp_query = (
        'node_hwmon_temp_celsius{chip="platform_coretemp_0", sensor="temp1"}'
    )
    ram_query = (
        "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100"
    )

    cpu = get_prometheus_metric(cpu_query)
    cpu_temp = get_prometheus_metric(cpu_temp_query)
    ram = get_prometheus_metric(ram_query)

    total = "Статус сервера: \n\n"
    total += f"CPU: <b>{cpu:.1f}</b> %\n" if cpu is not None else f"CPU: нет данных\n"
    total += (
        f"CPU, t: <b>{cpu_temp:.1f}</b> °C\n"
        if cpu_temp is not None
        else f"CPU, t: нет данных\n"
    )
    total += f"RAM: <b>{ram:.1f}</b> %\n" if ram is not None else f"RAM: нет данных\n"

    bot.send_message(message.chat.id, total, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Диски")
@restricted
def disks(message):
    bot.send_chat_action(message.chat.id, "typing")

    root_free = 'node_filesystem_avail_bytes{mountpoint="/"} / 1024 / 1024 / 1024'
    root_total = 'node_filesystem_size_bytes{mountpoint="/"} / 1024 / 1024 / 1024'
    docker_free = (
        'node_filesystem_avail_bytes{mountpoint="/var/lib/docker"} / 1024 / 1024 / 1024'
    )
    docker_total = (
        'node_filesystem_size_bytes{mountpoint="/var/lib/docker"} / 1024 / 1024 / 1024'
    )
    hdd_toshiba_free = 'node_filesystem_avail_bytes{mountpoint="/media/toshiba_650"} / 1024 / 1024 / 1024'
    hdd_toshiba_total = 'node_filesystem_size_bytes{mountpoint="/media/toshiba_650"} / 1024 / 1024 / 1024'

    root_free = get_prometheus_metric(root_free)
    root_total = get_prometheus_metric(root_total)
    docker_free = get_prometheus_metric(docker_free)
    docker_total = get_prometheus_metric(docker_total)
    hdd_toshiba_free = get_prometheus_metric(hdd_toshiba_free)
    hdd_toshiba_total = get_prometheus_metric(hdd_toshiba_total)

    root_used = (
        root_total - root_free
        if (root_total is not None and root_free is not None)
        else None
    )
    docker_used = (
        docker_total - docker_free
        if (docker_total is not None and docker_free is not None)
        else None
    )
    hdd_toshiba_used = (
        hdd_toshiba_total - hdd_toshiba_free
        if (hdd_toshiba_total is not None and hdd_toshiba_free is not None)
        else None
    )

    def format_string(name, used, free, total):
        a = []

        if used is not None:
            a.append(f"использовано <b>{used:.1f}</b> Gb")
        else:
            a.append(f"использовано <b>НЕТ ДАННЫХ</b>")

        if free is not None:
            a.append(f"свободно <b>{free:.1f}</b> Gb")
        else:
            a.append(f"свободно <b>НЕТ ДАННЫХ</b>")

        if total is not None:
            a.append(f"всего <b>{total:.1f}</b> Gb")
        else:
            a.append(f"всего <b>НЕТ ДАННЫХ</b>")

        string = f"<b>{name}</b>: " + ", ".join(a) + "\n"

        return string

    total = "<b>Статус дисков</b>:\n\n<b>SSD</b>:\n"
    total += format_string("Root", root_used, root_free, root_total)
    total += format_string("Docker", docker_used, docker_free, docker_total)
    total += "\n<b>HDD</b>:\n"
    total += format_string(
        "Toshiba 650", hdd_toshiba_used, hdd_toshiba_free, hdd_toshiba_total
    )

    bot.send_message(message.chat.id, total, parse_mode="HTML")


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


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
