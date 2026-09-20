import asyncio
import os
from pathlib import Path

import telebot
from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError, UserNotFoundError


STATE_FILE = Path("last_room_id.txt")


async def main():
    client = TikTokLiveClient(unique_id=os.environ["TT_ID"])

    try:
        await client.start()

        room_id = str(client.room_id)

        print(f"TikTok user is LIVE. Room ID: {room_id}")

        last_room_id = (
            STATE_FILE.read_text().strip()
            if STATE_FILE.exists()
            else None
        )

        print(f"Last notified Room ID: {last_room_id}")

        if room_id == last_room_id:
            print("Already notified about this stream")
            return

        bot = telebot.TeleBot(os.environ["TG_KEY"])

        bot.send_message(
            os.environ["TT_CHANNEL"],
            "🚨 AnneStezia зараз стрімить"
        )

        STATE_FILE.write_text(room_id)

        print("Telegram notification sent")
        print(f"Saved new Room ID: {room_id}")

    except (UserOfflineError, UserNotFoundError) as e:
        print(
            f"TikTok LIVE is not available: "
            f"{type(e).__name__}"
        )

    finally:
        if client.connected:
            print("Disconnecting from TikTok...")
            await client.disconnect(close_client=True)


if __name__ == "__main__":
    asyncio.run(main())
