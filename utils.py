# bot/utils.py

from datetime import datetime
import pytz
from config import TIMEZONE

def get_today_date():
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz).strftime("%A – %B %d")  # Example: Sunday – July 21

def is_admin(user_id: int) -> bool:
    from config import ADMINS
    return user_id in ADMINS

def log_error(e: Exception):
    print(f"[ERROR] {type(e).__name__}: {e}")
