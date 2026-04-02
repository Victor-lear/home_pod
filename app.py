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
    
    print(f"發言者 ID: {user_id}", flush=True)
    print(f"文字內容: {user_text}", flush=True)
if __name__ == "__main__":
    # Flask 預設跑在 5000 埠
    app.run(port=5000)