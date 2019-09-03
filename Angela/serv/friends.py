import os, time
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request

from BaiduAI import text_to_audio
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH
from redis_msg import get_msg_one

friends = Blueprint("friends", __name__)

@friends.route("/friend_list",methods=["POST"])
def friends_list():
    user_id = request.form.get("_id")
    user_info = MongoDB.Users.find_one({"_id": ObjectId(user_id)})

    friend_list = user_info.get("friend_list")

    RET["CODE"] = 0
    RET["MSG"] = "好友查询"
    RET["DATA"] = friend_list
    return jsonify(RET)

@friends.route("/chat_list",methods=["POST"])
def chat_list():
    chat_info = request.form.to_dict()
    chat_id = ObjectId(chat_info.get("chat_id"))
    chat = MongoDB.Chats.find_one({"_id":chat_id})

    # 获取聊天记录
    chat_window_list = chat.get("chat_list")[-5:]
    # 返回聊天记录
    RET["CODE"] = 0
    RET["MSG"] = "好友查询"
    RET["DATA"] = chat_window_list

    get_msg_one(chat_info.get("from_user"),chat_info.get("to_user"))
    return jsonify(RET)


@friends.route("/recv_msg",methods=['POST'])
def recv_msg():
    chat_info = request.form .to_dict()
    # 取出发送消息的人和接收消息的人
    sender = chat_info.get("from_user")
    receiver = chat_info.get("to_user")
    # 获取消息的数目，以及发消息的人
    count,sender = get_msg_one(sender,receiver)
    user_list = [sender,receiver]
    # 查找出两个人的聊天消息
    chat_window = MongoDB.Chats.find_one({"user_list":{"$all":user_list}})

    # 拿出最近的count条消息进行渲染
    ch = chat_window.get("chat_list")[-count:] # type=list
    # 将列表进行翻转
    ch.reverse()
    # 当收取消息时，不知道是谁发的，消息提醒2 = 以下是来自xxx的消息
    sender_name = "小伙伴"
    toy_info = MongoDB.Toys.find_one({"_id":ObjectId(receiver)})
    print(toy_info)
    for friend in toy_info.get("friend_list"):
        if friend.get("friend_id") == sender:
            sender_name = friend.get("friend_remark")

    filename = text_to_audio(f"以下是来自于{sender_name}的{count}条消息，请注意处理！")
    xxtx_dict = {
        "from_user":sender,
        "to_user":receiver,
        "chat":filename,
        "createTime":time.time()

    }
    ch.append(xxtx_dict)
    return jsonify(ch)

    # redis ;{
    # k:"{}"
    # }
    # k == 收消息方








@friends.route("/add_req",methods=["POST"])
def add_req():
    req_info = request.form.to_dict() # {'add_user': '5d56472b153df76949c8c4cd', 'toy_id': '5d5a586993b0f1aa17feb23b', 'add_type': 'toy', 'req_info': '我是亚索', 'remark': '瑞文'}
    user_id = ObjectId(req_info.get("add_user"))
    toy_id = ObjectId(req_info.get("toy_id"))
    toy_info = MongoDB.Toys.find_one({"_id":toy_id})

    # 对收到的好友请求类型进行判断，并且到对应的数据库中去查询
    if req_info.get("add_type") == "toy":
        user_info = MongoDB.Toys.find_one({"_id": user_id})
    else:
        user_info = MongoDB.Users.find_one({"_id": user_id})

    # 补全数据结构 avatar、nickname、status、toy_name
    req_info["avatar"] = user_info.get("avatar")
    req_info["nickname"] =user_info.get("nickname") if user_info.get("nickname") else user_info.get("toy_name")
    req_info["status"] = 0
    req_info["toy_name"] = toy_info.get("toy_name")


    # req_info = {
    #     "add_user":req_info.get("add_user"),
    #     "toy_id":req_info.get("toy_id"),
    #     "add_type":req_info.get("add_type"),
    #     "req_info":req_info.get("req_info"),
    #     "remark":req_info.get("remark"),
    #     "avatar":user_info.get("avatar"),
    #     "nickname":user_info.get("nickname"),
    #     "status":1,
    #     "toy_name":toy_info.get("toy_name")
    #
    # }
    # 创建好数据结构，然后创建Request表
    MongoDB.Request.insert_one(req_info)

    RET["CODE"] = 0
    RET["MSG"] = "查询好友请求！"
    RET["DATA"] = {}

    return jsonify(RET)






