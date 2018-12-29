# encoding: utf-8
import math
import operator
# def ItemSimilarity(train):
#     C = dict()
#     N = dict()
#     for _, items in train.items():
#         for i in items:
#             if N. has_key(i) == False:
#                 N[i] = 0
#             N[i] += 1
#             for j in items:
#                 if i == j:
#                     continue
#                 if C. has_key(i) == False:
#                     C[i] = dict()
#                 if C[i]. has_key(j) == False:
#                     C[i][j] = 0
#                 C[i][j] += 1
#                 # # 惩罚过于活跃的用户
#                 # C[i][j] += 1 / math.log(1 + len(items) * 1.0)
#     print "用户-物品倒排表"
#     #     a   b   c   d   e
#     # a       1       2
#     # b   1       2   2   1
#     # c       2       2   1
#     # d   2   2   2
#     # e       1     1
#     print C
#     W  = dict()    # {'a': {'b': 1, 'd': 2}, 'c': {'b': 2, 'e': 1, 'd': 2}, 'b': {'a': 1, 'c': 2, 'e': 1, 'd': 2}, 'e': {'c': 1, 'b': 1}, 'd': {'a': 2, 'c': 2, 'b': 2}}
#     for i, related_items in C.items():
#         for j, cij in related_items.items():
#             if W. has_key(i) == False:
#                 W[i] = dict()
#             if W[i]. has_key(j) == False:
#                 W[i][j] = 0
#             W[i][j] = cij / math.sqrt(N[i] * N[j])
#     return W
# train = {"A": ["a", "b", "d"], "B": ["b", "c", "e"], "C": ["c", "d"], "D": ["c", "d", "b"], "E": ["a", "d"]}
# w = ItemSimilarity(train)
# print w

train = {"A": ["a", "b", "d"], "B": ["b", "c", "e"], "C": ["c", "d"], "D": ["c", "d", "b"], "E": ["a", "d"]}
# w = ItemSimilarity(train)
# print w
print "物品相似度归一化"
def ItemSimilarity2(train):
    C = dict()
    N = dict()
    for _, items in train.items():
        for i in items:
            if N. has_key(i) == False:
                N[i] = 0
            N[i] += 1
            for j in items:
                if i == j:
                    continue
                if C. has_key(i) == False:
                    C[i] = dict()
                if C[i]. has_key(j) == False:
                    C[i][j] = 0
                C[i][j] += 1
                # # 惩罚过于活跃的用户
                # C[i][j] += 1 / math.log(1 + len(items) * 1.0)
    print "用户-物品倒排表"
    #     a   b   c   d   e
    # a       1       2
    # b   1       2   2   1
    # c       2       2   1
    # d   2   2   2
    # e       1     1
    print C
    W  = dict()    # {'a': {'b': 1, 'd': 2}, 'c': {'b': 2, 'e': 1, 'd': 2}, 'b': {'a': 1, 'c': 2, 'e': 1, 'd': 2}, 'e': {'c': 1, 'b': 1}, 'd': {'a': 2, 'c': 2, 'b': 2}}
    for i, related_items in C.items():
        Max = 0
        for j, cij in related_items.items():
            if W. has_key(i) == False:
                W[i] = dict()
            if W[i]. has_key(j) == False:
                W[i][j] = 0
            W[i][j] = cij / math.sqrt(N[i] * N[j])
            if W[i][j] > Max:
                Max = W[i][j]
        if Max != 0:
            W[i] = norm(W[i], Max)
    return W
# 物品相似度归一化
def norm(wi,Max):
    res = dict()
    for j, value in wi. items():
        res[j] = value/Max
    return res
w = ItemSimilarity2(train)
print w
print "=======Recommendation========"

def Recommendation(train,user_id,W,K):
    rank = dict()
    ru = train[user_id]
    for i in ru:
        for j, wj in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            if rank. has_key(j) == False:
                rank[j] = 0
            pi = 1
            rank[j] += pi * wj
    return rank
print Recommendation(train, "A", w, 20)

# print "=======Recommendation 对推荐解释========"
# class Item:
#     pass
# def Recommendation2(train,user_id,W,K):
#     rank = dict()
#     ru = train[user_id]
#     for i in ru:
#         for j, wj in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
#             if j in ru:
#                 continue
#             if rank. has_key(j) == False:
#                 rank[j] = Item()
#                 rank[j].weight = 0
#                 rank[j].reason = dict()
#             pi = 1
#             rank[j].weight += pi * wj
#             rank[j].reason[i] = pi * wj
#     return rank
# recommand = Recommendation2(train, "C", w, 10)
# for i, item in recommand.items():
#     print i, item.weight, item.reason
