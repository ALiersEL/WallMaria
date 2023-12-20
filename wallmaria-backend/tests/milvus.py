from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType

connections.connect(
    alias='default',
    host='58.37.44.136',
    port='19530',
    user='root',
    password='Milvus',
)

collection = None

def create_collection():
    global collection
    # 定义字段
    image_id = FieldSchema(name="image_id", dtype=DataType.INT64, is_primary=True, auto_id=False)
    rating = FieldSchema(name="rating", dtype=DataType.VARCHAR, max_length=10)
    score = FieldSchema(name="score", dtype=DataType.INT64)
    date = FieldSchema(name="timestamp", dtype=DataType.INT64)
    feature_vector = FieldSchema(name="feature_vector", dtype=DataType.FLOAT_VECTOR, dim=768)

    # 创建 Collection schema
    schema = CollectionSchema(fields=[image_id, rating, score, date, feature_vector], description="Post collection")

    # 创建 Collection
    collection_name = "posts"
    collection = Collection(name=collection_name, schema=schema)

    print(f"Collection {collection_name} created successfully.")

def get_collection():
    global collection
    collection = Collection(name="posts")
    print(f"Collection {collection.name} loaded successfully.")

def insert_data():
    collection = Collection(name="posts")
    to_insert = {
        "image_id": [1, 2, 3],
        "rating": ["g", "s", "e"],
        "score": [1, 2, 3],
        "timestamp": [1, 2, 3],
        "feature_vector": [[0.0 for _ in range(768)] for _ in range(3)]
    }
    collection.insert(to_insert)

    print(f"Data inserted successfully.")

# create_collection()
collection = Collection(name="posts")
collection.load()
print(collection.num_entities)
# 删除所有数据
# collection.drop()


# insert_data()