from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['wallmaria']
collection = db['posts']

# 找到重复的键
pipeline = [
    {"$group": {
        "_id": "$id",  # 替换为您的唯一字段名
        "ids": {"$push": "$_id"},
        "count": {"$sum": 1}
    }},
    {"$match": {
        "count": {"$gt": 1}
    }}
]

duplicates = collection.aggregate(pipeline)

cnt = 0
for document in duplicates:
    duplicate_ids = document['ids']
    # 删除除第一个之外的所有重复项
    collection.delete_many({"_id": {"$in": duplicate_ids[1:]}})
    cnt += 1

print(f"Removed {cnt} duplicates.")
