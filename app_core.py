from __future__ import unicode_literals
import os
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.tz import tzlocal
from flask import Flask, request, abort
from github import Github
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .utilitylib.time_handler import timezone_handler, get_stock_date_handler

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

date = timezone_handler(datetime.today(), 'CST')

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
    get_stock_date = get_stock_date_handler(date)
    g = Github(os.environ.get('GITHUB_TOKEN'))
    repository = g.get_user().get_repo('StockSelector-Storage')
    stock_data = repository.get_contents('stock_recommendation/{}.txt'.format(get_stock_date)).decoded_content.decode()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='{}\n股神小新的通靈選股\n'.format(get_stock_date) + stock_data)
    )


if __name__ == "__main__":
    app.run()