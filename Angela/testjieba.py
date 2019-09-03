import jieba
# 中文分词库
a = "先帝创业未半而中道崩殂"
b = "我想听小毛驴"

jieba.add_word("我想听") # 添加关键字，优先读取用户自定义库
res = list(jieba.cut(a))

res2 = list(jieba.cut_for_search(a))

res3 = list(jieba.cut(b))

res4 = list(jieba.cut_for_search(b))
print(res)
print(res2)
print(res3)
print(res4)


