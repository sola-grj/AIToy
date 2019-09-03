import json

from Config import RDB

# 设置未读消息，在哪设置？
# sender向receiver发起消息时，向receiver的数据中+1 或者创建
def set_msg(sender,receiver):
    # 1.判断当前有没有这个receiver的数据
    msg_count = RDB.get(receiver)
    # 如果从redis数据库中查找到了对应的数据
    if msg_count:
        # 首先进行反序列化，拿到我们存储数据的字典
        msg_count_dict = json.loads(msg_count)
        # 判断sender是不是第一个发消息的人，如果是则对该sender的count进行+1
        if msg_count_dict.get(sender):
            msg_count_dict[sender] += 1
        # 如果sender发消息的话，那么就先设置他发过来的消息为第一条消息
        else:
            msg_count_dict[sender] = 1
        # 在把字典序列化
        msg_count = json.dumps(msg_count_dict)
    # 没有查到的时候就进行创建对应的字典数据结构
    else:
        msg_count = json.dumps({sender: 1})
    # 在数据库中再次进行更新
    RDB.set(receiver, msg_count)

    # 2.当receiver收到sender的消息，对应当前的sender +1




# 获取未读消息
def get_msg_one(sender,receiver):
    # 从数据库中查找数据
    msg_count = RDB.get(receiver)
    # 如果找到了
    if msg_count:
        # 进行反序列化
        msg_count_dict = json.loads(msg_count)
        # 取出里面对应sender的发消息的数量
        count = msg_count_dict.get(sender,0)
        # 当上一个sender所发的消息为0的时候
        if count == 0:
            # 对消息的字典进行遍历
            for k,v in msg_count_dict.items():
                # 如果其中的消息数量不为0的话
                if v != 0:
                    # 我们把此时的sender换成当前有消息的sender
                    sender = k
                    # 把数量也进行替换
                    count = v
        # 把对应的sender中的count设置为0
        msg_count_dict[sender] = 0
    # 如果在数据库中并没有查到
    else:
        # 设置数据结构
        msg_count_dict = {sender:0}
        count = 0
    RDB.set(receiver,json.dumps(msg_count_dict))

    return count,sender

def get_msg_all(receiver):
    # 从数据库中查询sender发的消息
    msg_count = RDB.get(receiver)
    # 设置一个字典
    msg_count_dict = {"count":0}
    if msg_count:
        msg_count_dict = json.loads(msg_count)
        # 把count的值进行求和
        msg_count_dict["count"] = sum(msg_count_dict.values())

    return msg_count_dict