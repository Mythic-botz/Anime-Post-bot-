# bot.py
from pyrogram import Client
from utils import load_config
from scheduler import daily_post_scheduler
import asyncio

# Load config from JSON
config = load_config()

# Create bot client
bot = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

# Import handlers AFTER bot is defined
import handlers  # this will register all command handlers

# Function to launch bot and scheduler
async def start_bot():
    await bot.start()
    print("[✅] Bot started.")

    # Start the scheduler task
    asyncio.create_task(daily_post_scheduler(bot))

    # Keep the bot running
    await bot.idle()

# Run the bot
if __name__ == "__main__":
    asyncio.run(start_bot())
