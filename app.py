from flask import Flask, request, abort, render_template

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

line_bot_api = LineBotApi('wEAYlhnzhVzBVbSJnXhbbsOp/yccxr733nsKhZx3KX45MAa5lv7rdVuv+Qtju5w39DCU4HKiFqdJlEJdSEr///obW6spUhtbyPRS+KaTNF6gYIKH32ytWm21wsnM29630MMmhp1OCb9OI+tnPJaa0gdB04t89/1O/w1cDnyilFU=') #CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('972fe2410b1815a28ff6a68ac8f410b7') #CHANNEL_SECRET

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()