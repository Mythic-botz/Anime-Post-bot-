import json
from datetime import datetime

def generate_daily_post():
    with open("daily.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    date_str = datetime.now().strftime("%d %B %Y")
    post_lines = [f"📅 **{date_str} Anime Release Guide**\n"]

    for anime in data.get("animes", []):
        title = anime.get("title", "Unknown")
        ep = anime.get("episode", "?")
        time = anime.get("time", "??:??")
        platform = anime.get("platform", "Unknown")
        tags = anime.get("tags", "")
        post_lines.append(f"🆕 **{title}** - Ep {ep}\n🕒 {time} | 📺 {platform}\n{tags}\n")

    return "\n".join(post_lines)