@friends.route("/req_list",methods=["POST"])
def req_list():
    # fri_request = request.form.to_dict()
    _id = request.form.get("user_id")
    # 查询Users表中的bind_toys
    user_info = MongoDB.Users.find_one({"_id":ObjectId(_id)})
    bind_toys = user_info.get("bind_toys")
    # 玩具请求列表，这个需要使用到$in的方法，判断被添加的玩具id，也就是App中自己的玩具id只要在绑定列表中，就进行展示出来
    toy_req_list = list(MongoDB.Request.find({"toy_id":{"$in":bind_toys}}))
    # 使用枚举循环把数据中 的"_id" 进行str转换
    for index,req in enumerate(toy_req_list):
        toy_req_list[index]["_id"] = str(req.get("_id"))

    RET["CODE"] = 0
    RET["MSG"] = "添加好友请求成功！"
    RET["DATA"] = toy_req_list

    return jsonify(RET)


# 拒绝请求
@friends.route("/ref_req",methods=["POST"])
def ref_req():
    req_id = request.form.get("req_id")
    # 拒绝请求的时候，只需要把对应的status更新成2即可
    MongoDB.Request.update_one({"_id":ObjectId(req_id)},{"$set":{"status":2}})

    RET["CODE"] = 0
    RET["MSG"] = "拒绝添加好友！"
    RET["DATA"] = {}

    return jsonify(RET)

# 同意请求
@friends.route("/acc_req",methods=["POST"])
def acc_req():
    acc_info = request.form.to_dict() # req_id  remark
    # 拿到好友请求的id
    req_id = request.form.get("req_id")
    # 拿到给好友的备注
    remark = request.form.get("remark")

    # 查询好友请求的数据
    req_info = MongoDB.Request.find_one({"_id":ObjectId(req_id)})

    # 添加好友，双方交换名片
    # 名片的格式
    # a = {
    # 	# 		"friend_id" : "5d5a586993b0f1aa17feb23b",
    # 	# 		"friend_nick" : "豆豆",
    # 	# 		"friend_remark" : "锐雯",
    # 	# 		"friend_avatar" : "toy.jpg",
    # 	# 		"friend_chat" : "5d5a586993b0f1aa17feb23a",
    # 	# 		"friend_type" : "toy"
    # 	# 	}

    # 查询接收方toy的信息
    toy_info = MongoDB.Toys.find_one({"_id":ObjectId(req_info.get("toy_id"))})

    # 创建聊天窗口 add_user toy_id
    chat_window = MongoDB.Chats.insert_one({"user_list":[req_info.get("add_user"),req_info.get("toy_id")],"chat_list":[]})
    # 1.制作名片 add_user add toy\
    user_add_toy = {
        "friend_id": req_info.get("toy_id"),
        "friend_nick": toy_info.get("toy_name"),
        "friend_remark": req_info.get("remark"),  # 接收方在同意的时候添加的备注 发起方在发起请求的接收方备注
        "friend_avatar": toy_info.get("avatar"),
        "friend_chat": str(chat_window.inserted_id), # chat_window 新建聊天窗口
        "friend_type": "toy"  # 接收方永远是toy
    }

    # 2.将名片添加到add_user的friend_list中

    if req_info.get("add_type") == "toy":
        MongoDB.Toys.update_one({"_id":ObjectId(req_info.get("add_user"))},{"$push":{"friend_list":user_add_toy}})
    else:
        MongoDB.Users.update_one({"_id":ObjectId(req_info.get("add_user"))},{"$push":{"friend_list":user_add_toy}})


    # 2.制作名片 toy add add_user
    toy_add_user = {
        "friend_id": req_info.get("add_user"),
        "friend_nick": req_info.get("nick_name"),
        "friend_remark": remark,
        "friend_avatar": req_info.get("avatar"),
        "friend_chat": str(chat_window.inserted_id),
        "friend_type": req_info.get("add_type")
    }
    # 将名片更新到friend_list
    MongoDB.Toys.update_one({"_id": ObjectId(req_info.get("toy_id"))}, {"$push": {"friend_list": toy_add_user}})

    MongoDB.Request.update_one({"_id":ObjectId(req_id)},{"$set":{"status":1}})

    RET["CODE"] = 0
    RET["MSG"] = "同意添加好友！"
    RET["DATA"] = {}

    return jsonify(RET)