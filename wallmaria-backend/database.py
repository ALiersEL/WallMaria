from motor.motor_asyncio import AsyncIOMotorClient
from pymilvus import connections, Collection
from redis.asyncio import Redis

from config import config

def connect_mongo():
    # MongoDB
    client = AsyncIOMotorClient(config["mongo"]["url"])
    database = client[config["mongo"]["database"]]
    return database

def connect_milvus():
    # Milvus
    connections.connect(
        alias='default',
        host=config["milvus"]["host"],
        port=config["milvus"]["port"],
        user=config["milvus"]["user"],
        password=config["milvus"]["password"]
    )

def connect_redis():
    # Redis
    redis_client = Redis(host=config["redis"]["host"], port=config["redis"]["port"], password=config["redis"]["password"])
    return redis_client

def search_similar_images(milvus_client: Collection, features, page=1, page_size=10):
    """
    在 Milvus 中搜索相似的图片。

    参数:
        milvus_client (Collection): Milvus 的集合实例。
        features (list): 查询特征向量。
        page (int): 起始页码。
        page_size (int): 每页返回的结果数量。

    返回:
        list: 搜索结果，包含相似图片的 image_id。
    """
    offset = (page - 1) * page_size
    search_params = {
        "data": features,
        "anns_field": "feature_vector",
        "param": {"metric_type": "COSINE", "index_type": "IVF_FLAT", "offset": offset, "params": {"nprobe": 256}},
        "limit": page_size,
        "expr": "rating in ['g', 's']",
        "output_fields": ["image_id"]
    }

    results = milvus_client.search(**search_params)
    return [hit.id for hit in results[0]]  # 假设只对第一个查询的结果感兴趣