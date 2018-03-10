


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('NzpVlTGjg4wfT44M65VszunYhzzZvKB8k+Oa+poBnOvYE2ru7xlfCqvglxYs0kdcgV94mVwrqfMUmtiQsVaFpB6T+yoRY9aAwG+L4JcP3le18oKC/NTXa5vSUuUfFtTYrESrlr7VhJsxdxzEf9IOpgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bf25eefb7a251e8eae394aeca428a626')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text) + "good")


if __name__ == "__main__":
    app.run()
