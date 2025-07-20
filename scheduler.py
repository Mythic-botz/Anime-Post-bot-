# scheduler.py

import asyncio
from datetime import datetime
from pyrogram import Client
from utils import load_config, load_schedule, format_anime_post

last_posted_day = None  # To ensure only one post per day


async def start_scheduler(bot: Client):
    global last_posted_day

    while True:
        try:
            now = datetime.now()
            config = load_config()
            post_hour, post_minute = map(int, config["post_time"].split(":"))
            channel_id = config["channel_id"]

            if channel_id is None:
                await asyncio.sleep(30)
                continue

            if (now.hour == post_hour and now.minute == post_minute):
                weekday = now.strftime("%A")

                # Prevent reposting on same day
                if last_posted_day == weekday:
                    await asyncio.sleep(60)
                    continue

                schedule = load_schedule()
                today_schedule = schedule.get(weekday, [])

                if not today_schedule:
                    print(f"[{weekday}] No schedule found, skipping post.")
                else:
                    # Format message and send
                    caption = format_anime_post(weekday, now.strftime("%B %d"), today_schedule)
                    await bot.send_message(chat_id=channel_id, text=caption)

                    print(f"✅ Posted schedule for {weekday}")
                    last_posted_day = weekday

        except Exception as e:
            print(f"❌ Scheduler error: {e}")

        await asyncio.sleep(60)  # Check again in 1 minute
