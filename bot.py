# bot.py

import asyncio
import os
from pyrogram import Client
from aiohttp import web
from utils import load_config
from scheduler import daily_post_scheduler
from handlers import setup_handlers

# ✅ Load config
config = load_config()

# ✅ Initialize bot client
bot = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

# ✅ Setup all command handlers
setup_handlers(bot)

# 🌐 Dummy web server to keep Render happy
async def handle(request):
    return web.Response(text="✅ Anime Post Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    await site.start()
    print(f"🌍 Web server running on port {os.environ.get('PORT', 10000)}")

# ✅ Main bot startup
async def start():
    await bot.start()
    print("✅ Bot started with long polling")

    asyncio.create_task(daily_post_scheduler(bot))
    asyncio.create_task(start_web_server())

    await bot.stop()  # ends after long polling unless .idle() is replaced
    print("🛑 Bot stopped.")

if __name__ == "__main__":
    asyncio.run(start())
