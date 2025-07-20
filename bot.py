# bot.py

import os
import asyncio
from pyrogram import Client
from handlers import setup_handlers
from utils.web_server import start_web_server
from utils.schedule import daily_post_scheduler
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME

bot = Client(
    name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():
    print("🌍 Starting web server...")
    await start_web_server()

    print("✅ Registering handlers...")
    setup_handlers(bot)

    print("⏰ Starting daily post scheduler...")
    asyncio.create_task(daily_post_scheduler(bot))

    print("🤖 Starting bot...")
    await bot.start()
    print("✅ Bot started.")

    await bot.idle()
    print("👋 Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Fallback for Render's already running loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("⚠️ Event loop already running. Using create_task fallback.")
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
