import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask (__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['hDEXigBx3q22MD9N4c4k9h/7ql08sBMCUTAuhBAevphGCcbIJb65W0nik3BePY6w68ZBPb9dkjc/s+2znFz26qZrSiOSKCghglNRZJCnQe7NUHi+RGMIExGa0r+A3HGYMAVFZwctBTmuqyTyp2aDAAdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(condig['linebot']['bc1445fa31789d24b3cebe96a69b5010'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']


@app.route("/callback", methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


def pattern_mega(text):
    patterns = [
        'mega','mg', 'mu'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True



def digiroin():
    target_url = 'https://www.digiroin.com/forum/login'
    print('launching Digiroin in a second')
    rs = reqests.session()
    res = rs.get(traget_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        if pattern_mega(titleURL.text):
            title = titleURL.text
            if '11379780-1-1' in titleURL['href']:
                continue
            link = 'http://www.digiroin.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content


def apple_news():
    target_url = 'http://www.appledaily.com.tw/realtimenews/section/new'
    head = 'http://www.appledaily.com.tw'
    print('Start opening appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), o):
        if index == 15:
            return content
        if head in data['href']:
            link = data['href']
        else:
            link = head + data['href']
        content += '{}\n\n'.format(link)
    return content


def technews():
    target_url = 'https://technews.tw/'
    print('Start opening Technews...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.txt, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('article div h1. entry-title a')):
        if index == 12:
            return content
        title = data.text
        link - data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content


def gironews():
    target_url = 'https://www.giro.com/'
    print('Start opening gironews...')
    rs = requests.session()
    res = rs.get(traget_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.txt, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('article div h1. entry-title a')):
        if index == 12:
            return content
        title = data.text
        link - data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text", event.message.text)
    if event.message.text == "digiroin":
        content = digiroin()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "apple_news":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "technews":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "gironews":
        content = gironews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "giro":
        buttons_template = TemplateSendMessage(
            alt_text='this is about Giro',
            template=ButtonTemplate(
                title='This is info about Giro and Digiroin',
                text='this is about Giro and Digiroin',
                thumbnail_image_url='https://example.com/digiroin.jpg',
                actions=[
                    MessageTemplateAction(
                        label='More Info',
                        Text='More info about Giro please'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)



if __name__ == '__main__':
    app.run