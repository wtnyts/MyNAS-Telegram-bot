import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ALLOWED_USER_IDs = [int(i.strip()) for i in os.getenv('ALLOWED_USER_IDS', '').split(',') if i.strip()]