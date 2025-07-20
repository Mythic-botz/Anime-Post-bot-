# bot.py
import asyncio
from pyrogram import Client
from utils import load_config
from scheduler import daily_post_scheduler
import handlers  # this imports command handlers

config = load_config()

app = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

@app.on_message()
async def dummy_handler(client, message):
    pass  # placeholder for Pyrogram to keep running

async def main():
    await app.start()
    print("[✅] Bot started successfully.")

    # Start the scheduler task
    asyncio.create_task(daily_post_scheduler(app))

    await idle()  # keep the bot running

if __name__ == "__main__":
    from pyrogram.idle import idle
    asyncio.run(main())
