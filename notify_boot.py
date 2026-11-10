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
    errors = "Не удалось прочитать логи"

# 3. Определяем причину
if errors and "No entries" not in errors:
    reason = "АВАРИЙНАЯ"
    details = errors.split('\n')[-3:] # Берем последние 3 строки ошибок
    details_text = "\n".join(details)
else:
    reason = "Плановая"
    details_text = "Логи чистые"

message = f"Сервер mynas перезагружен.\nПричина: {reason}\nЯдро: {kernel}"
if details_text:
    message += f"\n\nПоследние ошибки:\n{details_text}"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

for user_id in USER_IDS.split(','):
    user_id = user_id.strip()
    if user_id:
        payload = {
            "chat_id": user_id,
            "text": message
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception:
            pass