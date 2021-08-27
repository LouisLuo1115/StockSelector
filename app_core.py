from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('2b5XK6oJrGdqoSTVcNC5tY/8jE35CPiMwQbGemOw4uLeRIZsQWi9De9yOiaabKdtjiPmWatSl9RDS5JGMCw4GU0gadLRYMbwaBqbeMQmotbVO+xBm9kaKGNbDqy0HzNu7paW1y0KiW0uTUap0Fi+iQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c55fa76148e4d738e635cbe24f898d91')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def stock_recommendation(event):
    with open('./data/topn_stock_data/20210827.txt', 'r') as f:
        stock_data = f.read()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='股神小新今天的通靈選股\n' + stock_data)
    )

if __name__ == "__main__":
    app.run()