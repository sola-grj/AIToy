import os
import time

import pypinyin
import requests
from bson import ObjectId

from Config import AUDIO_CLIENT, CHAT_PATH, VOICE, MongoDB, NATURAL_NLP, TL_DATA, TL_URL
from uuid import uuid4
import os

# 语言合成
from my_nlp import my_gensim_nlp


def text_to_audio(text):
    filename = f"{uuid4()}.mp3"
    file_path = os.path.join(CHAT_PATH,filename)
    res = AUDIO_CLIENT.synthesis(text,"zh",1,VOICE)
    if type(res) == dict:
        pass
    with open(file_path,"wb")as f:
        f.write(res)
    return filename


def get_file_content(filePath):
    cmd_str = f"ffmpeg -y  -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm"
    os.system(cmd_str)
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()
# 语音识别
def audio_to_text(filepath):
    res = get_file_content(filepath)

    ret = AUDIO_CLIENT.asr(res, 'pcm', 16000, {
        'dev_pid': 1536,
    })
    print(ret.get("result")[0],type(ret.get("result")[0]))
    return ret.get("result")[0]


# 自然语言处理
def my_nlp(Q:str,toy_id):

    # 理解Q 的意图
    # 点播歌曲 - 我想听小毛驴 我要听 请播放
    max_score = 0
    if "我想听" in Q or "我要听" in Q or "请播放" in Q:
        q = Q
        q = q.replace("我想听","")
        q = q.replace("我要听","")
        q = q.replace("请播放","")
        content_dict = my_gensim_nlp(q)
        if content_dict:
            return {"from_user": "ai", "music": content_dict.get("music")}

    # 主动发起聊天
    if "发消息" in Q or "聊天" in Q:
        Q_py = "".join(pypinyin.lazy_pinyin(Q,pypinyin.TONE3))
        toy = MongoDB.Toys.find_one({"_id":ObjectId(toy_id)})
        for friend in toy.get("friend_list"):
            nick_py = "".join(pypinyin.lazy_pinyin(friend.get("friend_nick"),pypinyin.TONE3))
            remark_py = "".join(pypinyin.lazy_pinyin(friend.get("friend_remark"),pypinyin.TONE3))
            print(nick_py)
            print(remark_py)
            if nick_py in Q_py or remark_py in Q_py:
                filename = text_to_audio(f"现在可以给{friend.get('friend_remark')}发消息了")
                return {
                    "from_user":friend.get("friend_id"),
                    "chat":filename,
                    "friend_type":friend.get("friend_type")
                }

    TL_DATA["perception"]["inputText"]["text"] = Q
    TL_DATA["userInfo"]["userId"] = toy_id
    res = requests.post(TL_URL, json=TL_DATA)
    res_json = res.json()
    a = res_json.get("results")[0].get("values").get("text")
    answer = text_to_audio(a)
    return {"from_user":"ai","chat":answer}



