from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
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
    QuickReplyButton,
    MessageAction,
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
                    if mtext == '課程應修':
                        course(event)

                    elif mtext == '教授清單':  
                        show_professors(event)

                    elif mtext == '顯示教授清單':
                        show_professors(event)

                    elif mtext == '顯示一年級必修課程':
                        show_course(event)

                    elif mtext == '顯示二年級必修課程':
                        show_course1(event)

                    elif mtext == '顯示三、四年級必修課程':
                        show_course2(event)

                    elif mtext == '顯示畢業應修最低學分數':
                        show_credits(event)

                    elif mtext == '顯示基本知能科目':
                        show_credits1(event)

                    elif mtext == '顯示通識基礎必修科目':
                        show_credits2(event)

                    elif mtext == '美食':
                        food(event)

                    elif mtext == '顯示夜市美食':
                        food1(event)

                    elif mtext == '顯示女、男博得美食':
                        food2(event)

                    elif mtext == '顯示商學小門美食':
                        food3(event)
                        
                    elif mtext == "基本資訊":
                        sendbasid(event)
                    
                    elif mtext == "community":
                        sendCommunity(event)
                        
                    elif mtext == "map":
                        sendMap(event)
                        
                    elif mtext == "學長姐QA":
                        sendQA(event)
                        
                    elif handle_qa_response(event, mtext):
                        # QA回應已處理
                        pass
                    elif mtext == "交通資訊":
                        sendTraffic(event)

                    elif mtext == '往北交通資訊':
                        north(event)

                    elif mtext == '往南交通資訊':
                        south(event)

                    elif mtext == '住宿資訊':
                        live(event)

                    elif mtext == '男宿':
                        boylive(event)

                    elif mtext == '男宿基本資訊':
                        bb(event)

                    elif mtext == '男宿位置':
                        sendPosition1(event)

                    elif mtext == '女宿':
                        girllive(event)

                    elif mtext == '恩慈':
                        gn(event)
                    elif mtext == '恩慈基本資訊':
                        gnn(event)
                    elif mtext == '恩慈位置':
                        sendPosition2(event)

                    elif mtext == '良善':
                        gc(event)

                    elif mtext == '良善基本資訊':
                        gcc(event)

                    elif mtext == '良善位置':
                        sendPosition3(event)

                    elif mtext == '租屋':
                        liveoutside(event)
                    elif mtext == '租房基本資訊':
                        ll(event)




                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))
                        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()






