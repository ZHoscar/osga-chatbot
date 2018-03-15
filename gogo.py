
import urllib3
from googletrans import Translator
from bs4 import BeautifulSoup



from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *



app = Flask(__name__)

line_bot_api = LineBotApi('Qn7SS4hSK8gTwFUwpqJzCX9s/BuowQh3cgJrQ44KWgtbwttZGawrvyPjz75iaiAdgV94mVwrqfMUmtiQsVaFpB6T+yoRY9aAwG+L4JcP3lfbVgzcRHM5K5C7jTsCRV+Zw9cNV1dBL2bZkFJlRzFBFwdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('0b09c163f73558e065ccb5a6a24e057d')


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

    if event.message.text == "image":
        buttons_template = TemplateSendMessage(
            alt_text = 'image template',
            template = ButtonsTemplate(
                title = 'Title 1 ',
                text  = 'Text 1',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                           MessageTemplateAction(
                           label = 'first label', text = 'label1'),
                           MessageTemplateAction(
                           label = 'second label', text = 'label2')
                           ]
                )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0



    if event.message.text.find("//")>= 0:
        translator = Translator()
        trans = translator.translate(event.message.text[2:], dest='zh-TW')
        line_bot_api.reply_message(
                                   event.reply_token,  TextSendMessage(text=trans.text))
        return 0

    if event.message.text.find("\\") >= 0:
        translator = Translator()
        trans = translator.translate(event.message.text[2:])
        

        line_bot_api.reply_message(
                                   event.reply_token, TextSendMessage(text=trans.text))
        return 0
    if event.message.text.find("\/") >= 0:
        translator = Translator()
        trans = translator.translate(event.message.text[4:], dest='ja')


        line_bot_api.reply_message(
                                    event.reply_token, TextSendMessage(text=trans.text)
        )
        return 0

    elif event.message.text == "Carousel template":
        Carousel_template = TemplateSendMessage(
          alt_text='Carousel template',
          template=CarouselTemplate(
            columns=[
              CarouselColumn(
                thumbnail_image_url='https://a.ecimg.tw/items/DCABCTA90057H2O/000002_1478321440.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                  PostbackTemplateAction(
                    label='postback1',
                    text='postback text1',
                    data='action=buy&itemid=1'
                                        ),
                  MessageTemplateAction(
                    label='message1',
                    text='message text1'
                                        ),
                  URITemplateAction(
                    label='uri1',
                    uri='http://example.com/1'
                                   )
                        ]
                           ),
             CarouselColumn(
               thumbnail_image_url='https://a.ecimg.tw/items/DCABCTA90057H2O/000002_1478321440.jpg',
               title='this is menu2',
               text='description2',
               actions=[
                 PostbackTemplateAction(
                   label='postback2',
                   text='postback text2',
                   data='action=buy&itemid=2'
                                       ),
                MessageTemplateAction(
                  label='message2',
                  text='message text2'
                                     ),
               URITemplateAction(
                  label='連結2',
                  uri='http://example.com/2'
                                )
                      ]
                         )
                      ]
              )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        return 0








if __name__ == "__main__":
    app.run()





