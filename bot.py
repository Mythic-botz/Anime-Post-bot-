# bot.py

import asyncio
import os
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

setup_handlers(bot)  # ⬅️ register handlers here

# 🌐 Dummy web server for Render
async def handle(request):
    return web.Response(text="✅ Anime Post Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    await site.start()
    print(f"🌍 Web server running on port {os.environ.get('PORT', 10000)}")

# ✅ Run everything together
async def main():
    await start_web_server()                      # start dummy server
    asyncio.create_task(daily_post_scheduler(bot))  # schedule posts
    await bot.run()  # ✅ this keeps the bot alive

if __name__ == "__main__":
    asyncio.run(main())
