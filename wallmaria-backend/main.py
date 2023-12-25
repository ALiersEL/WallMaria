from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from models import Post, PostInDB, UploadResponse, TagInfo
from bson import ObjectId

import pymongo
from pymilvus import Collection

import database
import numpy as np
from database import search_similar_images
from clip_loader import load_clip_model, extract_text_features, extract_image_features

import io
import uuid
import json
import hashlib
from collections import Counter
from PIL import Image
from utils import _transform
from config import config

# from odmantic import AIOEngine, Model, Field, ObjectId

app = FastAPI()

# MongoDB
mongodb = database.connect_mongo()
post_mongo = mongodb["posts"]
search_mongo = mongodb["searches"]

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

@app.post("/search_by_image_dep", response_model=list[Post], deprecated=True)
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

@app.post("/upload_text_dep", response_model=UploadResponse, deprecated=True)
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

@app.post("/upload_image_dep", response_model=UploadResponse, deprecated=True)
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

@app.get("/get_results_dep", response_model=list[Post], deprecated=True)
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

@app.get("/search_by_text", response_model=list[Post])
async def search_by_text(text: str, page: int = 1, page_size: int = 10, neg_text: str = None, neg_weight: float = 0.5):
    """
    根据文本搜索相似的图片，并缓存文本特征。
    """
    # 使用文本内容作为 Redis 缓存的键
    features = await get_text_cache(text)
    neg_features = await get_text_cache(neg_text) if neg_text else None
    
    # 混合特征
    if neg_features is not None:
        features -= neg_weight * neg_features

    # 在 Milvus 中搜索相似的图片
    image_ids = search_similar_images(post_milvus, features, page, page_size)
    posts = await get_posts_from_ids(image_ids)
    return posts

