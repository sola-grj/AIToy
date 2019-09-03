# 静态文件的存放了路径
from aip import AipSpeech, AipNlp

MUSIC_PATH = "Music"
COVER_PATH = "Cover"
QRCODE_PATH = "QRcode"
CHAT_PATH = "Chat"

# 数据库配置
from pymongo import MongoClient
MC = MongoClient("localhost",27017)
MongoDB = MC["Angela"]

# redis数据库
from redis import Redis
RDB = Redis("127.0.0.1",6379)



# 返回配置
RET = {
    "CODE":0,
    "MSG":"",
    "DATA":{}
}

# 二维码
LT_URL = "http://qr.liantu.com/api.php?text=%s"


# 百度AI = API
APP_ID = '16981694'
API_KEY = 'NkmlMswhfgrbe55PjsX85aAH'
SECRET_KEY = '7GuSfCOE5n6GeVRU73rhT8FXarB8XCk6'
VOICE = {
    'vol': 5,
    'spd':4,
    'pit':6,
    'per':4

}
AUDIO_CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
NATURAL_NLP = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# 图灵
TL_URL = "http://openapi.tuling123.com/openapi/api/v2"
import requests

TL_DATA = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "你的男朋友是谁啊？"
        },

    },
    "userInfo": {
        "apiKey": "9839d499aa73422382b5cbde26b044c6",
        "userId": "1131631886"
    }
}