import os
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET,MongoDB,COVER_PATH,MUSIC_PATH,CHAT_PATH

toy = Blueprint("toy",__name__)

@toy.route("/open_toy",methods=["POST"])
def open_toy():
    device_key = request.form.get("device_key")
    print(device_key)
    RET = {}
    # return "200"
    # toys表中是否存在Toy的信息，用DeviceKey查询
    toy_info = MongoDB.Toys.find_one({"device_key":device_key})
    if toy_info:
        RET = {
            "code":0,
            "music":"Success.mp3",
            "toy_id":str(toy_info.get("_id")),
            "name":toy_info.get("toy_name")
        }
    else:
        is_device = MongoDB.Devices.find_one(device_key)
        if is_device:
            RET = {
                "code":1,
                "music":"Nobind.mp3"

            }
        else:
            RET = {
                "code": 2,
                "music": "Nolic.mp3"

            }
    print(RET)
    return jsonify(RET)



# 语音发送消息
# @toy.route("/app_uploader",methods=["POST"])
# def app_uploader():
#     msg_info = request.form.to_dict()
#     voice_info = request.files.get("reco_file")
#
#     voice_path = os.path.join(CHAT_PATH,voice_info.filename)
#     # os.system(f"ffmpeg -i {voice_path} {voice_path}.mp3")
#     voice_info.save(voice_path)
#     print(msg_info)
#     print(voice_info)
#     toy_id = msg_info.get("to_user")
#     toy_info = MongoDB.Toys.find_one({"_id":ObjectId(toy_id)})
#     print(toy_info)
#     data = {
#         "filename":voice_info.filename,
#         "friend_type":"app"
#     }
#     RET["CODE"] = 0
#     RET["MSG"] = "上传成功"
#     RET["DATA"] = data
#     return jsonify(RET)
#
#
# @toy.route("/recv_msg",methods=["POST"])
# def recv_msg():
#     msg_info = request.form.to_dict()
#     voice_msg = request.files.to_dict()
#     print("recv_info********",msg_info)
#     print(voice_msg)
#     return "200"

