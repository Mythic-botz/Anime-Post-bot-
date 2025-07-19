import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-render-app.onrender.com
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8000

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # e.g., -100xxxxxxxxx
WATERMARK = os.getenv("WATERMARK", "@Mythic_Animes")
