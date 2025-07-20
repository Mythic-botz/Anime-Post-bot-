# bot.py
import os
from fastapi import FastAPI, Request
from pyrogram import Client

# ⚙️ Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Initialize Pyrogram Client
bot = Client("anime_post_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Webhook endpoint to receive updates
@app.post("/")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        await bot._dispatch_raw_update(data)  # ✅ Correct internal method
        return {"ok": True}
    except Exception as e:
        print(f"❌ Error handling update: {e}")
        return {"ok": False, "error": str(e)}

# ✅ Start bot before server begins
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting bot...")
    await bot.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Stopping bot...")
    await bot.stop()