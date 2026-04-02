from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhooks import (MessageEvent,TextMessageContent)
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
    # 取得 LINE 傳來的簽章驗證身份
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 在這裡加一行最簡單的 print 測試
    print(">>> 進入了 handle_message 函式 <<<", flush=True)
    
    user_id = event.source.user_id
    user_text = event.message.text
    print(f"收到來自 {user_id} 的訊息: {user_text}", flush=True)
if __name__ == "__main__":
    # Flask 預設跑在 5000 埠
    app.run(port=5000)