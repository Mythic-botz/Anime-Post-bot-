# main.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
from bot.post import post_anime

# 🔧 Create bot client
bot = Client(
    "AnimeAutoPosterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 👋 Handle /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello Otaku!\n\nI'm your Anime Auto Poster Bot.\nUse /post to post a new anime episode!"
    )

# 🎬 Handle /post command
@bot.on_message(filters.command("post") & filters.private)
async def handle_post(client: Client, message: Message):
    await post_anime(client, message)

# ▶️ Run the bot
if __name__ == "__main__":
    bot.run()
