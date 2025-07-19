# main.py
import os
from fastapi import FastAPI, Request
from pyrogram import Client, filters
from pyrogram.types import Update, Message
from config import API_ID, API_HASH, BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT, WEBHOOK_HOST
from bot.post import post_anime
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

# ✅ Register /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello Otaku!\n\nI'm your Anime Auto Poster Bot.\nUse /post to post a new anime episode!"
    )

# ✅ Register /post command
@bot.on_message(filters.command("post") & filters.private)
async def handle_post(client: Client, message: Message):
    await post_anime(client, message)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host=WEBHOOK_HOST, port=WEBHOOK_PORT)