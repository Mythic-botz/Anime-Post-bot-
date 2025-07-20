# bot/utils.py

from datetime import datetime
import pytz
from config import TIMEZONE

def get_today_date():
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz).strftime("%A – %B %d")  # Example: Sunday – July 21

def is_admin(user_id: int) -> bool:
    from config import ADMINS
    return user_id in ADMINS

def log_error(e: Exception):
    print(f"[ERROR] {type(e).__name__}: {e}")
# utils.py
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_schedule():
    with open("anime_schedule.json", "r") as f:
        return json.load(f)

def format_schedule(data):
    date = data.get("date", "📅 Unknown Date")
    title = data.get("title", "")
    entries = data.get("entries", [])

    lines = [
        "⟣━━━━━━━━━━━━━━━━━━━⟢",
        f"   {date}",
        f"  『 {title} 』",
        "⟣━━━━━━━━━━━━━━━━━━━⟢",
        ""
    ]

    for entry in entries:
        anime = entry.get("anime", "Unknown")
        ep = entry.get("episode", "")
        time = entry.get("time", "")
        platform = entry.get("platform", "")
        tags = entry.get("tags", "")

        block = (
            f"╭⛦⃕‌  {anime}\n"
            f"┃🎬 Episode: {ep} \n"
            f"┃🕒 Time: {time} \n"
            f"┃📺 Platform: {platform} \n"
            f"┃🏷️ {tags}\n"
            f"╰─────────────────────\n"
        )
        lines.append(block)

    lines.append("🔔 Daily Hindi Anime Updates")
    lines.append("📲 Follow 👉 @Hindi_Anime_News")
    lines.append("#Hindi_Anime_News #HindiDubbed #AnimeInHindi #Crunchyroll #MuseIndia #AnimeUpdate")

    return "\n".join(lines)
