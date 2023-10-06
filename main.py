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
    quote_api_url = 'https://api.quotable.io/quotes/random'
    quote_data = requests.get(quote_api_url)
    quote_data = quote_data.json()[0]
    my_quote_string = f"{quote_data['content']} \n\n - {quote_data['author']} \n\n"

    question_api_url = "https://poopoo-api.vercel.app/api/qotd"
    question_data = requests.get(question_api_url)
    question_data = question_data.json()
    question = question_data['question']
    question_string = f"Question of the day: \n {question}"

    message = f"{date[2]}/{date[1]} - {date[0]} \n\n"
    message += my_quote_string
    message += question_string
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
