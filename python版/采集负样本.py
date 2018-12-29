# encoding: utf-8
import random
# items: 用户有过行为的物品
#items_pool:候选物品列表（一般选择热门的物品）
def RandomSelectNegativeSample(self,items,items_pool):
    # ret 物品:是否感兴趣(0:正样本 1:负样本)
    ret = dict()
    for i in items.keys():
        ret[i] = 1
    n = 0
    # 为了保证正负样本数尽量一致 取len(items)*3个物品
    for i in range(0, len(items)*3):
        # 随机取一个热门物品
        item = items_pool[random.randint(0, len(items_pool) - 1)]
        if item in items:
            continue
        ret[item] = 0
        n += 1
        if n > len(items):
            break
    return ret
