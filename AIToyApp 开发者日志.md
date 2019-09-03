# AIToyApp 开发者日志

## 1.寻找与儿童成长、开发智力等相关的信息提供商

- 这时候我们找到了中国某知名内容提供商，通过获取对应的数据，并对数据进行数据分析

```python
import json
import os
import requests # 爬虫模块
from uuid import uuid4 # 随机生成对应的文件名称
from Config import COVER_PATH,MUSIC_PATH,MongoDB # 从配置文件导入对应的音乐文件夹路径、图片文件夹路径
DATA = '对应的数据'
# 由于数据里面的true和false没有大写，因此通过json来转换成对应的python格式
data = json.loads(DATA)
audio_list = data["data"]["tracksAudioPlay"]
print(audio_list)
res = requests.get("https://www.ximalaya.com/ertong/424529/",headers=header)

"""
trackName 歌曲名字
trackCoverPath 图片地址，需要加上HTTP协议头
albumName 专辑名称
src 歌曲内容地址
"""
content_list = []
for content_info in audio_list:
    # 构造自己所需要的内容字典
    content = {
        "title":content_info.get("trackName"),
        "album":content_info.get("albumName"),
        # 此时的图片和歌曲的暂时不提取爬取到的数据，原因是，图片缺少了对应的HTTP请求头，
        # 而歌曲是对应的网址，一旦喜马拉雅有所变动我们则没办法得到对应的数据，因此，把对应的属于依次下载到本地
        "cover":"",
        "music":"",
    }
    # 通过uuid4来获取随机的名字，让图片和歌曲的前缀名字可以一一对应得上
    file_name = uuid4()
    # 通过拼接HTTP请求头，来获取到每个歌曲对应的图片地址
    cover_res = requests.get("http:" + content_info.get("trackCoverPath"))
    cover_file_name = f"{file_name}.jpg"
    # 通过路径拼接，将图片数据保存在对应的Cover文件下
    cover_file_path = os.path.join(COVER_PATH,cover_file_name)
    with open(cover_file_path,"wb")as f:
        f.write(cover_res.content)

    music_res = requests.get(content_info.get("src"))
    music_file_name = f"{file_name}.mp3"
    music_file_path = os.path.join(MUSIC_PATH, music_file_name)
    with open(music_file_path, "wb")as f:
        f.write(music_res.content)
    content["cover"] = cover_file_name
    content["music"] = music_file_name

    content_list.append(content)



MongoDB.Content.insert_many(content_list)
```

## 2.对接前端app的接口

### 1./content_list 获取内容列表

```python
import os
from flask import Blueprint, jsonify, send_file
from Config import RET,MongoDB,COVER_PATH,MUSIC_PATH

content = Blueprint("content",__name__)
# 获取所有的数据，并展示到页面上
@content.route("/content_list",methods=["POST"])
def content_list():
    # 从数据库中查出所有的数据[{},{},{}]
    con_list = list(MongoDB.Content.find({}))
    # 使用枚举将"_id"变成str类型
    for index,cont in enumerate(con_list):
        con_list[index]["_id"] = str(cont.get("_id"))

    RET["CODE"] = 0
    RET["MSG"] = "获取内容资源列表"
    RET["data"] = con_list

    return jsonify(RET)

```

### 2./get_cover 和 /get_music 获取内容详情

这里使用到了动态参数路由

```python
# 从前端调用get_cover 以及 get_music 这两个方法分别获取到对应的音频和图片，在通过send_file发送给前端进行渲染
@content.route("/get_cover/<filename>",methods=["GET"])
def get_cover(filename):
    file_path = os.path.join(COVER_PATH,filename)
    return send_file(file_path)


@content.route("/get_music/<filename>",methods=["GET"])
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH,filename)
    return send_file(file_path)
```

### 3./reg 注册用户

在注册的时候，由于前端提交过来的user_info 不足以满足数据库中的字段需求，因此，自己继续向字典中进行赋值

```python
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
```

### 4./login 用户登录

在做用户登录的时候，不能讲密码频繁的传输于前后端，需要在传输时，对password进行忽略

```python
@user.route("/login",methods=["POST"])
def login():
    user_dict = request.form.to_dict()
    user_info = MongoDB.Users.find_one(user_dict,{"password":0}) # 传输时忽略password
    user_info["_id"] = str(user_info.get("_id"))

    RET["CODE"] = 0
    RET["MSG"] = "登陆成功"
    RET["DATA"] = user_info
    return jsonify(RET)

@user.route("/auto_login",methods=["POST"])
def auto_login():
    user_info = request.form.to_dict()
    print("*****",user_info)
    user_info["_id"] = ObjectId(user_info.pop("_id"))
    user_dict = MongoDB.Users.find_one(user_info,{"password":0})
    print("6666",user_dict)
    if user_dict:
        user_dict["_id"] = str(user_dict.get("_id"))
        RET["CODE"] = 0
        RET["MSG"] = "登陆成功"
        RET["DATA"] = user_dict
    else:
        RET["CODE"] = 99
        RET["MSG"] = "登陆失败"
    return jsonify(RET)
```

### 5./auto_login 用户的自动登录

