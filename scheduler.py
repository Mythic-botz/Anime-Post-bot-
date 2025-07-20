# scheduler.py
import asyncio
from datetime import datetime
from pyrogram import Client
from utils import load_config, load_schedule, format_schedule

async def daily_post_scheduler(bot: Client):
    while True:
        now = datetime.now().strftime("%H:%M")
        config = load_config()

        if now == config["post_time"]:
            print(f"[+] Posting scheduled anime updates at {now}")

            try:
                schedule = load_schedule()
                message = format_schedule(schedule)
                await bot.send_message(config["channel_id"], message)
                print("[+] Posted successfully!")

            except Exception as e:
                print(f"[!] Failed to post: {e}")

            await asyncio.sleep(61)  # Wait a bit longer after posting
        else:
            await asyncio.sleep(20)  # Check every 20 seconds
