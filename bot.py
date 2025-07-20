# bot.py
import os
import logging
from fastapi import FastAPI, Request
from pyrogram import Client
from pyrogram.types import Update

# Load ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your Render webhook URL

# Bot instance
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup():
    logging.info("🔄 Starting bot...")
    await bot.start()
    logging.info("✅ Bot started!")

@app.on_event("shutdown")
async def shutdown():
    logging.info("⏹️ Stopping bot...")
    await bot.stop()
    logging.info("🚫 Bot stopped!")

@app.post("/")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data)
    await bot.dispatcher.feed_update(update)
    return {"ok": True}
