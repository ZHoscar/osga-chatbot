


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

line_bot_api = LineBotApi('M+/tC1AZwAbrFRMVHK1gcCwpOK6T/KtubM7yHvW6uBTMJHZTzjnmerh/b00LUUFBgV94mVwrqfMUmtiQsVaFpB6T+yoRY9aAwG+L4JcP3ld78aJ3f66h7p1vHrCpDCUe9z/aauWcb8rx7KRb3cCN7wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a6d0aa8b6ec9ec90d1d5b9db8bc28456')


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
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()