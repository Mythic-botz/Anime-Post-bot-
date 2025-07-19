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

# Initialize Pyrogram Client (in-memory session)
bot = Client(
    "AnimeAutoPosterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./runtime",
    in_memory=True
)

# /start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello Otaku!\n\nI'm your Anime Auto Poster Bot.\nUse /post to post a new anime episode!"
    )

# /post command handler
@bot.on_message(filters.command("post") & filters.private)
async def handle_post(client: Client, message: Message):
    await post_anime(client, message)

# Health check route for Render
@app.get("/")
def read_root():
    return {"status": "✅ Bot is running on webhook!"}

# Telegram webhook endpoint
@app.post(f"/webhook")
async def telegram_webhook(request: Request):
    raw_update = await request.body()
    update = Update.de_json(raw_update)
    await bot.process_update(update)
    return {"ok": True}

# Bot startup + webhook setup
if __name__ == "__main__":
    import asyncio

    async def startup():
        await bot.start()
        await bot.set_webhook(url=https://anime-post-bot-256h.onrender.com)
        print("✅ Webhook set successfully.")

    asyncio.get_event_loop().run_until_complete(startup())
    uvicorn.run("main:app", host=WEBHOOK_HOST, port=WEBHOOK_PORT)
