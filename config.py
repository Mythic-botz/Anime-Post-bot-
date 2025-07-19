import os

API_ID = int(os.getenv("API_ID", "23476863"))
API_HASH = os.getenv("API_HASH", "69daa0835439c4211f34c2e9ad0acb5c")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", ""))
WATERMARK = os.getenv("WATERMARK", "@Mythic_Animes")

# Web support 
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = int(os.getenv("PORT", 8080))  # Render uses this
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app-name.onrender.com/webhook")
