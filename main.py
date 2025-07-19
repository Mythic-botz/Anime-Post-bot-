# main.py
import os
import json
from fastapi import FastAPI, Request
from pyrogram import Client, filters
from pyrogram.types import Message, Update
from config import API_ID, API_HASH, BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_URL, CHANNEL_ID
import uvicorn
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import generate_daily_post

app = FastAPI()

bot = Client(
    "AnimeAutoPosterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./runtime",
    in_memory=True
)

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    await bot.start()
    print("✅ Bot started via webhook!")

    # Schedule auto-post at 9 PM JST (12:00 UTC)
    scheduler.add_job(auto_post_daily, "cron", hour=12, minute=0)
    scheduler.start()
    print("📅 Scheduler started for daily posts.")

async def auto_post_daily():
    try:
        post_text = generate_daily_post()
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text, disable_web_page_preview=True)
        print("📢 Daily post sent successfully.")
    except Exception as e:
        print("❌ Failed to send daily post:", e)

@app.get("/")
def home():
    return {"status": "ok", "message": "🤖 Bot is running via webhook!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    raw_update = await request.body()
    update = Update.de_json(raw_update)
    await bot.process_update(update)
    return {"ok": True}

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply_text("👋 Hello Otaku! Use /post to manually send today’s anime post.\nUpdate JSON with /update.")

@bot.on_message(filters.command("post") & filters.private)
async def handle_post(client: Client, message: Message):
    try:
        post_text = generate_daily_post()
        await client.send_message(chat_id=CHANNEL_ID, text=post_text, disable_web_page_preview=True)
        await message.reply_text("✅ Sent today’s anime post.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@bot.on_message(filters.command("update") & filters.private)
async def update_json(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("⚠️ Please reply to a JSON file.")

    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".json"):
        return await message.reply_text("⚠️ Only .json files are accepted.")

    path = "daily.json"
    try:
        await doc.download(file_name=path)
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)  # Validate format
        await message.reply_text("✅ JSON updated successfully.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to update JSON: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host=WEBHOOK_HOST, port=WEBHOOK_PORT)
