
import urllib3
from googletrans import Translator
from bs4 import BeautifulSoup
import copy
from urllib.parse import quote
import random

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



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


class Product_T:
    product_name = ""
    product_image_url = ""
    product_price = ""
    product_url=""
    product_seller=""
    product_seller_url=""


def Rakuten(search_name):
    
    
    Product = Product_T()
    
    search_name = quote(search_name)
    url = 'https://www.rakuten.com.tw/search/' + search_name
    
    http = urllib3.PoolManager()
    
    response = http.request('GET', url)
    
    soup = BeautifulSoup(response.data, "html.parser")
    
    temp_soup = soup.find_all('div', class_='b-mod-item-vertical products-grid-section', limit = 5)
    
    ListOfProduct = []
    
    for n in range(len(temp_soup)):
        
        temp_name = temp_soup[n].find_next('img')
        temp_price = temp_soup[n].find_next('span', class_="b-text-prime")
        temp_url = temp_soup[n].find_next('a')
        temp_seller = temp_soup[n].find_next('a', class_="product-shop")
        
        Product.product_seller = temp_seller.text.strip()
        Product.product_seller_url = temp_seller['href']
        
        Product.product_name = temp_name["alt"]
        Product.product_url = 'https://www.rakuten.com.tw'+ temp_url['href']
        Product.product_image_url = temp_name["data-src"]
        Product.product_price = temp_price.text.strip()
        
        ListOfProduct.append(copy.copy(Product))
    
    
    return ListOfProduct






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
    if event.message.text.find("()jp") >= 0:
        translator = Translator()
        trans = translator.translate(event.message.text[4:], dest='ja')


        line_bot_api.reply_message(
                                    event.reply_token, TextSendMessage(text=trans.text)
        )
        return 0

    elif event.message.text.find("我要買") >= 0:
        User_Product = Product_T()
        User_Product = Rakuten(event.message.text[3:])


        Carousel_template = TemplateSendMessage(
          alt_text='Carousel Template',
          template=CarouselTemplate(
            columns=[
              CarouselColumn(
                thumbnail_image_url=User_Product[0].product_image_url,
                title=User_Product[0].product_name[:39],
                text='商品價格： ' + User_Product[0].product_price,
                             
                actions=[
                  URITemplateAction(
                    label='商品：' + event.message.text[3:],
                    uri = User_Product[0].product_url
                                        ),
                  URITemplateAction(
                    label='商品賣家： ' + User_Product[0].product_seller[:9],
                    uri=User_Product[0].product_seller_url
                                        ),
                  URITemplateAction(
                    label='比價此商品',
                    uri='http://feebee.com.tw'
                                   )
                        ]
                           ),
             CarouselColumn(
               thumbnail_image_url=User_Product[1].product_image_url,
               title=User_Product[1].product_name[:39],
               text='商品價格： ' + User_Product[1].product_price,
               actions=[
                 URITemplateAction(
                   label='商品： '+ event.message.text[3:],
                   uri = User_Product[1].product_url
                                       ),
                 URITemplateAction(
                  label='商品賣家： ' + User_Product[1].product_seller[:9],
                  uri=User_Product[1].product_seller_url
                                     ),
                 URITemplateAction(
                  label='比價此商品',
                  uri='http://feebee.com.tw')]),
             
            CarouselColumn(
              thumbnail_image_url=User_Product[2].product_image_url,
              title=User_Product[2].product_name[:39],
              text='商品價格： ' + User_Product[2].product_price,
              actions=[
              URITemplateAction(
                    label='商品： ' + event.message.text[3:],
                    uri = User_Product[2].product_url
                                    ),
              URITemplateAction(
                    label='商品賣家： ' + User_Product[2].product_seller[:9],
                    uri=User_Product[2].product_seller_url
                                    ),
              URITemplateAction(
                    label='比價此商品',
                    uri='http://feebee.com.tw')]),
            
                     
           CarouselColumn(
             thumbnail_image_url=User_Product[3].product_image_url,
             title=User_Product[3].product_name[:39],
             text='商品價格： ' + User_Product[3].product_price,
             actions=[
               URITemplateAction(
                    label='商品： ' + event.message.text[3:],
                    uri = User_Product[3].product_url
                                     ),
               URITemplateAction(
                    label='商品賣家： ' + User_Product[3].product_seller[:9],
                    uri=User_Product[3].product_seller_url
                                ),
               URITemplateAction(
                    label='比價此商品',
                    uri='http://feebee.com.tw')]),
                     
              
                     
           CarouselColumn(
             thumbnail_image_url=User_Product[4].product_image_url,
             title=User_Product[4].product_name[:39],
             text='商品價格： ' + User_Product[4].product_price,
             actions=[
             URITemplateAction(
                label='商品： ' + event.message.text[3:],
                uri = User_Product[4].product_url
                                  ),
             URITemplateAction(
                label='商品賣家： ' + User_Product[4].product_seller[:9],
                uri=User_Product[4].product_seller_url
                               ),
             URITemplateAction(
                label='比價此商品',
                uri='http://feebee.com.tw')])
                 
              ]
           )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        return 0

    if event.message.text == "are you ok":
        a = random.randint(0,1)
        if a == 0 :
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "i am ok"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "i am not ok"))










if __name__ == "__main__":
    app.run()





