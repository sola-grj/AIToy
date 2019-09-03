from pypinyin import lazy_pinyin,TONE,TONE2,TONE3

a = "我要给媛媛发消息"
b = "我要给圆圆发消息"
c = "我要给苑苑发消息"
resa = lazy_pinyin(a,style=TONE)
print(resa)
resb = lazy_pinyin(b,style=TONE2)
print(resb)
resc = lazy_pinyin(c,style=TONE3)
print(resc)