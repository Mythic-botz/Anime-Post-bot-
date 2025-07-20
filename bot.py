# bot.py

import os
from fastapi import FastAPI, Request
from pyrogram import Client
from pyrogram.types import Update

# ⚙️ Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-app.onrender.com/

# ✅ Initialize Pyrogram Client
bot = Client(
    name=None,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Load handlers (you must call this)
from handlers import setup_handlers
setup_handlers(bot)

# ✅ FastAPI App
app = FastAPI()


# ✅ Webhook handler
@app.post("/")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot)  # ✅ Correct for webhook-based updates
        await bot.process_update(update)    # ✅ THIS is the correct method
        return {"ok": True}
    except Exception as e:
        print(f"❌ Error handling update: {e}")
        return {"ok": False, "error": str(e)}


# ✅ Startup: Start bot and set webhook
@app.on_event("startup")
async def startup():
    print("🚀 Starting bot...")
    await bot.start()
    try:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook set to {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Webhook error: {e}")


# ✅ Shutdown: Stop bot
@app.on_event("shutdown")
async def shutdown():
    print("🛑 Stopping bot...")
    await bot.stop()