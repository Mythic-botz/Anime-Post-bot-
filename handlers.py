# handlers.py
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils import load_config, load_schedule
import json

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("👋 Welcome to the Anime Post Bot!\nUse /update to upload a new schedule.")

@bot.on_message(filters.command("channel") & filters.private)
async def set_channel(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: /channel <channel_id>")

    new_id = message.command[1]
    try:
        config = load_config()
        config["channel_id"] = new_id
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        await message.reply_text(f"✅ Channel ID updated to `{new_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@bot.on_message(filters.command("update") & filters.private)
async def update_json(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("⚠️ Please reply to a JSON file.")

    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".json"):
        return await message.reply_text("❌ Only .json files are supported.")

    try:
        await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        await doc.download(file_name="anime_schedule.json")
        await message.reply_text("✅ Schedule updated successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to update: {e}")
