# main.py
import os
from fastapi import FastAPI, Request
from pyrogram import Client
from pyrogram.types import Update
from config import API_ID, API_HASH, BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT, WEBHOOK_HOST
from bot.post import post_anime
from pyrogram import filters
from pyrogram.types import Message
import uvicorn

app = FastAPI()

bot = Client(
    "AnimeAutoPosterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./runtime",
    in_memory=True
)

@app.on_event("startup")
async def startup():
    await bot.start()
    print("✅ Bot started via webhook!")

@app.get("/")
def home():
    return {"status": "ok", "message": "🤖 Bot is running via webhook!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    raw_update = await request.body()
    update = Update.de_json(raw_update)
    await bot.process_update(update)
    return {"ok": True}

# Run FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host=WEBHOOK_HOST, port=WEBHOOK_PORT)