@app.post("/upload_image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片并保存，返回一个唯一的 token。
    """
    image_data = await file.read()
    # Calculate MD5 hash
    md5_hash = hashlib.md5(image_data).hexdigest()
    # 插入图片到 MongoDB
    try:
        await search_mongo.insert_one({"md5_hash": md5_hash, "image_data": image_data})
    except pymongo.errors.DuplicateKeyError:
        pass
    return {"token": md5_hash}

@app.get("/searches/{token}", response_class=StreamingResponse)
async def get_search_image(token: str):
    """
    根据 token 返回图片文件。
    """
    try:
        image_record = await search_mongo.find_one({"md5_hash": token})
    except:
        raise HTTPException(status_code=404, detail="Invalid token")

    if not image_record:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(io.BytesIO(image_record["image_data"]), media_type="image/png")

@app.get("/search_by_crop", response_model=list[Post])
async def search_by_crop(token: str, left: int, top: int, width: int, height: int, page: int = 1, page_size: int = 10):
    """
    根据裁剪参数和 token 搜索相似的图片。
    """
    # 从 Redis 获取特征
    features = await get_crop_cache(token, left, top, width, height)

    # 在 Milvus 中搜索相似的图片
    image_ids = search_similar_images(post_milvus, features, page, page_size)
    posts = await get_posts_from_ids(image_ids)
    return posts

@app.get("/search_by_image_text", response_model=list[Post])
async def search_by_image_text(token: str, left: int, top: int, width: int, height: int, text: str, alpha: float = 0.5, page: int = 1, page_size: int = 10):
    """
    根据图片和文本搜索相似的图片。
    """
    image_features = await get_crop_cache(token, left, top, width, height)
    text_features = await get_text_cache(text)

    # 混合特征
    features = (1 - alpha) * image_features + alpha * text_features

    # 在 Milvus 中搜索相似的图片
    image_ids = search_similar_images(post_milvus, features, page, page_size)
    posts = await get_posts_from_ids(image_ids)
    return posts

@app.get("/predict_image_info", response_model=list[TagInfo])
async def predict_image_info(token: str, left: int, top: int, width: int, height: int, top_k: int = 10, threshold: float = 0.2):
    """
    提供图片信息的预测。
    """
    features = await get_crop_cache(token, left, top, width, height)
    image_ids = search_similar_images(post_milvus, features, page=1, page_size=top_k)
    posts = await get_posts_from_ids(image_ids)

    # 统计 tags 频率
    tag_counter = Counter()
    tag_type = {}
    for post in posts:
        # tag_string_character
        characters = post["tag_string_character"].split()
        tag_counter.update(characters)
        tag_type.update({character: "character" for character in characters})
        # tag_string_artist
        artists = post["tag_string_artist"].split()
        tag_counter.update(artists)
        tag_type.update({artist: "artist" for artist in artists})
        # tag_string_copyright
        copy_rights = post["tag_string_copyright"].split()
        tag_counter.update(copy_rights)
        tag_type.update({copy_right: "copyright" for copy_right in copy_rights})

    # 找出超过阈值的 tags
    total_count = len(posts)
    relevant_tags = [tag for tag, count in tag_counter.items() if count / total_count >= threshold]

    # 构建响应
    tag_infos = []
    for tag in relevant_tags:
        if tag == "original":
            continue
        # 找出包含该 tag 相似度最高的图片 & 实际上就是第一次出现的图片
        highest_similar_post = next(post for post in posts if tag in post["tag_string"])
        tag_infos.append(
            TagInfo(
                type=tag_type[tag],
                name=tag,
                preview_url=highest_similar_post["preview_file_url"],
                source=highest_similar_post["source"],
                occurrences=tag_counter[tag]
            )
        )

    # 按照 occurrences 降序排序
    tag_infos.sort(key=lambda tag_info: tag_info.occurrences, reverse=True)

    return tag_infos

async def get_posts_from_ids(image_ids):
    # 在 MongoDB 中查询图片信息
    posts = await post_mongo.find({"id": {"$in": image_ids}}).to_list(length=len(image_ids))
    # 遍历 posts，若存在 pixiv_id，把 source 替换为 pixiv.net/artworks/{pixiv_id}
    for post in posts:
        if post["pixiv_id"]:
            post["source"] = f"https://pixiv.net/artworks/{post['pixiv_id']}"
    # 根据 image_ids 的顺序对 posts 进行排序
    posts.sort(key=lambda post: image_ids.index(post["id"]))
    return posts

async def get_text_cache(text):
    # 检查 Redis 缓存
    cache_key = f"text_{text}"
    cached_features = await redis_client.get(cache_key)

    if cached_features is None:
        # 提取文本特征
        features = extract_text_features(clip_model, [text], device=device)

        # 将特征保存到 Redis
        await redis_client.set(text, json.dumps(features.tolist()), ex=3600)  # 例如，缓存 1 小时
    else:
        # 使用缓存的特征
        features = np.array(json.loads(cached_features))

    return features

async def get_crop_cache(token, left, top, width, height):
    # 检查 Redis 缓存
    cache_key = f"{token}_{left}_{top}_{width}_{height}"
    cached_features = await redis_client.get(cache_key)

    if cached_features is None:
        # 从 MongoDB 获取图片
        try:
            image_record = await search_mongo.find_one({"md5_hash": token})
        except:
            raise HTTPException(status_code=404, detail="Invalid token")

        if not image_record:
            raise HTTPException(status_code=404, detail="Image not found")

        image = Image.open(io.BytesIO(image_record["image_data"]))
        # 有界性检查
        if left < 0 or top < 0 or width < 0 or height < 0 or left + width > image.width or top + height > image.height:
            raise HTTPException(status_code=400, detail="Invalid crop parameters")
        # 执行裁剪和特征提取
        cropped_image = image.crop((left, top, left + width, top + height))
        transformed_image = transform(cropped_image)
        features = extract_image_features(clip_model, [transformed_image], device=device)

        # 将特征保存到 Redis
        await redis_client.set(cache_key, json.dumps(features.tolist()), ex=3600)  # 例如，缓存 1 小时
    else:
        # 使用缓存的特征
        features = np.array(json.loads(cached_features))

    return features
