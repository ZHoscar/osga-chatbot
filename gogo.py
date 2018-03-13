
import urllib3
import goslate
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




app = Flask(__name__)

line_bot_api = LineBotApi('I6zOR82ZAC1jQnRkhVnxFNFCi91+2JoAFhAM5LlrXngHWa3w6VTo1NS7hPzi7lN6gV94mVwrqfMUmtiQsVaFpB6T+yoRY9aAwG+L4JcP3ldYLO1SEIJMfDUJiApCmEpdyNn6ofW1XiADIxjRmX7ejAdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('306e5633e514f160f87e86453adb4b7d')


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

    soup = BeautifulSoup(response.data,"html.parser")
    


    AllTitles = soup.find_all('a', class_="gs-c-promo-heading nw-o-link-split__anchor gs-o-faux-block-link__overlay-link gel-pica-bold", limit = 10)

    AllParahs = [0] * len(AllTitles)

    for num in range(len(AllTitles)):

        if (AllTitles[num].find_next("p")!="0"):
            AllParahs[num] = AllTitles[num].find_next("p")
            AllTitles[num] = AllTitles[num].text.strip()
            AllParahs[num] = AllParahs[num].text.strip()
    Content = ""

    for num in range(len(AllTitles)):
        Content += "Head News:   " + AllTitles[num] + "\n""\t    " + AllParahs[num] + "\n""\n"

    return Content










@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "echo":
        line_bot_api.reply_message(
                                   event.reply_token,
                                   TextSendMessage(text=event.message.text))
        return 0


    if event.message.text == "BBC":
        content = BBC_News()
        line_bot_api.reply_message(
                                   event.reply_token,
                                   TextSendMessage(text=content))
        return 0

    else if "/" in event.message.text:
        gs = goslate.Goslate()
        
        line_bot_api.reply_message(
                                   event.reply_token,                                 TextSendMessage(text=gs.translate(event.message.text, 'zh')))
        return 0








if __name__ == "__main__":
    app.run()





