import json
f1 = open('train.txt', 'rb+')
# users = {"user2": ["1", "2", "3"],
#          "user": ["1", "4", "3"]}
# j = json.dumps(users)
# f1.writelines(j)
# f1.seek(0, 0)
a = f1.read()
print a
# user = json.loads(a)
# print user["user"]
# print f1.read()
f1.close()
