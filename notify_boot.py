import os
import sys
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
USER_IDS = os.getenv('ALLOWED_USER_IDS')

if not TOKEN or not USER_IDS:
    sys.exit(1)

# 1. Получаем версию ядра
kernel = os.uname().release

# 2. Ищем ошибки в логах ПРОШЛОЙ загрузки
# -b -1 означает "предыдущая загрузка". Ищем паники, зависания и ошибки.
try:
    result = subprocess.run(
        ["journalctl", "-k", "-b", "-1", "-p", "err", "--no-pager"],
        capture_output=True, text=True, check=True
    )
    errors = result.stdout.strip()
except subprocess.CalledProcessError:
    errors = "не удалось прочитать логи"

# 3. Определяем причину
if errors and "No entries" not in errors:
    reason = "АВАРИЙНО"
    details = errors.split('\n')[-3:] # Берем последние 3 строки ошибок
    details_text = "\n".join(details)
else:
    reason = "планово"
    details_text = "не обнаружены"

message = f"Сервер MyNAS перезагружен {reason}"
if details_text:
    message += f"\n\nПоследние ошибки:\n{details_text}"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Ищем ID группы (у групп ID отрицательный, например -100123456789)
group_ids = []
for chat_id in USER_IDS.split(','):
    chat_id = chat_id.strip()
    if chat_id.startswith('-'):
        group_ids.append(chat_id)

# Если группа не найдена, можно отправить в первый попавшийся ID (или ничего не делать)
if not group_ids:
    print("В ALLOWED_USER_IDS не найдено ID группы (начинается с '-'). Уведомление не отправлено.")
    sys.exit(0)

# Отправляем только в группы
for chat_id in group_ids:
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass