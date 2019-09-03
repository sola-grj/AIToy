import jieba
import gensim
from gensim import corpora
from gensim import models
from gensim import similarities

# l1 = ["你的名字是什么", "你今年几岁了", "你有多高你胸多大", "你胸多大"]
# a = "你今年多大了"
from Config import MongoDB

l1 = list(MongoDB.Content.find({})) # 从数据库中获取问题库
all_doc_list = []
for doc in l1:
    doc_list = list(jieba.cut_for_search(doc.get("title"))) # 把Content表中的歌曲名进行jieba处理，放在大的列表中
    all_doc_list.append(doc_list)


# 制作语料库
dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
lsi = models.LsiModel(corpus)  # 数据量小时相对精确，大了就非常的不精确 500万以内，LsiModel就是用来寻找、提取公共的搜索条件
index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))


def my_gensim_nlp(a):
    doc_test_list = list(jieba.cut_for_search(a))
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    sim = index[lsi[doc_test_vec]]
    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    if cc[0][0] >= 0.55:
        text = l1[cc[0][0]]

        return text