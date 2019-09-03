import os, time
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH

devices = Blueprint("devices", __name__)


@devices.route("/scan_qr", methods=['POST'])
def scan():
    qr_info = request.form.to_dict()
    print(qr_info)
    res = MongoDB.Devices.find_one(qr_info)
    # 从数据库中对device_key进行查询
    toy_info = MongoDB.Toys.find_one(qr_info)
    # 第一种情况，直接进行绑定
    if res:
        RET["CODE"] = 0
        RET["MSG"] = "二维码扫描成功"
        RET["DATA"] = qr_info
    # 第二种情况，二维码并不存在
    else:
        RET["CODE"] = 1
        RET["MSG"] = "二维码扫描失败"
        RET["DATA"] = {}
    # 第三种情况，二维码已经被别人绑定了
    if toy_info:
        toy_id = str(toy_info.get("_id"))
        RET["CODE"] = 2
        RET["MSG"] = "设备已经绑定了！"
        RET["DATA"] = {"toy_id":toy_id}
    return jsonify(RET)


@devices.route("/bind_toy", methods=['POST'])
def bind_toy():
    toy_info = request.form.to_dict()
    user_id = toy_info.pop("user_id")
    # 创建Chats的聊天表
    chat_info = {
        "user_list": [],
        "chat_list": []
    }
    chat_info["user_list"].append(user_id)
    cha_window = MongoDB.Chats.insert_one(chat_info)
    chat_id = str(cha_window.inserted_id)

    # 创建Toys表

    user_info = MongoDB.Users.find_one({"_id":ObjectId(user_id)})
    toy_info["avatar"] = "toy.jpg"
    toy_info["bind_user"] = user_id
    toy_info["friend_list"] = []
    # 给toy绑定对应的App相关的通讯录信息
    toy_add_user = {
        "friend_id": user_id,
        "friend_nick": user_info.get("nickname"),
        "friend_remark": toy_info.pop("remark"),
        "friend_avatar": user_info.get("avatar"),
        "friend_chat": chat_id,
        "friend_type": "app"
    }
    # 将user的名片存放在toy_friend_list
    toy_info["friend_list"].append(toy_add_user)
    # 写入数据库
    toy = MongoDB.Toys.insert_one(toy_info)
    # 得到toy的id
    toy_id = str(toy.inserted_id)
    # 建立和App的绑定关系 user["bind_toy"].append(toy_id)

    # 方式一  查询用户，更改用户信息user["bind_toy"].append(toy_id)，更新用户信息
    # 方式二  直接更新用户信息表中的 bind_toy
    user_info["bind_toys"].append(toy_id)

    # 给App添加对应的toy通讯录系信息
    user_add_toy = {
        "friend_id": toy_id,
        "friend_nick": toy_info.get("baby_name"),
        "friend_remark": toy_info.get("toy_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_chat": chat_id,
        "friend_type": "toy"
    }
    # 名片属于通讯录 friend_list
    user_info["friend_list"].append(user_add_toy)

    # 更新用户user_info的数据
    MongoDB.Users.update_one({"_id":ObjectId(user_id)},{"$set":user_info})

    # 聊天窗口 chat_window
    user_list = [toy_id,user_id]
    MongoDB.Chats.update_one({"_id":cha_window.inserted_id},{"$set":{"user_list":user_list}})
    # MongoDB.Users.update({"_id":ObjectId(toy_info.get("user_id"))},{"$set":{"bind_toys":toy_check.get("_id"),"friend_list":[friend_dict1]}})

    # 双方的关系
    # App可以与toy沟通
    # user[friend_list] toy_info[friend_list] 互相交换名片
    # 名片 = ？ user添加 toy 的名片到friend_list

    # friend_chat 私聊窗口id
    # chat_window = MongoDB.Chats.insert_one({user_list:[appid toyid],chat_list=[]})

    """
    toy添加App为好友
    """
    print(toy_info)
    RET["CODE"] = 0
    RET["MSG"] = "绑定完成"
    RET["DATA"] = {}
    return jsonify(RET)


@devices.route("/toy_list", methods=['POST'])
def toy_list():
    # 拿到用户的id
    user_id = request.form.get("_id")
    user_bind_toy_list = list(MongoDB.Toys.find({"bind_user":user_id}))
    for index,item in enumerate(user_bind_toy_list):
        user_bind_toy_list[index]["_id"] = str(item.get("_id"))
    RET["CODE"] = 0
    RET["MSG"] = "获取toy列表"
    RET["DATA"] = user_bind_toy_list
    return jsonify(RET)
    # return "200 ok"