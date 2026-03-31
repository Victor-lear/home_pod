from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
ENV = './.env' 
load_dotenv(dotenv_path=ENV)
app = Flask(__name__)

# --- 請在此填入你的憑證 ---
# 從 LINE Developers Console 取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') 
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') 

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

# 當收到「文字訊息」時觸發
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    print(f"收到訊息: {user_msg}")
    
    # 這裡可以根據 user_msg 決定要呼叫什麼 API
    # 範例：簡單回傳
    reply = f"你說了：{user_msg}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    # Flask 預設跑在 5000 埠
    app.run(port=5000)