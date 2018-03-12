
import urllib3
from bs4 import BeautifulSoup


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


### class definition ###
"""
    class for BBC_NEWS
"""







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


def BBC_News():

    url = 'www.bbc.com/news'

    http = urllib3.PoolManager()
    response = http.request('GET', url)

    soup = BeautifulSoup(request.data,"html.parser")



    AllTitles = soup.find_al('a', class_="gs-c-promo-heading nw-o-link-split__anchor gs-o-faux-block-link__overlay-link gel-pica-bold", limit = 10)

    AllParahs = [0] * len(AllTitles)

    for num in range(len(AllTitles)):

        if (AllTitles[num].find_next("p")!="0"):
            AllParahs[num] = AllTitles[num].find_next("p")
            AllTitles[num] = AllTitles[num].text.strip()
            AllParahs[num] = AllParahs[num].text.strip()


    for num in range(len(AllTitles)):
        Content = AllTitles[num] + "\n" + AllParahs[num] + "\n"

    return Content










@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "echo":
        line_bot_api.reply_message(
                                   event.reply_token,
                                   TextSendMessage(text=event.message.text))


    if event.message.text == "BBC":
        content = BBC_News()
        line_bot_api.reply_message(
                                   event.reply_token,
                                   TextSendMessage(text=content))






if __name__ == "__main__":
    app.run()





