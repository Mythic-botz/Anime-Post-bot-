# 🤖 Anime Auto Poster Bot

A FastAPI + Pyrogram-based Telegram bot that auto-posts daily anime episode updates to a Telegram channel. You can manually trigger posts or update the anime schedule using a simple JSON file.

---

## ✨ Features

- 🕘 **Auto Post** daily anime list at 9 PM JST (12:00 UTC).
- ✍️ **Editable** post content via a JSON file.
- 📤 **Manual Posting** with `/post` command.
- 📁 **JSON Update** via `/update` (reply to a .json file).
- ⚙️ **Webhook-Based** FastAPI server (Render-compatible).
- 🔒 **Private Command Handling** for safety.

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/anime-auto-poster-bot.git
cd anime-auto-poster-bot

2. Install dependencies

pip install -r requirements.txt

3. Create .env file

Create a .env file in the root directory with the following:

API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://your-render-url.onrender.com
CHANNEL_ID=-100xxxxxxxxxx

> 📝 Get API_ID and API_HASH from my.telegram.org.




---

🚀 Run Locally

uvicorn main:app --host 0.0.0.0 --port 8000

Then set your webhook manually:

https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-render-url.onrender.com/webhook


---

☁️ Deploy to Render

1. Go to render.com


2. Create a new Web Service


3. Connect to your GitHub repo


4. Set the start command to:



uvicorn main:app --host 0.0.0.0 --port 8000

5. Add environment variables from .env


6. Deploy!




---

🔧 Bot Commands


---

📁 JSON Structure (daily.json)

{
  "animes": [
    {
      "title": "Attack on Titan",
      "episode": "8",
      "time": "21:00 JST",
      "platform": "Crunchyroll",
      "tags": "#AttackOnTitan #ShingekiNoKyojin"
    }
  ]
}

Update it daily by replying to /update with the new file.


---

💬 Credits

Made with 💖 using Pyrogram and FastAPI
Built by @YourUsername


---
