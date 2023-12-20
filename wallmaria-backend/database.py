from motor.motor_asyncio import AsyncIOMotorClient
from pymilvus import connections, Collection

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