import jieba
import gensim
from gensim import corpora
from gensim import models
from gensim import similarities

# l1 = ["你的名字是什么", "你今年几岁了", "你有多高你胸多大", "你胸多大"]
# a = "你今年多大了"
from Config import MongoDB
l1 = list(MongoDB.Content.find({}))
a = "我想听祖国我爱你"

all_doc_list = []
for doc in l1:
    doc_list = list(jieba.cut_for_search(doc.get("title")))
    all_doc_list.append(doc_list)

print(all_doc_list)
doc_test_list = [word for word in jieba.cut(a)]

# 制作语料库
dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
# 词袋的理解
# 词袋就是将很多很多的词,进行排列形成一个 词(key) 与一个 标志位(value) 的字典
# 例如: {'什么': 0, '你': 1, '名字': 2, '是': 3, '的': 4, '了': 5, '今年': 6, '几岁': 7, '多': 8, '有': 9, '胸多大': 10, '高': 11}
# 至于它是做什么用的,带着问题往下看

print("token2id", dictionary.token2id)
print("dictionary", dictionary, type(dictionary))

corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
# 语料库:
# 这里是将all_doc_list 中的每一个列表中的词语 与 dictionary 中的Key进行匹配
# 得到一个匹配后的结果,例如['你', '今年', '几岁', '了']
# 就可以得到 [(1, 1), (5, 1), (6, 1), (7, 1)]
# 1代表的的是 你 1代表出现一次, 5代表的是 了  1代表出现了一次, 以此类推 6 = 今年 , 7 = 几岁
print("corpus", corpus, type(corpus))

# 将需要寻找相似度的分词列表 做成 语料库 doc_test_vec
doc_test_vec = dictionary.doc2bow(doc_test_list)
print("doc_test_vec", doc_test_vec, type(doc_test_vec))

# 将corpus语料库(初识语料库) 使用Lsi模型进行训练
lsi = models.LsiModel(corpus) # 数据量小时相对精确，大了就非常的不精确 500万以内，LsiModel就是用来寻找、提取公共的搜索条件
# 这里的只是需要学习Lsi模型来了解的,这里不做阐述
print("lsi", lsi, type(lsi))
# 语料库corpus的训练结果
print("lsi[corpus]", lsi[corpus])
# 获得语料库doc_test_vec 在 语料库corpus的训练结果 中的 向量表示
print("lsi[doc_test_vec]", lsi[doc_test_vec])

# 文本相似度
# 稀疏矩阵相似度 将 主 语料库corpus的训练结果 作为初始值
index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))
print("index", index, type(index))

# 将 语料库doc_test_vec 在 语料库corpus的训练结果 中的 向量表示 与 语料库corpus的 向量表示 做矩阵相似度计算
sim = index[lsi[doc_test_vec]]

print("sim", sim, type(sim))

# 对下标和相似度结果进行一个排序,拿出相似度最高的结果
# cc = sorted(enumerate(sim), key=lambda item: item[1],reverse=True)
cc = sorted(enumerate(sim), key=lambda item: -item[1])
print(cc)

text = l1[cc[0][0]]

print(a,text)