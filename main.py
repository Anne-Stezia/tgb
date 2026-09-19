from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent
import os
import telebot

bot = telebot.TeleBot(os.environ["TG_KEY"])

client = TikTokLiveClient(
    unique_id=os.environ["TT_ID"]
)


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    bot.send_message(
        os.environ["TT_CHANNEL"],
        "🚨 AnneStezia зараз стрімить"
    )


if __name__ == "__main__":
    client.run()
