# bot.py

import asyncio
from pyrogram import Client, idle
from utils import load_config
from scheduler import daily_post_scheduler
import handlers  # this imports command handlers and attaches to the bot

# Load config from config.json
config = load_config()

# Create the bot client
bot = Client(
    "anime_post_bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

async def start_bot():
    await bot.start()
    print("[✅] Bot started.")

    # Start the post scheduler
    asyncio.create_task(daily_post_scheduler(bot))

    # Keep the bot running
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
