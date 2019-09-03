# 智能玩具 MongoDB 数据结构

#### 1.App用户数据表

##### 表名 : 

```
Users
```

##### 数据结构:

```json
{
	"_id" : ObjectId("5c9d8da3ea512d2048826260"),  //自动生成ID
	"username" : "asdf", //用户名
	"password" : "962012d09b8170d912f0669f6d7d9d07", //密码
	"nickname" : "DragonFire", // 用户昵称
	"gender" : "2", // 用户性别
	"avatar" : "baba.jpg", // 用户头像 男=="baba.jpg" 女=="mama.jpg"
	"bind_toys" : [ // 用户绑定的玩具ID(string)
		"5ca17c7aea512d26281bcb8d",
		"5ca17f85ea512d215cd9b079"
	], 
	"friend_list" : [ // 用户的通讯录列表
		{ // 通讯录信息
			"friend_id" : "5ca17c7aea512d26281bcb8d", // 好友id
			"friend_nick" : "背背", // 好友的昵称
			"friend_remark" : "臭屎蛋儿", // 好友备注
			"friend_avatar" : "toy.jpg", // 好友头像
			"friend_chat" : "5ca17c7aea512d26281bcb8c", // 私聊窗口ID 聊天数据表对应值
			"friend_type" : "toy" // 好友类型
		},
		{
			"friend_id" : "5ca17f85ea512d215cd9b079",
			"friend_nick" : "圆圆",
			"friend_remark" : "小粪球儿",
			"friend_avatar" : "toy.jpg",
			"friend_chat" : "5ca17f85ea512d215cd9b078",
			"friend_type" : "toy"
		}
	]
}
```



#### 2.玩具信息数据表

##### 表名 : 

```
Toys
```

##### 数据结构:

```json
{
	"_id" : ObjectId("5ca17f85ea512d215cd9b079"), // 自动生成ID
	"toy_name" : "小粪球儿", // 玩具的昵称
	"baby_name" : "圆圆", // 玩具主人的昵称
	"device_key" : "afc59916257ae8a2b6ccdfb9fd273373", // 玩具的设备编号
	"avatar" : "toy.jpg", // 玩具的头像固定值 "toy.jpg"
	"bind_user" : "5c9d8da3ea512d2048826260", // 玩具的绑定用户
	"friend_list" : [ // 玩具通讯录信息 
		{ // 与Users数据表 friend_list 结构相同
			"friend_id" : "5c9d8da3ea512d2048826260",
			"friend_nick" : "DragonFire",
			"friend_remark" : "爸爸",
			"friend_avatar" : "baba.jpg",
			"friend_chat" : "5ca17f85ea512d215cd9b078",
			"friend_type" : "app"
		},
		{
			"friend_id" : "5ca17c7aea512d26281bcb8d",
			"friend_nick" : "臭屎蛋儿",
			"friend_remark" : "蛋蛋的忧伤",
			"friend_avatar" : "toy.jpg",
			"friend_chat" : "5ca5e789ea512d2e544da015",
			"friend_type" : "toy"
		}
	]
}
```



#### 3.好友请求信息数据表

##### 表名: 

```
Request
```

##### 数据结构:

```json
{
	"_id" : ObjectId("5ca5bfbaea512d269449ed1b"), // 自动生成ID
	"add_user" : "5ca17c7aea512d26281bcb8d", // 发起好友申请方
	"toy_id" : "5ca17f85ea512d215cd9b079", // 收到好友申请方
	"add_type" : "toy", // 发起方的用户类型 app/toy
	"req_info" : "我是仇视单", // 请求信息
	"remark" : "园园", // 发起方对接收方的好友备注
	"avatar" : "toy.jpg", // 发起方的头像
	"nickname" : "背背", // 发起方的名称
	"status" : 1, // 请求状态 1同意 0未处理 2拒绝
	"toy_name" : "圆圆" // 接收方的名称
}
```



#### 4.设备信息数据表

##### 表名 :

```
Devices
```

##### 数据结构:

```json
{
	"_id" : ObjectId("5c9d9e72ea512d1ae49f002e"), // 自动生成ID
	"device_key" : "afc59916257ae8a2b6ccdfb9fd273373" // 设备的唯一编号 二维码信息
}
```



#### 5.幼教内容数据表

##### 表名 :

```
Content
```

##### 数据结构:

```JSON
{
	"_id" : ObjectId("5c9c53a7ea512d282495a499"), // 自动生成ID
	"music" : "2f1fe658-d018-4aaf-a088-bdaaeed29745.mp3", // 内容文件名
	"cover" : "2f1fe658-d018-4aaf-a088-bdaaeed29745.jpg", // 内容图像
	"title" : "一只哈巴狗" // 内容名称
}
```



#### 6.聊天信息数据表

##### 表名 : 

```
Chats
```

##### 数据结构:

```json
{
	"_id" : ObjectId("5ca5e789ea512d2e544da015"), //自动生成ID
	"user_list" : [ // 用户列表 数据此聊天窗口的用户
		"5ca17f85ea512d215cd9b079",
		"5ca17c7aea512d26281bcb8d"
	],
	"chat_list" : [ // 聊天内容列表
		{
			"from_user" : "5ca17c7aea512d26281bcb8d", // 信息发送方ID
			"to_user" : "5ca17f85ea512d215cd9b079", // 信息接收方ID
			"chat" : "c22b9edd-4e7a-4eee-94e7-b239a90b9b16.wav", // 语音消息文件名
			"createTime" : 1554376821.5634897 // 聊天创建时间
		}
    ]
}
```

