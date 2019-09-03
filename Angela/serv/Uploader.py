import os, time
from uuid import uuid4

from bson import ObjectId
from BaiduAI import text_to_audio, my_nlp, audio_to_text
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH, CHAT_PATH
from redis_msg import set_msg

uploader = Blueprint("uploader", __name__)


@uploader.route("/app_uploader", methods=["POST"])
def app_uploader():
    msg_info = request.form.to_dict()
    # user_id sender to_user receiver
    # 用过user_list 子集查询 $all 可以获取到当前的聊天窗口，会将所有的聊天数据全部都查询得到，能不能不查询直接更新
    user_list = [msg_info.get("user_id"),msg_info.get("to_user")]
    chat_window = MongoDB.Chats.find_one({"user_list":{"$all":user_list}})
    print("chat_window4444",chat_window)
    voice_info = request.files.get("reco_file")
    voice_path = os.path.join(CHAT_PATH,voice_info.filename)

    voice_info.save(voice_path)
    os.system(f"ffmpeg -i {voice_path} {voice_path}.mp3")
    os.remove(voice_path)

    chat_info = {
        "from_user": msg_info.get("user_id"),
        "to_user": msg_info.get("to_user"),
        "chat": f"{voice_info.filename}.mp3",
        "create_time":time.time()

    }
    MongoDB.Chats.update_one({"user_list":{"$all":user_list}},{"$push":{"chat_list":chat_info}})

    set_msg(msg_info.get("user_id"),msg_info.get("to_user"))
    # 替换返回值中的filename，可以让toy播放不同 的内容
    toy_id = ObjectId(msg_info.get("to_user"))
    toy_info = MongoDB.Toys.find_one({"_id":toy_id})

    sender = "小伙伴"
    for friend in toy_info["friend_list"]:
        if friend["friend_id"] == msg_info.get("user_id"):
            sender = friend.get("friend_remark")

    filename = text_to_audio(f"你有一条来自于{sender}的消息，请注意处理！")
    data = {
        # "filename":f"{voice_info.filename}.mp3",
        "filename":filename,
        "friend_type":"app"
    }
    RET["CODE"] = 0
    RET["MSG"] = "上传成功"
    RET["DATA"] = data
    return jsonify(RET)



@uploader.route("/toy_uploader",methods=["POST"])
def toy_uploader():
    msg_info = request.form.to_dict()
    # 把自己的id以及接收消息的人都放在列表中，用来查询时使用 $all
    user_list = [msg_info.get("user_id"), msg_info.get("to_user")]
    chat_window = MongoDB.Chats.find_one({"user_list": {"$all": user_list}})
    # 获取发出去的语音消息
    voice_info = request.files.get("reco")
    # 由于前端的一些问题，我们把语音的名字进行UUID修改
    filename = f"{voice_info.filename}{uuid4()}"
    # 找一个存放语音的文件进行了路径的拼接
    voice_path = os.path.join(CHAT_PATH, filename)
    # 按照路径把语音文件存放好
    voice_info.save(voice_path)
    # 由于渲染的问题，我们把语音文件转换为MP3
    os.system(f"ffmpeg -i {voice_path} {voice_path}.mp3")
    # 再把最开始的语音文件删除掉
    os.remove(voice_path)
    # 这个时候构造聊天字典（根据Chats表的数据结构创建）
    chat_info = {
        "from_user": msg_info.get("user_id"),
        "to_user": msg_info.get("to_user"),
        "chat": f"{filename}.mp3",
        "create_time": time.time()

    }
    # 在把聊天记录更新到Chats表中，使用$push
    MongoDB.Chats.update_one({"user_list": {"$all": user_list}}, {"$push": {"chat_list": chat_info}})
    # 使用redis创建receiver ：{sender：1}的数据结构
    set_msg(msg_info.get("user_id"),msg_info.get("to_user"))

    # 获取自己的好友类型 App/Toy
    if MongoDB.Toys.find_one({"_id":ObjectId(msg_info.get("user_id"))}):
        friend_type = "toy"
    else:
        friend_type = "app"
    # 当语音接收方的类型是toy时，再次触发这个消息的提醒
    if msg_info.get("friend_type") == "toy":
        sender = "小伙伴"
        toy_info = MongoDB.Toys.find_one({"_id":ObjectId(msg_info.get("user_id"))})
        print("toy_info",toy_info)
        print("msg_info",msg_info)
        for friend in toy_info["friend_list"]:
            if friend["friend_id"] == msg_info.get("to_user"):
                sender = toy_info.get("toy_name")
        filename = text_to_audio(f"你有一条来自于{sender}的消息，请注意处理！")

    data = {
        "filename": filename,
        "friend_type": friend_type
    }
    RET["CODE"] = 0
    RET["MSG"] = "上传成功"
    RET["DATA"] = data
    return jsonify(RET)


@uploader.route("/ai_uploader",methods=["POST"])
def ai_upoader():
    toy_info = request.form.to_dict()
    reco = request.files.get("reco")
    filename = f"{uuid4()}.wav"
    filepath = os.path.join(CHAT_PATH,filename)
    reco.save(filepath)

    # 人工智能操作
    # 点播音乐
    Q = audio_to_text(filepath)

    ret = my_nlp(Q,toy_info.get("toy_id"))
    # AI对话

    # 主动发起消息

    return jsonify(ret)









# @uploader.route("/recv_msg", methods=["POST"])
# def recv_msg():
#     msg_info = request.form.to_dict()
#     user_list = [msg_info.get("from_user"),msg_info.get("to_user")]
#     chat_window = MongoDB.Chats.find_one({"user_list": {"$all": user_list}})
#     message_list = []
#     data = []
#     for chat in chat_window["chat_list"]:
#         if chat.get("from_user") == msg_info.get("from_user"):
#             message_list.append(chat.get("create_time"))
#     else:
#         sorted(message_list)
#     last_mes_time = message_list[-1]
#     for i in chat_window["chat_list"]:
#         if i["create_time"] == last_mes_time:
#             data.append(i)
#     print("message_list********",message_list)
#
#     return jsonify(data)
