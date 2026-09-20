import asyncio
import os
from pathlib import Path

import telebot
from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError


STATE_FILE = Path("last_room_id.txt")


async def main():
    client = TikTokLiveClient(unique_id=os.environ["TT_ID"])

    try:
        room_id = str(
            await client.web.fetch_room_id_from_html(client.unique_id)
        )
    except UserOfflineError:
        print("TikTok user is offline")
        return

    print(f"TikTok user is LIVE. Room ID: {room_id}")

    # Читаем ID стрима, о котором уже уведомляли
    last_room_id = (
        STATE_FILE.read_text().strip()
        if STATE_FILE.exists()
        else None
    )

    if room_id == last_room_id:
        print("Already notified about this stream")
        return

    # Новый стрим
    bot = telebot.TeleBot(os.environ["TG_KEY"])

    bot.send_message(
        os.environ["TT_CHANNEL"],
        "🚨 AnneStezia зараз стрімить"
    )

    # Записываем state только ПОСЛЕ успешной отправки Telegram
    STATE_FILE.write_text(room_id)

    print("Telegram notification sent")
    print(f"Saved new Room ID: {room_id}")


if __name__ == "__main__":
    asyncio.run(main())
