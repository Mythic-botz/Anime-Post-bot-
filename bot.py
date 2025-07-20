# bot.py

import os
from fastapi import FastAPI, Request
from pyrogram import Client
from pyrogram.types import Update

# ⚙️ Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Pyrogram Bot Client (in-memory session, avoids flood)
bot = Client(
    name=":memory:",  # ➜ avoids file system session creation
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ FastAPI App
app = FastAPI()

# ✅ Webhook Handler
@app.post("/")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        update = Update(data)
        await bot.invoke_update(update)
        return {"ok": True}
    except Exception as e:
        print(f"❌ Error handling update: {e}")
        return {"ok": False, "error": str(e)}

# ✅ FastAPI Lifecycle Hooks
@app.on_event("startup")
async def startup_event():
    print("🚀 Bot starting...")
    await bot.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Bot stopping...")
    await bot.stop()