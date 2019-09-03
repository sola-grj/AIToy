import os

import requests
from Config import LT_URL,QRCODE_PATH,MongoDB
from uuid import uuid4
import time,hashlib
# 创建 二维码


def create_qr(count):
    DeviceKey_list = []
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
        device_key = {
            "device_key":DeviceKey
        }
        DeviceKey_list.append(device_key)
        # 再将对应的二维码的值存到数据库中
    MongoDB.Devices.insert_many(DeviceKey_list)
# 存放在数据库中

create_qr(5)