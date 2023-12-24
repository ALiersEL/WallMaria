from fastapi import FastAPI, HTTPException, UploadFile, File

from models import Post, PostInDB, UploadResponse

from pymilvus import Collection

import database
from database import search_similar_images
from clip_loader import load_clip_model, extract_text_features, extract_image_features

import io
import uuid
import json
from PIL import Image
from utils import _transform
from config import config

# from odmantic import AIOEngine, Model, Field, ObjectId

app = FastAPI()

# MongoDB
mongodb = database.connect_mongo()
post_mongo = mongodb["posts"]

# Milvus
database.connect_milvus()
post_milvus = Collection(name="posts")

# Redis
redis_client = database.connect_redis()

# CLIP
# 检查 CUDA 是否可用
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
clip_model = load_clip_model(config["clip"]["path"], device=device)
transform = _transform(224)

@app.get("/")
async def root():
    return {"message": "Hello Maria"}

@app.get("/posts/{id}", response_model=Post)
async def get_post_by_id(id: int):
    post = await post_mongo.find_one({"id": id})
    if post is None:
        raise HTTPException(404)
    return Post(**post)

@app.get("/posts", response_model=list[Post])
async def get_posts(limit: int = 10, skip: int = 0):
    posts = await post_mongo.find({"rating": {"$in": ["g"]}}).sort("score", -1).limit(limit).skip(skip).to_list(length=limit)
    return posts

@app.get("/search_by_text", response_model=list[Post])
async def search_images_by_text(text: str, top_k: int = 5):
    """
    根据文本查询相似的图片。

    参数:
        text (str): 查询用的文本。
        top_k (int): 返回的相似图片数量。

    返回:
        list: 相似图片的 image_id 列表。
    """

    print("Searching for images similar to:", text)
    # 将文本编码为向量
    text_features = extract_text_features(clip_model, [text], device=device)

    image_ids = search_similar_images(post_milvus, text_features, 1, top_k)

    posts = await get_posts_from_ids(image_ids)

    return posts

@app.post("/search_by_image", response_model=list[Post])
async def search_images_by_image(file: UploadFile = File(...), top_k: int = 5):
    """
    根据图片查询相似的图片。

    参数:
        file (UploadFile): 上传的图片文件。
        top_k (int): 返回的相似图片数量。

    返回:
        list: 相似图片的 image_id 列表。
    """

    print("Searching for images similar to the uploaded image")

    # 读取图片并转换为 PIL.Image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # 应用预处理
    transformed_image = transform(image)

    # 提取图片特征
    image_features = extract_image_features(clip_model, [transformed_image], device=device)

    # 在 Milvus 中搜索相似的图片
    image_ids = search_similar_images(post_milvus, image_features, 1, top_k)

    posts = await get_posts_from_ids(image_ids)

    return posts

@app.post("/upload_text", response_model=UploadResponse)
async def upload_text(text: str):
    """
    上传文本并缓存特征，返回 token。
    """
    # 提取特征
    text_features = extract_text_features(clip_model, [text], device=device)

    # 序列化特征以便存储
    features_serialized = json.dumps(text_features.tolist())

    # 生成唯一 token 并存储特征
    token = str(uuid.uuid4())
    await redis_client.set(token, features_serialized, ex=3600)  # 设置1小时过期时间

    return {"token": token}

@app.post("/upload_image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片并缓存特征，返回 token。
    """
    # 读取并转换图片
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    transformed_image = transform(image)

    # 提取特征
    image_features = extract_image_features(clip_model, [transformed_image], device=device)

    # 序列化特征以便存储
    features_serialized = json.dumps(image_features.tolist())

    # 生成唯一 token 并存储特征
    token = str(uuid.uuid4())
    await redis_client.set(token, features_serialized, ex=3600)  # 设置1小时过期时间

    return {"token": token}

@app.get("/get_results", response_model=list[Post])
async def get_results(token: str, page: int = 1, page_size: int = 10):
    """
    使用 token 获取搜索结果的不同页。
    """
    # 从 Redis 获取特征
    features_serialized = await redis_client.get(token)
    if not features_serialized:
        raise HTTPException(status_code=404, detail="Token not found or expired")

    # 反序列化特征
    features = json.loads(features_serialized)

    # 在 Milvus 中搜索相似的图片
    image_ids = search_similar_images(post_milvus, features, page, page_size)

    posts = await get_posts_from_ids(image_ids)

    return posts

async def get_posts_from_ids(image_ids):
    # 在 MongoDB 中查询图片信息
    posts = await post_mongo.find({"id": {"$in": image_ids}}).to_list(length=len(image_ids))
    # 根据 image_ids 的顺序对 posts 进行排序
    posts.sort(key=lambda post: image_ids.index(post["id"]))
    return posts