import json
import os
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH, CHAT_PATH, RDB
from redis_msg import get_msg_one, get_msg_all

user = Blueprint("user",__name__)

@user.route("/reg",methods=["POST"])
def reg():
    user_info = request.form.to_dict()
    user_info["avatar"] = "baba.jpg" if user_info.get("gender") == "2" else "mama.jpg"
    user_info["bind_toys"] = []
    user_info["friend_list"] = []
    MongoDB.Users.insert_one(user_info)
    RET["CODE"] = 0
    RET["MSG"] = "注册成功"
    RET["DATA"] = {}

    return jsonify(RET)

# @user.route("/login",methods=["POST"])
# def login():
#     user_dict = request.form.to_dict()
#     user_id = user_dict.get("_id")
#     user_info = MongoDB.Users.find_one(user_dict,{"password":0})
#
#     user_info["_id"] = str(user_info.get("_id"))
#
#     user_info["chat"] = {"count":0}
#     RET["CODE"] = 0
#     RET["MSG"] = "登陆成功"
#     RET["DATA"] = user_info
#     return jsonify(RET)
#
# @user.route("/auto_login",methods=["POST"])
# def auto_login():
#     user_dict = request.form.to_dict()
#
#
#     user_info["_id"] = ObjectId(user_info.pop("_id"))
#
#     user_dict = MongoDB.Users.find_one(user_info,{"password":0})
#
#     # chat_info = {}
#     # num_list = []
#     if user_dict:
#     # #
#     #     for friend_info in user_dict["friend_list"]:
#     #         num = get_msg_one(friend_info.get("friend_id"),user_id)
#     #         chat_info[friend_info.get("friend_id")] = num
#     #         num_list.append(num)
#     #     chat_info["count"] = sum(num_list)
#     #     print(chat_info)
#
#         # chat_info = RDB.get(str(user_dict.get("_id")))
#         # chat_info_dict = json.loads(chat_info)
#         # count = 0
#         # for i in chat_info_dict.values():
#         #     count += i
#         # chat_info_dict["count"] = count
#         user_dict["_id"] = str(user_dict.get("_id"))
#         user_dict["chat"] = {"count":0}
#         # user_dict["chat"] = chat_info
#         # print(chat_info_dict)
#         RET["CODE"] = 0
#         RET["MSG"] = "登陆成功"
#         RET["DATA"] = user_dict
#     else:
#         RET["CODE"] = 99
#         RET["MSG"] = "登陆失败"
#
#     return jsonify(RET)

@user.route("/login",methods=["POST"])
def login():
    user_dict = request.form.to_dict()
    user_info = MongoDB.Users.find_one(user_dict,{"password":0})
    user_info["_id"] = str(user_info.get("_id"))
    user_info["chat"] = get_msg_all(user_info["_id"])

    RET["CODE"] = 0
    RET["MSG"] = "登录成功"
    RET["DATA"] = user_info

    return jsonify(RET)


@user.route("/auto_login",methods=["POST"])
def auto_login():
    user_dict = request.form.to_dict()
    user_dict["_id"] = ObjectId(user_dict.get("_id"))
    user_info = MongoDB.Users.find_one(user_dict,{"password":0})
    user_info["_id"] = str(user_info.get("_id"))
    user_info["chat"]= get_msg_all(user_info["_id"])
    RET["CODE"] = 0
    RET["MSG"] = "登录成功"
    RET["DATA"] = user_info

    return jsonify(RET)