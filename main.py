from pyrogram import Client
from pyrogram.handlers import CommandHandler
from config import API_ID, API_HASH, BOT_TOKEN
from bot.post import post_anime
from pyrogram.types import Message

bot = Client(
    "AnimeAutoPosterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(CommandHandler("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello Otaku!\n\nI'm your Anime Auto Poster Bot.\nUse /post to post a new anime episode!"
    )

bot.add_handler(CommandHandler("post", post_anime))

if __name__ == "__main__":
    bot.run()
