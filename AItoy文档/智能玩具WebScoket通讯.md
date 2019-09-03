# 智能玩具WebSocket通讯

## App通讯

#### WebSocket连接地址:

ws://10.0.0.1:9528/app/<user_id>

##### 向Toy推送音乐:

```json
JSON:
{
	to_user: toy_id,	// 接收音乐的方ID
    music: music_name	// 发送的音乐名称
}
```

##### 向Toy推送语音消息:

```json
JSON:
{
    chat: chat_file_name, // 语音文件名
    to_user: toy_id, // 接收语音消息方ID
    from_user: user_id // 发送语音消息方ID
}
```

##### 接收Toy发送的语音消息:

```json
JSON:
{
    chat: chat_file_name, // 语音文件名
    to_user: toy_id, // 接收语音消息方ID
    from_user: user_id // 发送语音消息方ID
}
```



## Toy通讯

#### WebSocket连接地址:

ws://10.0.0.1:9528/toy/<toy_id>

##### 接收App推送音乐:

```json
JSON:
{
	to_user: toy_id,	// 接收音乐的方ID
    music: music_name	// 发送的音乐名称
}
```

##### 接收App推送语音消息:

```json
JSON:
{
    chat: ["chat","chat"], // 语音文件名列表
    to_user: toy_id, // 接收语音消息方ID
    from_user: user_id // 发送语音消息方ID
}
```

##### 向App推送语音消息:

```json
JSON:
{
    chat: chat_file_name, // 语音文件名
    to_user: toy_id, // 接收语音消息方ID
    from_user: user_id // 发送语音消息方ID
}
```