#交通資訊
def sendTraffic(event): #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='交通資訊',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.cycu.edu.tw/img/map.gif',
                        title='交通資訊',
                        text='你是北漂還是南漂？',
                        actions=[
                            MessageTemplateAction( 
                                label='北漂',
                                text='往北交通資訊'
                            ),
                            MessageTemplateAction( 
                                label='南漂',
                                text='往南交通資訊'
                            ),
                           
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

def north(event):
    try:
        text2 = '''
往北部移動的話，可以....

1.搭乘校門口的客運
2.可坐公車120或騎U-bike到機捷，搭至A22老街溪，坐到台北車站 
3.桃園高鐵站
4.搭乘155、156、167、122N至中壢火車站，搭乘火車前往

                '''
        message = TextSendMessage(
            text = text2
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def south(event):
    try:
        text2 = '''
往南部移動的話，可以....

1.搭乘181A往桃園高鐵站
2.坐到板橋高鐵站再往下搭（155/156/169/167/121N到中壢火車站 往上搭到板橋站再轉高鐵)
4.搭乘155、156、167、122N至中壢火車站，搭乘火車前往
                '''
        message = TextSendMessage(
            text = text2
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))



# 住宿資訊
def live(event): 
    try:
        message = TemplateSendMessage(
            alt_text='住宿資訊',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='住宿資訊',
                        text='要住哪！',
                        actions=[
                            MessageTemplateAction( 
                                label='男宿',
                                text='男宿'
                            ),
                            MessageTemplateAction( 
                                label='女宿',
                                text='女宿'
                            ),
                            MessageTemplateAction( 
                                label='租屋',
                                text='租屋'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

# 男住宿資訊
def boylive(event):  
    try:
        message = TemplateSendMessage(
            alt_text='男住宿資訊',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='男生住宿資訊',
                        text='點選想了解的內容',
                        actions=[
                            MessageTemplateAction( 
                                label='男宿基本資訊',
                                text='男宿基本資訊'
                            ),
                            MessageTemplateAction( 
                                label='男宿位置',
                                text='男宿位置'
                            ),
                            URITemplateAction(
                                label='力行宿舍介紹影片',
                                uri='https://www.youtube.com/watch?v=iSq_-5DO244&t=2s'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

# 男宿基本資訊
def bb(event): 
    try:
        text = '''
1.名稱：力行宿舍
2.六人一間，雅房
3.力行宿舍床墊尺寸：90CM × 200CM。可自行購買或是一起訂購
4.無頭鬼拍球鬼故事

(隱藏資訊：浴室在地名產：聽說水龍頭會變成水箭龜)
        '''
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

# 力行宿舍位置
def sendPosition1(event): 
    try:
        message = LocationSendMessage(
            title='力行宿舍',
            address='中原大學力行宿舍\n320桃園市中壢區新中北路291號',
            latitude=24.959707256475387,
            longitude=121.24077895356582
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))





# 女生住宿資訊
def girllive(event):  
    try:
        message = TemplateSendMessage(
            alt_text='女住宿資訊',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='女生住宿資訊',
                        text='女生宿舍分為恩慈跟良善~，點選想了解的內容吧！',
                        actions=[
                            MessageTemplateAction( 
                                label='恩慈',
                                text='恩慈'
                            ),
                            MessageTemplateAction( 
                                label='良善',
                                text='良善'
                            ),     
                        
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

# 恩慈基本資訊
def gn(event):  
    try:
        message = TemplateSendMessage(
            alt_text='恩慈',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='恩慈',
                        thumbnail_image_url='https://scontent.ftpe8-4.fna.fbcdn.net/v/t39.30808-6/472482520_1104141131409888_928593725460338375_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=U-N6Txl64IsQ7kNvwEj3R_2&_nc_oc=AdmNo9F9bTsH8jfdwex2XqBjGuJId0ohX14gtbGqvjBBKPLim9bqz93NtxVW4YhoOZA&_nc_zt=23&_nc_ht=scontent.ftpe8-4.fna&_nc_gid=vxhIOonHmBBdt-9fo3V0-g&oh=00_AfOox9Dvl4uAYtz-aM6Jhr7zdClhVZcJMAZ428pR0-A9oA&oe=684F41B0',
                        text='點選想了解的內容',
                        actions=[
                            MessageTemplateAction( 
                                label='恩慈基本資訊',
                                text='恩慈基本資訊'
                            ),
                            MessageTemplateAction( 
                                label='恩慈位置',
                                text='恩慈位置'
                            ),
                            URITemplateAction(
                                label='恩慈宿舍介紹影片',
                                uri='https://www.youtube.com/watch?v=zSmtxSjeaZA'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


# 恩慈基本資訊
def gnn(event): 
    try:
        text = '''
1.四人一間，雅房
2.宿舍床墊尺寸：85CM*190CM。可自行購買或是一起訂購
3.12點後會自動斷電
4.衛浴：一邊三間廁所一邊三間浴室
5.00:00~06:00需申請夜間進出同意書，刷指靜脈進入

        '''
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


# 恩慈宿舍位置
def sendPosition2(event): 
    try:
        message = LocationSendMessage(
            title='恩慈宿舍',
            address='320桃園市中壢區大仁二街35號',
            latitude=24.955495578095785,
            longitude=121.24245257437362
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))





# 良善基本資訊
def gc(event):  
    try:
        message = TemplateSendMessage(
            alt_text='良善',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='良善',
                        thumbnail_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/480497410_1183469673481104_1163668016500089089_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=E6DaaB6QA_IQ7kNvwH43G1J&_nc_oc=AdngwoF2e-864H0p2-MQsoNO5b6oJYS536HZ3rq47y75uefrbo5QjWFfN4i-ww7XXiM&_nc_zt=23&_nc_ht=scontent-tpe1-1.xx&_nc_gid=-_nzNTpayeYOAbO3lzzZuw&oh=00_AfM0tPRZtyRBg1vvUGXdyCmWvw-Z80cgmBCGZTmej_YrtQ&oe=684F5F98',
                        text='點選想了解的內容',
                        actions=[
                            MessageTemplateAction( 
                                label='良善基本資訊',
                                text='良善基本資訊'
                            ),
                            MessageTemplateAction( 
                                label='良善位置',
                                text='良善位置'
                            ),
                            URITemplateAction(
                                label='良善宿舍介紹影片',
                                uri='https://www.youtube.com/watch?v=fnr3mBE46lM&t=1s'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


# 良善基本資訊
def gcc(event): 
    try:
        text = '''
1.四人一間，套房
2.宿舍床墊尺寸：90CM*180CM。可自行購買或是一起訂購
3.00:00~06:00需申請夜間進出同意書，刷指靜脈進入
4.可借桌遊與遊戲

        '''
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


# 良善宿舍位置
def sendPosition3(event): 
    try:
        message = LocationSendMessage(
            title='良善宿舍',
            address='良善樓 No.82 Daren St, 中壢區桃園市320',
            latitude=24.955608540000007,
            longitude=121.2420865431405
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))



# 租房資訊
def liveoutside(event):  
    try:
        message = TemplateSendMessage(
            alt_text='租房資訊',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='租房資訊',
                        text='點選想了解的內容',
                        actions=[
                            MessageTemplateAction( 
                                label='租房基本資訊',
                                text='租房基本資訊'
                            ),
                            
                            URITemplateAction(
                                label='中原大學 校外賃居網',
                                uri='https://house.nfu.edu.tw/CYCU'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

# 租屋基本資訊
def ll(event): 
    try:
        text = '''
1.租房可在周邊看房 看有沒有電話 有就打過去問看看
2.基本上有名的房子為：哈佛劍橋(在女博得)、灰樓、紅樓、白樓、中原double、凱悅等等，可上dcard搜尋相關資訊

        '''
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


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


def course(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='課程應修',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/zh/thumb/8/83/CYCU.svg/1200px-CYCU.svg.png',
                        title='必修應修',
                        text='學系必修',
                        actions=[
                            MessageTemplateAction(
                                label='一年級',
                                text='顯示一年級必修課程'
                            ),
                            MessageTemplateAction(
                                label='二年級',
                                text='顯示二年級必修課程'
                            ),
                            MessageTemplateAction(
                                label='三、四年級',
                                text='顯示三、四年級必修課程'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/zh/thumb/8/83/CYCU.svg/1200px-CYCU.svg.png',
                        title='畢業門檻',
                        text='畢業學分結構',
                        actions=[
                            MessageTemplateAction(
                                label='畢業應修最低學分數',
                                text='顯示畢業應修最低學分數'
                            ),
                            MessageTemplateAction(
                                label='基本知能科目',
                                text='顯示基本知能科目'
                            ),
                            MessageTemplateAction(
                                label='通識基礎必修科目',
                                text='顯示通識基礎必修科目'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/zh/thumb/8/83/CYCU.svg/1200px-CYCU.svg.png',
                        title='教授資訊',
                        text='點選查看老師列表',
                        actions=[
                            MessageTemplateAction(label='教授清單', text='顯示教授清單'),
                            URITemplateAction(label='中原大學', uri='https://www.cycu.edu.tw/'),
                            URITemplateAction(label='中原資管系', uri='https://im.cycu.edu.tw/')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/zh/thumb/8/83/CYCU.svg/1200px-CYCU.svg.png',
                        title='學生時間線',
                        text='學生可查看哪年級該做甚麼事',
                        actions=[
                            URITemplateAction(
                                label='學生時間線',
                                uri='https://upload.cc/i1/2025/06/08/cHOfYk.png'
                            ),
                            URITemplateAction(
                                label='中原大學', uri='https://www.cycu.edu.tw/'
                            ),
                            URITemplateAction(
                                label='中原資管系', uri='https://im.cycu.edu.tw/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))



def show_professors(event):
    message = TemplateSendMessage(
        alt_text='教授清單',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='教授清單 1',
                    text='請選擇老師',
                    actions=[
    MessageTemplateAction(
        label='廖秀莉',
        text='''【廖秀莉 教授】
📧 hsiuliliao@cycu.edu.tw
🎓 國立台灣科技大學資訊管理 博士
📞 系主任辦公室 分機：5400 / 資管302D研究室 分機：5417
📚 電子商務、網路經營、專案管理、數位學習、人工智慧
📘 開設課程: 大學入門、行銷管理資訊系統、專案管理、資訊管理
、資訊管理文獻選讀、資訊管理專題(一) 、資訊管理專題(二)
、論文寫作

'''
    ),
    MessageTemplateAction(
        label='范錚強',
        text='''【范錚強 教授】
📧 ckfarn@gmail.com
🎓 美國加州大學洛杉磯分校資訊管理 博士
📞 資管304研究室 分機：5430
📚 資訊系統管理、電子化企業、企業電腦化問題
📘 開設課程:生產管理、企業e化研討、整合商業應用'''
    ),
    MessageTemplateAction(
        label='吳肇銘',
        text='''【吳肇銘 教授】
📧 mislighter@gmail.com
🎓 國立中央大學資訊管理 博士
📞 資管301研究室 分機：5428
📚 大數據、智慧治理、電子政府、地方創生
🏆 國家發展研究院長、100MVP、傑出資訊人才獎
📘開設課程: 企業概論、研究方法、資訊管理、論文寫作

'''
    )
]
                ),
                CarouselColumn(
                    title='教授清單 2',
                    text='請選擇老師查看資訊',
                    actions=[
                        MessageTemplateAction(label='皮世明', text='''【皮世明 教授】
📧 happypi@gmail.com
📧 smpi@cycu.edu.tw
🎓國立中央大學資訊管理 博士
📞 教務長室 分機：2000
📞 資管305D研究室 分機：5406
📚決策支援系統、商業智慧系統、醫療資訊系統、顧客關係管理
📘開設課程:生產管理資訊系統、決策支援研究、統計學(一) 、統計學(二)
、資訊管理專題(一) 、資訊管理專題(二) 、資訊管理理論、讓數字說話的統計學
'''),
                        MessageTemplateAction(label='劉士豪', text='''【劉士豪 教授】
📧 vandy1020@gmail.com
🎓國立政治大學企業管理研究所資訊管理組 博士
📞資管303A研究室 分機：5411
📚資訊管理專題、系統分析與設計、系統執行與評估、組織與資訊系統
📘開設課程:大數據分析、系統分析與設計、個案研究、個案研究(Ⅲ) 、軟體專案管理、資訊管理專題(一) 、資訊管理專題(二) 、資通安全管理與實務、網際網路政府應用
'''),
                        MessageTemplateAction(label='戚玉樑', text='''【戚玉樑 教授】
📧maxchi@cycu.edu.tw
🎓美國亞利桑那州立大學工業與管理系統 博士
📞資管305E研究室 分機：5408
📚分散式應用系統整合、資訊技術、知識工程語意網應用、網路服務技術
📘開設課程: Java程式設計、Python程式設計、企業倫理、企業倫理專題研討
''')
                    ]
                ),
                CarouselColumn(
                    title='教授清單 3',
                    text='請選擇老師查看資訊',
                    actions=[
                        MessageTemplateAction(label='洪智力', text='''【洪智力 教授】
📧chihli@cycu.edu.tw
🎓英國桑德蘭大學資訊 博士
📞資管305C研究室 分機：5407
📚類神經網路、資訊檢索、資料探勘、計算智慧
📘開設課程: 文字探勘、資料庫管理、網路程式設計
'''),
                        MessageTemplateAction(label='林志浩', text='''【林志浩 教授】 
📧linch@cycu.edu.tw
🎓國立台灣大學資訊管理學 博士
📞數位教育長室 分機：2700
📞AACSB執行長辦公室 分機：5007
📞資管303B研究室 分機：5410
📚行動通訊網路、智慧電網通訊、車載資通訊應用、系統最佳化、網路規劃與管理
📘開設課程: 企業資料通訊、行動智慧之最佳化應用、商用數學、資料結構、資訊管理專題(一) 、資訊管理專題(二) 、管理數學
'''),
                        MessageTemplateAction(label='李維平', text='''【李維平 教授】
📧wplee@cycu.edu.tw
🎓國立交通大學資訊工程 博士
📞資管302C研究室 分機：5416
📚人工智慧、大數據分析、資料探勘、智慧型投資、財務探勘
📘開設課程: 人工智慧與產業分析、資料探勘與人工智慧、資訊管理研討
、資訊管理專題(一) 、資訊管理專題(二) 、資訊管理專題講座、管理數學
 ''')
                    ]
                ),
                CarouselColumn(
                    title='教授清單 4',
                    text='請選擇老師查看資訊',
                    actions=[
                        MessageTemplateAction(label='廖慶榮', text='''【廖慶榮 教授】
📧cjliao@cycu.edu.tw
🎓逢甲大學資訊工程 博士
📞資管305A研究室 分機：5409
📚雲端計算與服務、磨課師與行動磨課師學習、數位學伴、創意問題解決
📘開設課程: Java程式設計、人工智慧與物聯網應用、企業實習 A、企業實習 B、作業系統、研究方法、計算機概論、資訊管理專題(一) 、資訊管理專題(二)
'''),
                        MessageTemplateAction(label='賴錦慧', text='''【賴錦慧 教授】
📧chlai@cycu.edu.tw
🎓國立交通大學資訊管理 博士
📞資管303D研究室 分機：5413
📚資料探勘、文字探勘、大數據分析、推薦系統、機器學習、資訊檢索、社群網路分析
📘開設課程: 多媒體程式設計、資料科學基礎、資料科學進階、資料科學導論、資料科學應用、資訊管理專題(一) 、資訊管理專題(二) 運算思維與程式設計
'''),
                        MessageTemplateAction(label='李國誠', text=''' 【李國誠 教授】
📧kuochen@cycu.edu.tw
🎓美國路易維爾大學資訊工程 博士
📞資管302B研究室 分機：5414
📚數位學習、類神經網路、資料開採、嵌入式系統程式設計
📘開設課程: java程式設計、Python商業應用、Python程式設計、大學入門、行動商務軟體應用、財法講座(專業自主一) 、財法講座(專業自主二)
''')
                    ]
                ),
                CarouselColumn(
                    title='教授清單 5',
                    text='請選擇老師查看資訊',
                    actions=[
                        MessageTemplateAction(label='金志聿', text='''【金志聿 教授】
📧king@cycu.edu.tw
🎓國立臺灣科技大學管理研究所 博士
📞資管302A研究室 分機：5405
📚創新與創業、網路社群行銷、電子商務、大數據分析應用
📘開設課程: 行動商務軟體應用、創業實務與個案研討
 '''),
                        MessageTemplateAction(label='周賢明', text='''【周賢明 教授】
📧chou0109@cycu.edu.tw
🎓美國馬里蘭大學資訊系統 博士
📞資管303C研究室 分機：5412
📚環境感知計算、手機應用、人工智慧應用、物聯網應用
📘開設課程:全球資訊系統策略基礎、區塊鏈與金融科技應用、商學概論、資訊科技導論、資訊管理專題(一) 、資訊管理專題(二)、運算思維與程式設計
 '''),
                        MessageTemplateAction(label='闕豪恩', text=''' 【闕豪恩 教授】
📧hechueh@cycu.edu.tw
🎓淡江大學資訊工程 博士
📞資管305B研究室 分機：5421
📞科學與人文教育發展中心 分機：2090
📚資料探勘、數位學習、人工智慧 、醫療資訊
📘開設課程: Android 程式設計、Python程式設計、決策支援研究、聊天機器人實作、資訊科技導論、資訊管理專題(一) 、資訊管理專題(二) 、運算思維與程式設計、數位科技應用、數位學習專題研究、論文寫作
''')
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
    
def show_course(event):
    try:
        text1 = '''
1. JAVA程式設計
2. NET程式設計
3. 資訊科技導論
4. 企業概論
5. 會計學(一)
6. 管理數學
7. 管理學
8. 企業資料通訊
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def show_course1(event):
    try:
        text1 = '''
1. 多媒體程式設計
2. 網路程式設計
3. 統計學(一)
4. 經濟學(一)
5. 資料結構
6. 資料庫管理
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def show_course2(event):
    try:
        text1 = '''
三年級
1. 商業英語會話(一)
2. 商業英語會話(二)
3. 系統分析與設計
4. 軟體專案管理
5. 資訊管理
6. 資訊管理專題(一)\n
四年級
1. 資訊管理專題(二)
2. 資訊與法律
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def show_credits(event):
    try:
        text1 = '''
應修最低學分數 128 
包括：
1.基本知能           6
2.通識基礎必修  14
3.學系必修         58
4.通識延伸選修  14
5.學系選修         20 
6.自由選修         16 
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def show_credits1(event):
    try:
        text1 = '''
英文(一) (二) 
英語聽講(一) (二) 
大一體育一、大一體育二；
大二、大三體育興趣擇四科 
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def show_credits2(event):
    try:
        text1 = '''
天
宗教哲學
人生哲學

人
台灣政治與民主
法律與現代生活
當代人權議題與挑戰
生活社會學
全球化大議題
經濟學的世界  (6擇1)

區域文明史   
文化思想史  (2擇1)

物
自然科學導論
工程與科技
電資與人類文明  (3擇1)

我
文學經典閱讀
語文與修辭
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def food(event): #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='美食',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.yiwulife.tw/wp-content/uploads/20201121182430_a73_DSC08347_1080x720_wm.jpg',
                        title='中原美食',
                        text='來中原都會吃的',
                        actions=[
                            MessageTemplateAction( 
                                label='夜市',
                                text='顯示夜市美食'
                            ),
                            MessageTemplateAction( 
                                label='女、男博得',
                                text='顯示女、男博得美食'
                            ),
                            MessageTemplateAction( 
                                label='商學小門',
                                text='顯示商學小門美食'
                            )
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))

def food1(event):
    try:
        text1 = '''
1. 扯後腿  
2. KiKi Garden 義大利麵
3. 手工烤布蕾(元氣眼鏡店前)
4. 勇伯
5. 月見山沙威瑪
6. 福建炒麵(吃香喝辣)
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def food2(event):
    try:
        text1 = '''
女博得：
1. 森沐
2. 越南河粉
3. 粥品

男博得：
1. 莎朗嘿 
2. 小而大 
3. 豐慶食堂 
4. 松川烤肉飯
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def food3(event):
    try:
        text1 = '''
1. 八方來    
2. 286水餃
3. 金隆便當
4. 日嚐
                '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
        
        
        
#QA功能

def sendQA(event):
    """發送學長姐QA選單"""
    
    # 創建快速回覆按鈕
    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label="💰一個月生活費", text="生活費問題")),
        QuickReplyButton(action=MessageAction(label="💳系學/學生會費", text="系學/學生會費問題")),
        QuickReplyButton(action=MessageAction(label="👥有沒有直屬", text="直屬問題")),
        QuickReplyButton(action=MessageAction(label="👗要穿什麼", text="穿搭問題")),
        QuickReplyButton(action=MessageAction(label="🏠學校住宿室友問題", text="學校住宿室友問題")),
        QuickReplyButton(action=MessageAction(label="📚必/選修課被當", text="必/選修課被當")),
        QuickReplyButton(action=MessageAction(label="🎯活動哪裡找", text="活動哪裡找")),
        QuickReplyButton(action=MessageAction(label="⏰被記曠課", text="被記曠課")),
        QuickReplyButton(action=MessageAction(label="🇺🇸英文畢業門檻", text="英文門檻問題")),
        QuickReplyButton(action=MessageAction(label="🔙返回", text="返回主選單"))
    ]
    
    # 發送QA選單訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="🎓 學長姐QA時間！\n\n請選擇你想了解的問題：",
            quick_reply=QuickReply(items=quick_reply_buttons)
        )
    )

def handle_qa_response(event, mtext):
    """處理QA回應"""
    
    qa_responses = {
        "生活費問題": {
            "question": "一個月生活費大概多少？",
            "answer": "💰 生活費大概8000～15000元\n\n這個範圍包含了基本的餐費、交通費、雜支等。實際花費會因個人消費習慣而有所不同喔！"
        },
        
        "系學/學生會費問題": {
            "question": "系學會費跟學生會費一定要繳嗎？",
            "answer": "💳 系費跟學生會費可以先不繳\n\n除非你對某些特定活動有興趣，不然可以先觀望。等熟悉環境後再決定要不要參加！"
        },
        
        "直屬問題": {
            "question": "有沒有直屬會怎樣嗎？",
            "answer": "👥 真心覺得沒差！\n\n通常只會一開始有交流，後面都跟死人一樣，很難變熟。除非你很主動會去跟他們聊天，不然影響不大。"
        },
        
        "穿搭問題": {
            "question": "我上大學要穿得很花枝招展嗎？",
            "answer": "👗 你穿得開心就好！\n\n真的沒人在乎你怎麼穿，大學就是要做自己。舒服自在最重要～"
        },
        
        "學校住宿室友問題": {
            "question": "住宿與室友不合怎麼辦？",
            "answer": "🏠 室友不合可以檢舉\n\n如果溝通後還是不行，可以申請換室友。學校都有相關的處理程序，不要委屈自己！"
        },
        
        "必/選修課被當": {
            "question": "如果必修要被當了/或是已經被當了，該怎麼辦？",
            "answer": "📚 怕被當可以停修\n\n通常下學期都可以重修，但要注意：\n• 有沒有老師開課\n• 會不會跟其他課撞課\n提早規劃比較好！"
        },
        
        "活動哪裡找": {
            "question": "學校活動要去哪裡看？",
            "answer": "🎯 上i-touch找活動資訊\n\n通識活動、音樂會、獎學金申請等資訊都可以在i-touch上找到。記得定期關注！"
        },
        
        "被記曠課": {
            "question": "我被記曠課會怎樣嗎？",
            "answer": "⏰ 每堂課只能曠課兩次\n\n超過兩次就會被老師扣考，只能選擇停修。所以要注意出席率喔！"
        },
        
        "英文門檻問題": {
            "question": "學校英文畢業門檻是什麼？",
            "answer": "🇺🇸 英文畢業門檻\n\n• 一定要修兩門全英文課程\n• 多益要過550或是全民英檢過中級初試!!\n• 沒過，有大會考可以補救\n\n建議早點規劃，免得影響畢業！"
        }
    }
    
    if mtext in qa_responses:
        response = qa_responses[mtext]
        
        # 創建回到QA選單的快速回覆
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="📋 回到QA選單", text="學長姐QA")),
            QuickReplyButton(action=MessageAction(label="🔙 返回主選單", text="返回主選單"))
        ])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"{response['question']}\n\n{response['answer']}",
                quick_reply=quick_reply
            )
        )
        return True
    
    return False
