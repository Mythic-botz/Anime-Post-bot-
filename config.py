# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Webhook settings
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = int(os.getenv("PORT", 8000))

# Channel to auto-post
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1001234567890"))  # default fallback

# Admin(s)
ADMINS = list(map(int, os.getenv("ADMINS", "").split()))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

# Post schedule time
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", 9))  # 9 AM default
SCHEDULE_MIN = int(os.getenv("SCHEDULE_MIN", 0))    # 00 minutes
