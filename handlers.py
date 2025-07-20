# handlers.py

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils import save_config, load_config, save_schedule, load_schedule
import json
import os

# Add your Telegram user IDs here
ADMINS = [1234567890]  # 👈 Replace with your Telegram user ID


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# /start command
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text("👋 Hello! I’m your Anime Auto Poster Bot!\nUse /update, /channel, or /time to configure.")


# /channel command — set channel ID
@Client.on_message(filters.command("channel") & filters.private)
async def set_channel(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("🚫 You're not allowed to do this.")

    if len(message.command) != 2:
        return await message.reply_text("⚠️ Usage: `/channel -100xxxxxxxxxx`", quote=True)

    new_id = message.command[1]
    config = load_config()
    config["channel_id"] = new_id
    save_config(config)
    await message.reply_text(f"✅ Channel ID updated to `{new_id}`")


# /time command — set daily post time
@Client.on_message(filters.command("time") & filters.private)
async def set_time(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("🚫 You're not allowed to do this.")

    if len(message.command) != 2:
        return await message.reply_text("⚠️ Usage: `/time HH:MM` (24hr format)", quote=True)

    post_time = message.command[1]
    config = load_config()
    config["post_time"] = post_time
    save_config(config)
    await message.reply_text(f"✅ Daily post time updated to `{post_time}`")


# /update command — update anime_schedule.json via replied JSON file
@Client.on_message(filters.command("update") & filters.private)
async def update_schedule(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("🚫 You're not allowed to do this.")

    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("⚠️ Please reply to a `.json` file.")

    doc = message.reply_to_message.document

    if not doc.file_name.endswith(".json"):
        return await message.reply_text("❌ Invalid file type. Please send a .json file.")

    try:
        await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        file_path = await doc.download(file_name="./anime_schedule.json")
        with open(file_path, "r") as f:
            schedule = json.load(f)
            save_schedule(schedule)

        await message.reply_text("✅ Anime schedule updated successfully!")

    except Exception as e:
        await message.reply_text(f"❌ Update failed: `{e}`")


# /showtime — show current config
@Client.on_message(filters.command("showtime") & filters.private)
async def show_config(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("🚫 You're not allowed to do this.")

    config = load_config()
    schedule = load_schedule()
    weekdays = "\n".join(f"📅 {day}: {len(episodes)} releases" for day, episodes in schedule.items())
    
    msg = f"🛠️ Current Config:\n\n🆔 Channel: `{config['channel_id']}`\n⏰ Post Time: `{config['post_time']}`\n\n{weekdays}"
    await message.reply_text(msg)
