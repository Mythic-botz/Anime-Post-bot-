# bot.py

import asyncio
from pyrogram import Client
from pyrogram.types import Update
from utils import load_config
from scheduler import daily_post_scheduler
import handlers

config = load_config()

app = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

async def start():
    await app.start()
    print("[✅] Bot started with webhook.")

    await app.set_webhook(
        url=config["webhook_url"],
        max_connections=40
    )

    # Start scheduler
    asyncio.create_task(daily_post_scheduler(app))

    # Keep running forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start())
