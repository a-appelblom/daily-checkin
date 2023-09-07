import os
import datetime
import requests
from fastapi import FastAPI

from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_ID")

app = FastAPI()

@app.post('/__space/v0/actions')
def actions(request: dict):
    client = WebClient(token=TOKEN)

    date = str(datetime.date.today())
    date = date.split("-")
    api_url = 'https://api.quotable.io/quotes/random'
    data = requests.get(api_url)
    data = data.json()[0]
    myString = f"\n\n {data['content']} \n\n - {data['author']}"

    message = f"{date[2]}/{date[1]} - {date[0]} \n\n"
    message += myString
    data = request
    event = data['event']
    if event['id'] == 'send-message':
        client.chat_postMessage(channel=CHANNEL, text=message)





if __name__ == '__main__':
    actions({
        "event": {
            "id": "send-message",
            "trigger": "schedule"
        }
    })
