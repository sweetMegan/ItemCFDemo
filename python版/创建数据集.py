# encoding: utf-8
import random
import pandas as pd
import operator
import time
import math
import json
# 生成训练集和测试集
def SplitData(data, M, k, seed):
    test = dict()
    train = dict()
    random.seed(seed)
    for user, item, ratings, createTime in data:
        # 随机产生一个测试集
        if random.randint(0, M) == k:
            if test .has_key(user) == False:
                test[user] = []
            test[user] .append(item)
        else:
            if train .has_key(user) == False:
                train[user] = []
            train[user] .append(item)
    return train, test

# df = pd.read_csv('ml-1m/ratings.dat', sep="::", names=['user_id', 'item_id', 'rating', 'titmestamp'], engine='python')
# print ("u.data")
# data = df.values.tolist()
# train, test = SplitData(data, 8, 2, 8)
f1 = open('train.txt', 'rb+')
# j = json.dumps(train)
# f1.writelines(j)
f1.seek(0, 0)
a = f1.read()
train = json.loads(a)
f1.close()
f = open('test.txt', 'rb+')
# j = json.dumps(test)
# f.writelines(j)
a = f.read()
test = json.loads(a)
f.close()
print len(train), len(test)
# print test[1]
# df_Test = pd.DataFrame(test)
# print df_Test.head()
# # 生成矩阵
def UserSimilarity(train):
    item_Users = dict()
    for u, items in train.items():
        for i in items:
            #         构建倒排表item_Users
            if i not in item_Users.keys():
                item_Users[i] = set()
            item_Users[i].add(u)
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
    W = dict()
    for u, related_users in C.items():
        for v, value in related_users.items():
            if W. has_key(u) == False:
                W[u] = dict()
            if W[u]. has_key(v) == False:
                W[u][v] = 0
            W[u][v] = value/math.sqrt(N[u]*N[v])
    return W
# print "开始生成矩阵",int(time.time())
# w = UserSimilarity(train)
# print "矩阵构建完成",int(time.time())
# print "矩阵写入文件",int(time.time())

fw = open('w.txt', 'rb+')
# j = json.dumps(w)
# fw.writelines(j)
# fw.seek(0, 0)
a = fw.read()
w = json.loads(a)
fw.close()

print "矩阵写入完成",int(time.time())
# a = sorted(w["1"].items(), key=operator.itemgetter(1), reverse=True)[0:10]
# for v,wuv in a:
#     print v,wuv
def GetRecommentdation(user, train, K):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(w[user].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
        if train .has_key(v):
            for i in train[v]:
                if i in interacted_items:
                    continue
                # rvi代表用户v对物品IDE兴趣，因为使用的是单一行为的隐反馈数据，所以所有的rvi=1
                # 如果是显示反馈数据，如点赞 需要获取rvi的值再与wuv相乘后的结果
                rvi = 1
                if rank.has_key(i) == False:
                    rank[i] = 0
                rank[i] += wuv * 1
                # for i, rvi in train[v].items():
                #     if i in interacted_items:
                #         rank[i] += wuv * rvi
    # 将结果降序排序
    res = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:K]
    return res
# 计算召回率
# 召回率：描叙有多少比例的用户-物品评分记录包含在最终的推荐列表中
def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        if test. has_key(user):
            tu = test[user]
            rank = GetRecommentdation(user, train, N)
            for item, pui in rank:
              if item in tu:
                 hit += 1
            all += len(tu)
    return hit / (all * 1.0)

# print "计算召回率",int(time.time())
# print Recall(train, test, 10)
# print "计算召回率完成",int(time.time())
# 计算准确率
# 准确率:描叙最终的推荐列表中有多少比例是发生过的用户-物品评分记录
def Precision(train,test,N):
    hit = 0
    all = 0
    for user in train.keys():
        if test. has_key(user):
            tu = test[user]
            rank = GetRecommentdation(user, train, N)
            for item, pui in rank:
                if item in tu:
                    hit += 1
            all += N
    return hit / (all * 1.0)

print "计算准确率",int(time.time())
print Precision(train, test, 10)
print "计算准确率结束",int(time.time())
