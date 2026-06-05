import requests
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

API_URL = "https://kick.com/api/v2/channels/kickzafer"

LIVE_ID_FILE = "live_id.txt"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

livestream = data.get("livestream")

if not livestream:
    print("Yayın açık değil.")
    exit()

live_id = str(livestream["id"])

old_id = ""

if os.path.exists(LIVE_ID_FILE):
    with open(LIVE_ID_FILE, "r", encoding="utf-8") as f:
        old_id = f.read().strip()

if old_id == live_id:
    print("Bildirim zaten gönderilmiş.")
    exit()

title = livestream.get("session_title", "Yayın Başladı")
viewer_count = livestream.get("viewer_count", 0)

category = "Bilinmiyor"
if livestream.get("categories"):
    category = livestream["categories"][0]["name"]

profile_pic = data.get("user", {}).get("profile_pic")

banner = None
if data.get("banner_image"):
    banner = data["banner_image"].get("url")

embed = {
    "title": "🔴 YAYIN BAŞLADI",
    "description": (
        f"👑 **kickzafer**\n\n"
        f"📝 **{title}**\n\n"
        f"🎮 **{category}**\n"
        f"👀 **{viewer_count} izleyici**\n\n"
        f"⚡ **Yayına Gel**\n"
        f"https://kick.com/kickzafer"
    ),
    "color": 65280,
    "footer": {
        "text": "Kick Yayın Bildirimi"
    }
}

if profile_pic:
    embed["thumbnail"] = {
        "url": profile_pic
    }

if banner:
    embed["image"] = {
        "url": banner
    }

payload = {
    "content": "@everyone",
    "embeds": [embed]
}

r = requests.post(WEBHOOK_URL, json=payload, timeout=30)

print("Discord Durum Kodu:", r.status_code)

with open(LIVE_ID_FILE, "w", encoding="utf-8") as f:
    f.write(live_id)

print("Yayın bildirimi gönderildi.")
