# bot.py
import asyncio
from pyrogram import Client
from pyrogram.idle import idle

from utils import load_config
from scheduler import daily_post_scheduler

# Load configuration
config = load_config()

# Initialize the Pyrogram Client
bot = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

# ✅ Import handlers only AFTER bot is defined to avoid circular import
import handlers  # This registers command handlers using `bot`

# Main async runner
async def main():
    await bot.start()
    print("[✅] Bot started successfully.")

    # Launch the scheduler to auto-post daily
    asyncio.create_task(daily_post_scheduler(bot))

    await idle()  # Keeps the bot alive

if __name__ == "__main__":
    asyncio.run(main())
