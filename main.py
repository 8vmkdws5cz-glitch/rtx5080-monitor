import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://api.store.nvidia.com/partner/v1/feinventory?locale=fr-fr"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

notified = False

while True:
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()

        available = False

        for item in data.get("listMap", []):
            title = str(item.get("productTitle", ""))

            if "5080" in title and item.get("is_active") == "true":
                available = True
                break

        if available and not notified:
            send_message(
                "🚨 RTX 5080 Founders Edition появилась во Франции!"
            )
            notified = True

        if not available:
            notified = False

    except Exception as e:
        print(e)

    time.sleep(60)
