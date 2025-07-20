# bot.py
import os
from fastapi import FastAPI, Request
from pyrogram import Client
from pyrogram.types import Update

# ⚙️ Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Pyrogram Client
bot = Client(
    name="bot",  # <- must NOT be None
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ✅ FastAPI app
app = FastAPI()

# ✅ Import handlers
from handlers import setup_handlers
setup_handlers(bot)

@app.on_event("startup")
async def startup():
    print("🚀 Bot starting...")
    await bot.start()

@app.on_event("shutdown")
async def shutdown():
    print("🛑 Bot stopping...")
    await bot.stop()

@app.post("/")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot)  # ✅ Parse JSON to Pyrogram Update
        await bot.dispatch(update)          # ✅ Dispatch update to handlers
        return {"ok": True}
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"ok": False, "error": str(e)}