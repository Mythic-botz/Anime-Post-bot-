import os
import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

# In-memory dict to store user states
user_steps = {}
anime_draft = {}

bot = Client(
    "anime_post_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# 📌 /start
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 Welcome to the Anime Post Bot!\n"
        "Use /addanime to add a new anime to the schedule."
    )

# ℹ️ /about
@bot.on_message(filters.command("about") & filters.private)
async def about_handler(client, message: Message):
    await message.reply_text(
        "**Anime Post Bot Info**\n\n"
        "➤ Add anime: /addanime\n"
        "➤ View today’s releases: /schedule\n"
        "➤ View full schedule: (coming soon)\n\n"
        "Built with ❤️ using Pyrogram.",
        parse_mode=ParseMode.MARKDOWN
    )

# 📅 /schedule
@bot.on_message(filters.command("schedule") & filters.private)
async def schedule_handler(client, message: Message):
    if not os.path.exists("anime_schedule.json"):
        return await message.reply_text("⚠️ No schedule found.")

    try:
        with open("anime_schedule.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        today = datetime.now().strftime("%Y-%m-%d")
        releases = [
            anime for anime in data.get("schedule", [])
            if anime.get("date") == today
        ]

        if not releases:
            return await message.reply_text("📭 No anime releases today.")

        text = f"📅 **Anime Releases for {today}:**\n\n"
        for anime in releases:
            text += f"• **{anime['title']}** - Ep {anime['episode']} at {anime['time']} on {anime['platform']}\n"

        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply_text(f"❌ Error reading schedule: {e}")

# 🆕 /addanime (step-by-step conversation)
@bot.on_message(filters.command("addanime") & filters.private)
async def addanime_handler(client, message: Message):
    user_id = message.from_user.id
    user_steps[user_id] = "title"
    anime_draft[user_id] = {}
    await message.reply_text("📌 Send the anime title:")

# 🔁 Handle step-by-step input
@bot.on_message(filters.text & filters.private)
async def conversation_handler(client, message: Message):
    user_id = message.from_user.id
    step = user_steps.get(user_id)

    if not step:
        return

    text = message.text.strip()

    if step == "title":
        anime_draft[user_id]["title"] = text
        user_steps[user_id] = "episode"
        await message.reply_text("🎞 Send the episode number:")
    
    elif step == "episode":
        anime_draft[user_id]["episode"] = text
        user_steps[user_id] = "date"
        await message.reply_text("📅 Send the date (YYYY-MM-DD):")
    
    elif step == "date":
        anime_draft[user_id]["date"] = text
        user_steps[user_id] = "time"
        await message.reply_text("⏰ Send the time (HH:MM):")
    
    elif step == "time":
        anime_draft[user_id]["time"] = text
        user_steps[user_id] = "platform"
        await message.reply_text("📺 Send the platform name:")
    
    elif step == "platform":
        anime_draft[user_id]["platform"] = text

        # Save to JSON file
        schedule = []
        if os.path.exists("anime_schedule.json"):
            with open("anime_schedule.json", "r", encoding="utf-8") as f:
                try:
                    schedule = json.load(f).get("schedule", [])
                except:
                    pass

        schedule.append(anime_draft[user_id])
        with open("anime_schedule.json", "w", encoding="utf-8") as f:
            json.dump({"schedule": schedule}, f, indent=4)

        # Clear state
        user_steps.pop(user_id)
        anime_draft.pop(user_id)

        await message.reply_text("✅ Anime successfully added to schedule!")