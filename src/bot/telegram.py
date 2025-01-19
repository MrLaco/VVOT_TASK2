import os
from itertools import batched

import requests


class Telegram:
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.environ["TG_BOT_KEY"]}"

    def send_message(self, reply_text, message):
        url = f"{self.TELEGRAM_API_URL}/sendMessage"

        payload = {
            "chat_id": message["chat"]["id"],
            "text": reply_text,
            "reply_parameters": {
                "message_id": message["message_id"],
            },
        }

        requests.post(url=url, json=payload)

    def send_photo(self, photo_url, message):
        url = f"{self.TELEGRAM_API_URL}/sendPhoto"

        payload = {
            "chat_id": message["chat"]["id"],
            "photo": photo_url,
            "reply_parameters": {
                "message_id": message["message_id"],
            },
        }

        response = requests.post(url=url, json=payload)
        return response.json()["result"]["photo"][-1]["file_unique_id"]

    def send_media_group(self, media_urls, message):
        if len(media_urls) == 1:
            return self.send_photo(media_urls[0], message)

        url = f"{self.TELEGRAM_API_URL}/sendMediaGroup"

        payload = {
            "chat_id": message["chat"]["id"],
            "reply_parameters": {
                "message_id": message["message_id"],
            },
        }

        for group in batched(media_urls, 10):
            payload["media"] = [{"type": "photo", "media": media_url} for media_url in group]
            requests.post(url=url, json=payload)