自动登录的原理：首先在完成前端的加载的时候，对window.localStorage.getItem("user_id")进行判断，如果有对应的"user_id"，则直接去执行对应的/auto_login的函数

```html
mui.plusReady(function () {
			if(window.localStorage.getItem("user_id")){
				mui.post(window.serv + '/auto_login',{
						_id:window.localStorage.getItem("user_id")
				},function(data){ 
						user_info = data.DATA;
						console.log(JSON.stringify(user_info));
						document.getElementById("count").innerText = user_info.chat.count;
						create_ws(data.DATA._id);
					},'json'
				);
			}		    
		}) 
```

这个时候，把对应的"_id"传给了后端，通过全宇宙唯一的"id"取数据库中进行查询到对应的用户，如果查询到了，就把对应用户的信息传给了前端进行渲染

```python
@user.route("/auto_login",methods=["POST"])
def auto_login():
    user_info = request.form.to_dict()
    user_info["_id"] = ObjectId(user_info.pop("_id"))
    user_dict = MongoDB.Users.find_one(user_info,{"password":0})
    if user_dict:
        user_dict["_id"] = str(user_dict.get("_id"))
        RET["CODE"] = 0
        RET["MSG"] = "登陆成功"
        RET["DATA"] = user_dict
    else:
        RET["CODE"] = 99
        RET["MSG"] = "登陆失败"
    return jsonify(RET)
```

### 6./scan_qr 扫描二维码

```python
import os

import requests
from Config import LT_URL,QRCODE_PATH,MongoDB
from uuid import uuid4
import time,hashlib
# 创建 二维码

DeviceKey_list = []
def create_qr(count):
    for i in  range(count):
        # 生成随机的二维码的内容，越复杂越好，保证不被破解
        DeviceKey = hashlib.md5(f"{uuid4()} {time.time()} {uuid4()}".encode("utf-8")).hexdigest()
        # 通过联图来获取二维码
        res = requests.get(LT_URL%(DeviceKey))
        # 对应的文件名
        qr_name = f"{DeviceKey}.jpg"
        #指定好路径
        qr_file_path = os.path.join(QRCODE_PATH,qr_name)
        # 将二维码写入到指定的文件中
        with open(qr_file_path,"wb")as f:
            f.write(res.content)
        # 再将对应的二维码的值存到数据库中
        MongoDB.Devices.insert_one({"device_key":DeviceKey})
# 存放在数据库中

create_qr(5)
```

在进行扫描的时候，有三种情况，文档中有对应的描述：

- 第一种是扫描成功，二维码还没有被绑定，
- 第二种情况，是扫描失败，对应的二维码并不在，
- 第三种情况是扫描成功，但是二维码已经被别人绑定好了

```python
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
```

### 7./bind_toy绑定玩具

1.创建Chats表：

在进行绑定玩具的时候，需要创建一个Toys的玩具表，但是有一个问题是：玩具表中并没有"friend_chat"，这个数据在Chats这个表中，就是这张表的"_id",因此我们可以先创建好这个Chats这张表

```python
# 创建Chats的聊天表
    chat_info = {
        "user_list": [],
        "chat_list": []
    }
    chat_info["user_list"].append(user_id)
    cha_window = MongoDB.Chats.insert_one(chat_info)
    chat_id = str(cha_window.inserted_id)
```

2.创建Toys表：

创建好了之后，我们就可以得到了"chat_id"把它放入到玩具表中的``friend_chat``，这时我们的Toys表也就创建好了，

```python
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
```

3.更新Users表

这样同时也就得到了"toy_id",然后再把"toy_id"更新到Users表中的"bind_toys",Users表中的通讯录信息也就可以得到了完善，里面的对应聊天的"friend_chat"也是"chat_id",这样Users表的数据也就完善好了，

```python
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
```

4.更新Chats表

最后，我们再把最开始创建的Chats这张表也进行完善，把对应的"user_id","toy_id"放入Chats表中的"user_list"中进行更新即可

```python
# 聊天窗口 chat_window
user_list = [toy_id,user_id]
MongoDB.Chats.update_one({"_id":cha_window.inserted_id},{"$set":{"user_list":user_list}})
```

### 8./toy_list 玩具列表

通过前端的传来的"_id"，找到对应的user_id,在从数据库中进行查找，把ObjectID转换成str类型即可

```python
@devices.route("/toy_list", methods=['POST'])
def toy_list():
    # 拿到用户的id
    user_id = request.form.get("_id")
    user_bind_toy_list = list(MongoDB.Toys.find({"bind_user":user_id}))
    for index,item in enumerate(user_bind_toy_list):
        print(index,item)
        user_bind_toy_list[index]["_id"] = str(item.get("_id"))
    RET["CODE"] = 0
    RET["MSG"] = "获取toy列表"
    RET["DATA"] = user_bind_toy_list
    return jsonify(RET)
```

### 9./get_qr 获取二维码的图片信息

```python
@content.route("/get_qr/<filename>",methods=["GET"])
def get_qr(filename):
    file_path = os.path.join(QRCODE_PATH,filename)
    return send_file(file_path)
```

