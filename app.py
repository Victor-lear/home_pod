import json
import sys
import requests
# Import blinka python modules.
import board
import digitalio
import RPi.GPIO as GPIO  # 引入 RPi.GPIO 库
import time
import socket
from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from dotenv import load_dotenv
ENV = './.env' 
load_dotenv(dotenv_path=ENV)
app = Flask(__name__)

# --- 請在此填入你的憑證 ---
# 從 LINE Developers Console 取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') 
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET') 

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    # 這是第一道關卡：看有沒有收到資料
    print("--- 收到 Webhook 請求 ---", flush=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("!!! 簽章驗證失敗 !!!", flush=True)
        abort(400)
    except Exception as e:
        print(f"!!! 發生錯誤: {e} !!!", flush=True)
        abort(500)

    return 'OK'

# 這是第二道關卡：注意參數的寫法
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print(">>> 進入了 handle_message 函式 <<<", flush=True)
    
    user_id = event.source.user_id
    # v3 版獲取文字的方式
    user_text = event.message.text
    
    with open("member.json", "r", encoding="utf-8") as f:
        member = json.load(f)

    if (user_text=="addmember") :
        if (user_id not in member['member']):
            member['member'].append(user_id)
            with open("member.json", "w", encoding="utf-8") as f:
                json.dump(member, f, indent=4, ensure_ascii=False)
    else:
        if user_id in member['member']:
            if user_text=='openair':
                try:
                    import gpio
                    gpio.click()
                except:
                    pass
            if user_text=='openlight':
                try:
                    import gpio
                    gpio.socketsub()
                except:
                    pass
if __name__ == "__main__":
    # Flask 預設跑在 5000 埠
    app.run(port=5000)