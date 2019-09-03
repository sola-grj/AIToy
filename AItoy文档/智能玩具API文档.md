# 智能玩具API文档

## 用户相关API

#### 用户注册:

用于App用户注册

URL地址:	 /reg
请求方式:	POST
请求协议:

```json
JSON:
{
	"username":username,
	"password":password,
	"nickname":nickname,
	"gender":gender,
	"avatar":avatar.jpg
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"注册成功",
	"data":{}
}
```



#### 用户登录:

用于App用户登录

URL地址:	 /login
请求方式:	POST 
请求协议: 

```json
JSON:
{
	"username":username,
	"password":password
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"登录成功",
	"data":
	{
        "_id" : "5c8f582f268d7942f44c6703",
        "username" : "DragonFire",
        "gender" : "2",
        "nickname" : "厉害了我的哥",
        "avatar" : "baba.jpg",
        "friend_list" : [],
        "bind_toy" : []
    }
}
```



#### 用户自动登录:

用于App打开时用户进行自动登录

URL地址:	 /auto_login
请求方式:	POST
请求协议:

```json
JSON:
{
    "_id" : "5c8f582f268d7942f44c6703"
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"登录成功",
	"data":
	{
		"_id" : "5c8f582f268d7942f44c6703",
        "username" : "DragonFire",
        "gender" : "2",
        "nickname" : "厉害了我的哥",
        "avatar" : "baba.jpg",
        "friend_list" : [],
        "bind_toy" : []
	}
}
```





## 内容相关API

#### 获取内容资源:

用于App首页内容资源获取

URL地址:	 /content_list
请求方式:	POST
请求协议:

```json
JSON:
{
    
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"获取内容资源列表",
	"data":
	[
		{
            "_id" : "5c8f58eb268d79173c97bac5",
            "music" : "21b61cc0-9292-4e51-bf58-72be8ee6f962.mp3",
            "cover" : "21b61cc0-9292-4e51-bf58-72be8ee6f962.jpg",
            "title" : "一只哈巴狗"
		},
		{
			"_id" : "5c8f58eb268d79173c97bac4",
            "music" : "aa523ebe-95f9-4641-9478-1663cc74c6a6.mp3",
            "cover" : "aa523ebe-95f9-4641-9478-1663cc74c6a6.jpg",
            "title" : "学习雷锋好榜样"
		}
	]
}
```



### 获取音乐资源

用于App/Toy播放内容

URL地址:	 /get_music/<musicname>.mp3
请求方式:	GET
请求协议:	无
响应数据:	数据流



### 获取图片资源

用于App获取图片资源

URL地址:	 /get_image/<imagename>.jpg
请求方式:	GET
请求协议:	无
响应数据:	数据流



### 获取语音消息资源

用于App/Toy播放语音消息

URL地址:	 /get_chat/<chatname>.mp3
请求方式:	GET
请求协议:	无
响应数据:	数据流



### 获取二维码图片资源

用于App获取二维码图片

URL地址:	 /get_qr/<qrname>.mp3
请求方式:	GET
请求协议:	无
响应数据:	数据流



## 音频上传相关API

#### App录制语音上传接口:

用于App录制语音消息上传

URL地址:	 /app_uploader
请求方式:	POST
请求协议:

```json
JSON:
{
    "to_user":to_user, //语音消息接收方
    "user_id":from_user, //语音消息发送方
    "reco_file":File, //语音文件
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"上传成功",
	"data":
	{
        "filename":"filename",
        "friend_type":"app"
	}
}
```

#### Toy录制语音上传接口:

用于Toy录制语音消息上传

URL地址:	 /toy_uploader
请求方式:	POST
请求协议:

```json
JSON:
{
    "to_user":to_user, //语音消息接收方
    "user_id":from_user, //语音消息发送方
    "friend_type":app/toy, //语音接收方的用户类型
    "reco":File, //语音文件
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"上传成功",
	"data":
	{
        "filename":"filename",
        "friend_type":"app"
	}
}
```

#### Toy录制语音上传AI接口:

用于Toy录制语音消息上传至AI接口

URL地址:	 /ai_uploader
请求方式:	POST
请求协议:

```json
JSON:
{
    "toy_id":toy_id, //Toy的Id
    "reco":File, //语音文件
}
```

响应数据:

```
JSON:
//1.ai响应播放音乐
{
    "from_user": "ai",
    "music": music_name
}
//2.ai响应语音消息
{
    "from_user": "ai", 
    "chat": filename
}
//3.ai响应主动发起消息
{
    "from_user":friend_id,
    "chat":filename,
    "friend_type":app/toy
}
```



## 语音消息相关API

#### App获取历史消息:

用于App获取历史消息

URL地址:	 /chat_list
请求方式:	POST
请求协议:

```json
JSON:
{
    "chat_id":chat_id, //聊天窗口Id
    "to_user":user_id, //App用户Id
    "from_user":friend_id, //接收消息方Id
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"查询聊天记录",
	"data":
	[
		{
			"from_user" : "5c8f582f268d7942f44c6703",
			"message" : "1552898221960.amr.mp3",
			"create_time" : 1552898225.2744157
		},
		{
			"from_user" : "5c8f5853268d7942f44c6705",
			"message" : "ba7462dd-62a5-460c-bfab-bb64edd7c983.wav",
			"create_time" : 1552899004.6702642
		}
	]
}
```

#### Toy接收未读消息:

用于Toy收到消息提醒后

URL地址:	 /recv_msg
请求方式:	POST
请求协议:

```json
JSON:
{
    "from_user":user_id/toy_id, //发送语音消息方Id
    "to_user":toy_id, //当前接收语音消息的toy_id
}
```

响应数据:

```
JSON:
[
    {
        "from_user" : "5c8f582f268d7942f44c6703",
        "message" : "1552898221960.amr.mp3",
        "create_time" : 1552898225.2744157
    },
    {
        "from_user" : "5c8f5853268d7942f44c6705",
        "message" : "ba7462dd-62a5-460c-bfab-bb64edd7c983.wav",
        "create_time" : 1552899004.6702642
    }
]
```

#### 

## 硬件设备及二维码相关API

#### App扫描二维码验证接口:

用于App扫描Toy对应二维码进行识别

URL地址:	 /scan_qr
请求方式:	POST
请求协议:

```json
JSON:
{
    "device_key":device_key, //app扫描二维码后获取到的device_key
}
```

响应数据:

```
JSON:
//1.二维码扫描成功并且设备未进行绑定
{
	"code":0,
	"msg":"二维码扫描成功",
	"data":
	{
        "device_key":device_key
	}
}

//2.二维码扫描失败,扫描的条码不是设备库中存在的
{
	"code":1,
	"msg":"请扫描玩具二维码",
	"data":{}
}

//3.二维码扫描成功,但设备已经进行绑定
{
	"code":2,
	"msg":"设备已经进行绑定",
	"data":
	{
        "toy_id":toy_id
	}
}
```

#### App绑定设备接口:

用于App绑定设备,并创建Toy信息

URL地址:	 /bind_toy
请求方式:	POST
请求协议:

```json
JSON:
{
    "toy_name":toy_name, //toy名称
    "baby_name":baby_name, //toy所属主人名称
    "remark":remark, //toy主人对App用户的称呼
    "user_id":user_id,//绑定Toy的App用户Id
    "device_key":device_key, //设备唯一编码device_key
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"绑定完成",
	"data":{}
}
```

#### App获取绑定Toy信息接口:

用于App获取已经绑定的设备和创建过Toy信息

URL地址:	 /toy_list
请求方式:	POST
请求协议:

```json
JSON:
{
    "_id":user_id //App用户Id
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"获取Toy列表",
	"data":
	[
		{
            "_id" : ObjectId("5bcdaaa6268d794ec8af3fa2"),
            "device_key" : "bc557bcc9570069a494a64eb38698d35",
            "bind_user" : "5bcda858268d796fc8d3e3de",
            "toy_name" : "蛋蛋",
            "avatar" : "toy.jpg",
            "baby_name" : "臭屎蛋儿",
            "gender" : "1",
            "friend_list" : [
                {
                    "friend_nickname" : "淫王",
                    "friend_avatar" : "girl.jpg",
                    "friend_remark" : "爸爸",
                    "friend_chat" : "5bcdaaa6268d794ec8af3fa1"
                }
            ]
        },
        {
            "_id" : ObjectId("5bcdaa6f268d794ec8af3fa0"),
            "device_key" : "a195ac8014fb069676835a78d300f8a3",
            "bind_user" : "5bcda858268d796fc8d3e3de",
            "toy_name" : "球球",
            "avatar" : "toy.jpg",
            "baby_name" : "小粪球儿",
            "gender" : "1",
            "friend_list" : [
                {
                    "friend_nickname" : "淫王",
                    "friend_avatar" : "girl.jpg",
                    "friend_remark" : "爸爸",
                    "friend_chat" : "5bcdaa6f268d794ec8af3f9f"
                }
            ]
        }
	]
}
```

#### 设备启动登录接口:

用于设备启动后验证身份信息

URL地址:	 /open_toy
请求方式:	POST
请求协议:

```json
JSON:
{
    "device_key":device_key, //设备中写定的DeviceKey
}
```

响应数据:

```
JSON:
//1.设备处于绑定状态,正常启动
{
	"code":0,
	"music":"Success.mp3",
	"toy_id":toy_id,
	"name":toy_name
}

//2.设备未绑定
{
	"code":2,
	"music":"Nolic.mp3"
}

//3.设备未授权
{
	"code":1,
	"music":"Nobind.mp3"
}
```

#### 

## 好友通讯录相关API

#### App获取好友列表接口:

用于App获取好友通讯录

URL地址:	 /friend_list
请求方式:	POST
请求协议:

```json
JSON:
{
    "_id":user_id, //app用户Id
}
```

响应数据:

```
JSON:
//1.二维码扫描成功并且设备未进行绑定
{
	"code":0,
	"msg":"好友查询",
	"data":
	[
    	{
			"friend_id" : "5c8f5853268d7942f44c6705",
			"friend_nick" : "小粪球儿",
			"friend_remark" : "圆圆",
			"friend_avatar" : "toy.jpg",
			"friend_chat" : "5c8f5853268d7942f44c6704",
			"friend_type" : "toy"
		}
	]
}
```

#### 添加好友请求接口:

用于请求添加好友

URL地址:	 /add_req
请求方式:	POST
请求协议:

```json
JSON:
{
    "req_user":req_user_id, //发送好友请求方Id
    "add_user":add_user_id, //被请求方Id
    "type":app/toy, //请求方客户端类型
    "req_info":"我是xxx", //请求内容信息
    "remark":remark //请求方 对 被请求方 的备注名称
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"添加好友请求成功",
	"data":{}
}
```

#### App好友请求列表查询接口:

用于App查询绑定Toy的好友请求

URL地址:	 /req_list
请求方式:	POST
请求协议:

```json
JSON:
{
    "_id":user_id, //app用户Id
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"查询好友请求",
	"data":
	[
		{
            "req_user":req_user_id, //发送好友请求方Id
            "add_user":add_user_id, //被请求方Id
            "type":app/toy, //请求方客户端类型
            "req_info":"我是xxx", //请求内容信息
            "remark":remark //请求方 对 被请求方 的备注名称
            "avatar":avatar.jpg // 请求方的头像
            "nickname":"nickname" // 请求方的昵称
            "status":0 // 请求状态 0待处理 1同意 2拒绝
            "toy_name":"toy_name" // 被请求方的昵称
		}
	]
}
```

#### App拒绝好友请求接口:

用于App拒绝绑定Toy被添加为好友

URL地址:	 /ref_req
请求方式:	POST
请求协议:

```json
JSON:
{
    "req_id":req_id //好友请求信息Id
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"拒绝添加好友",
	"data":{}
}
```

#### App同意好友请求接口:

用于App同意绑定Toy被添加为好友

URL地址:	 /acc_req
请求方式:	POST
请求协议:

```json
JSON:
{
    "req_id":req_id, //好友请求信息Id
    "remark":"friend_remark", //为请求方添加备注名称
}
```

响应数据:

```
JSON:
{
	"code":0,
	"msg":"同意添加好友",
	"data":{}
}
```

#### 