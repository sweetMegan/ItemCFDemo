# encoding: utf-8
import math
import operator
def UserSimilarity(train):
    item_Users = dict()
    for u, items in train.items():
        for i in items:
            #         构建倒排表item_Users
            if i not in item_Users.keys():
                item_Users[i] = set()
            item_Users[i].add(u)
    print item_Users #{'a': set(['A', 'B']), 'c': set(['B', 'D']), 'b': set(['A', 'C']), 'e': set(['C', 'D']), 'd': set(['A', 'D'])}

    #         构建矩阵
    C = dict()
    N = dict()
    for i, users in item_Users.items():
        for user in users:
            # 记录user浏览过的物品数量
            if N. has_key(user) == False:
                N[user] = 0
            N[user] += 1 #N["A"] = 3, N["B"] = 2, N["C"] = 2, N["D"] = 3
            # 构建矩阵
            for v in users:
                #
                # 1.C["A"] = {
                #
                # }
                #
                if C. has_key(user) == False:
                    C[user] = dict()
                # 2.C["A"]["A"] = 0
                if C[user]. has_key(v) == False:
                    C[user][v] = 0
                if user == v:
                    # C["A"]["A"] = 0
                    continue
                    # C["A"]["B"] = 1
                # 惩罚用户user和用户v共同兴趣列表中热门物品对他们相似度的影响
                C[user][v] += 1 / math.log(1+len(users))
    print C
    # 相似度矩阵
    # C[u][v]
   #    u
   # v      "A" "B" "C" "D"
   #   "A" value
   #   "B"
   #   "C"
   #   "D"
    W = dict()
    for u, related_users in C.items():
        for v, value in related_users.items():
            if W. has_key(u) == False:
                W[u] = dict()
            if W[u]. has_key(v) == False:
                W[u][v] = 0
                #
            W[u][v] = value/math.sqrt(N[u]*N[v])
    return W

train = {"A": ["a", "b", "d"], "B": ["a", "c"], "C": ["b", "e"], "D": ["c", "d", "e"]}
w = UserSimilarity(train)
a = sorted(w["A"].items(), key=operator.itemgetter(1), reverse=True)[0:10]
print a
print "==========Recommend============="
# 推荐物品
def Recommend(user,train,W,K):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(w[user].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
        print v, wuv
        for i in train[v]:
            if i in interacted_items:
                continue
            # rvi代表用户v对物品IDE兴趣，因为使用的是单一行为的隐反馈数据，所以所有的rvi=1
            # 如果是显示反馈数据，如点赞 需要获取rvi的值再与wuv相乘后的结果
            rvi = 1
            if rank. has_key(i) == False:
                    rank[i] = 0
            rank[i] += wuv * 1
        # for i, rvi in train[v].items():
        #     if i in interacted_items:
        #         rank[i] += wuv * rvi
    # 将结果降序排序
    res = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    return res

r = Recommend("A", train, w, 10)
print r
r = Recommend("B", train, w, 10)
print r

# /usr/local/Cellar/python@2/2.7.15_1/Frameworks/Python.framework/Versions/2.7/bin/python2.7 /Users/zhqmac/PycharmProjects/untitled3/用户协同过滤改进.py
# {'a': set(['A', 'B']), 'c': set(['B', 'D']), 'b': set(['A', 'C']), 'e': set(['C', 'D']), 'd': set(['A', 'D'])}
# {'A': {'A': 0, 'C': 0.9102392266268373, 'B': 0.9102392266268373, 'D': 0.9102392266268373}, 'C': {'A': 0.9102392266268373, 'C': 0, 'D': 0.9102392266268373}, 'B': {'A': 0.9102392266268373, 'B': 0, 'D': 0.9102392266268373}, 'D': {'A': 0.9102392266268373, 'C': 0.9102392266268373, 'B': 0.9102392266268373, 'D': 0}}
# ==========Recommend=============
# C 0.371603608184
# B 0.371603608184
# D 0.303413075542
# A 0.0
# [('c', 0.6750166837258342), ('e', 0.6750166837258342)]
# A 0.371603608184
# D 0.371603608184
# B 0.0
# [('d', 0.7432072163671103), ('b', 0.37160360818355515), ('e', 0.37160360818355515)]


