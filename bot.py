# bot.py
import os
import asyncio
from fastapi import FastAPI, Request
from pyrogram import Client
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # eg: https://your-bot-name.onrender.com
PORT = int(os.getenv("PORT", 8000))

# Initialize bot
bot = Client("animebot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize FastAPI
app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Starting bot and setting webhook...")
    await bot.start()
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook set to {WEBHOOK_URL}")


@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    await bot.stop()


@app.post("/")
async def telegram_webhook(req: Request):
    update = await req.body()
    await bot.process_update(update)
    return {"ok": True}
