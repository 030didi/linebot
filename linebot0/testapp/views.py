from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TextMessage,
    ImageSendMessage,
    StickerSendMessage,
    LocationSendMessage,
    AudioSendMessage,
)
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from linebot.models import VideoSendMessage, TemplateSendMessage
from linebot.models import (
    ButtonsTemplate,
    MessageTemplateAction,
    URITemplateAction,
    PostbackTemplateAction,
    PostbackEvent,
)
from linebot.models import ConfirmTemplate, CarouselColumn, CarouselTemplate
from linebot.models import ImageCarouselTemplate, ImageCarouselColumn
from linebot.models import (
    ImagemapSendMessage,
    BaseSize,
    MessageImagemapAction,
    ImagemapArea,
    URIImagemapAction,
)
from linebot.models import DatetimePickerTemplateAction, PostbackAction
import datetime


import requests

from urllib.parse import parse_qsl


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == "基本資訊":
                        sendbasid(event)
                    
                    elif mtext == "community":
                        sendCommunity(event)
                        
                    elif mtext == "map":
                        sendMap(event)
                    
                    else:
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text=mtext)
                        )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def sendbasid(event):  # 基本資訊
    try:
        message = TemplateSendMessage(
            alt_text="確認樣板",
            template=ConfirmTemplate(
                text="想要了解甚麼呢?",
                actions=[
                    MessageTemplateAction(label="資管系社群", text="community"),  # 按鈕選項
                    MessageTemplateAction(label="學校地圖", text="map"),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤!"))


def get_ngrok_url():# 學校地圖自動取得 ngrok 網址
    try:
        # ngrok 的本地 API
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except:
        return None

def sendMap(event):  # 學校地圖
    try:
        # 自動取得 ngrok 網址
        base_url = get_ngrok_url()
        if not base_url:
            # 如果取不到，就用固定的
            base_url = "https://your-ngrok-url.ngrok.io"
            
        image_url = f"{base_url}/static/map.jpg"
        
        message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url,
        )
        line_bot_api.reply_message(event.reply_token, message)
        
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="地圖載入失敗"))


def sendCommunity(event):  # 資管系社群
    try:
        message = TemplateSendMessage(
            alt_text="按鈕樣板",
            template=ButtonsTemplate(
                thumbnail_image_url="https://im.cycu.edu.tw/wp-content/uploads/college-unit_LOGO-%E8%B3%87%E8%A8%8A%E7%AE%A1%E7%90%86%E5%AD%B8%E7%B3%BB.png",
                title="中原大學資管系主要社群",  # 主標題
                text="請選擇：",  # 副標題
                actions=[
                    URITemplateAction(  # 開啟網頁
                        label="官網",
                        uri="https://im.cycu.edu.tw/",
                    ),
                    URITemplateAction(  # 開啟網頁
                        label="FB",
                        uri="https://www.facebook.com/share/g/1AtRVLBzBo/?mibextid=wwXIfr",
                    ),
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="資管系社群發生錯誤!")
        )

