# bot.py
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pyrogram import Client
from dotenv import load_dotenv
import uvicorn

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # example: https://your-app.onrender.com
PORT = int(os.getenv("PORT", 8000))

bot = Client("animebot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ New lifespan event handling (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Starting bot with webhook...")
    await bot.start()
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook set to {WEBHOOK_URL}")
    yield
    print("🔻 Stopping bot...")
    await bot.stop()

app = FastAPI(lifespan=lifespan)

# ✅ Webhook endpoint
@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.body()
    await bot.process_update(data)
    return {"ok": True}
