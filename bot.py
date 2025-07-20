# bot.py

import os
import asyncio
from pyrogram import Client
from aiohttp import web
from utils import load_config
from scheduler import daily_post_scheduler
from handlers import setup_handlers

config = load_config()

bot = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

# 🌐 Dummy Web Server for Render
async def handle(request):
    return web.Response(text="✅ Anime Post Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    await site.start()
    print(f"🌍 Web server running on port {os.environ.get('PORT', 8000)}")

# ✅ Schedule daily post before bot.run()
async def setup_and_run():
    await start_web_server()
    setup_handlers(bot)
    asyncio.create_task(daily_post_scheduler(bot))  # Background scheduler

    bot.run()  # ✅ Do not await this

# 🚀 Start the bot
if __name__ == "__main__":
    try:
        asyncio.run(setup_and_run())
    except RuntimeError as e:
        # 💥 This happens if event loop is already running (Render edge case)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(setup_and_run())
