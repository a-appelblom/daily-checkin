import os
import datetime

from deta import app
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_ID")

client = WebClient(token=TOKEN)

date = str(datetime.date.today())
date = date.split("-")

message = f"{date[2]}/{date[1]} - {date[0]}"

client.chat_postMessage(channel=CHANNEL, text=message)


@app.lib.crono()
def app(event):
    client.chat_postMessage(channel=CHANNEL, text=message)
