# bot.py

import os
from fastapi import FastAPI, Request
from pyrogram import Client

# ⚙️ Load environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Example: https://your-bot-name.onrender.com/

# ✅ Initialize Pyrogram Client
bot = Client("anime_post_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Telegram webhook route
@app.post("/")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        await bot._dispatch_raw_update(data)  # ✅ Pyrogram internal method for dispatching updates
        return {"ok": True}
    except Exception as e:
        print(f"❌ Error handling update: {e}")
        return {"ok": False, "error": str(e)}

# ✅ Startup: Start bot and set webhook
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting bot...")
    await bot.start()

    if WEBHOOK_URL:
        try:
            webhook_set = await bot.set_webhook(WEBHOOK_URL)
            print(f"✅ Webhook set to: {WEBHOOK_URL} | Success: {webhook_set}")
        except Exception as e:
            print(f"❌ Failed to set webhook: {e}")

# ✅ Shutdown: Stop bot cleanly
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Stopping bot...")
    await bot.stop()