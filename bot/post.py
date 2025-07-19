# bot/post.py
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_ID, WATERMARK

async def post_anime(client: Client, message: Message):
    try:
        # Split the command message to extract content
        content = message.text.split(" ", 1)[1]
    except IndexError:
        await message.reply_text("⚠️ Usage: `/post Anime Name EpXX | [Watch Link] [Download Link]`", quote=True)
        return

    try:
        caption_part, link_part = content.split("|", 1)
        caption = caption_part.strip()
        links = link_part.strip().split(" ")

        watch_link = links[0] if len(links) > 0 else "#"
        download_link = links[1] if len(links) > 1 else "#"

        final_caption = f"🎬 **{caption}**\n\n🚀 Posted by: {WATERMARK}"

        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("▶️ Watch", url=watch_link),
                InlineKeyboardButton("⬇️ Download", url=download_link)
            ]]
        )

        await client.send_message(
            chat_id=CHANNEL_ID,
            text=final_caption,
            reply_markup=buttons
        )

        await message.reply_text("✅ Posted successfully to the channel!")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")
