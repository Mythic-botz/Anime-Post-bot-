# bot.py

import asyncio
from pyrogram import Client
from utils import load_config
from scheduler import daily_post_scheduler
import handlers  # make sure this file uses `app`, not `bot`
from aiohttp import web

config = load_config()

app = Client(
    "anime-bot",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    bot_token=config["bot_token"]
)

# --- Dummy HTTP server to satisfy Render ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app_web = web.Application()
    app_web.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    await site.start()
    print("🌐 Web server started on port", os.environ.get("PORT", 10000))

# --- Main bot startup ---
async def main():
    await app.start()
    print("✅ Bot started using long polling")
    asyncio.create_task(daily_post_scheduler(app))
    asyncio.create_task(start_web_server())
    await app.idle()
# Expose app for import
    bot = app


if __name__ == "__main__":
    import os
    asyncio.run(main())
