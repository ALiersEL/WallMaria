from fastapi import FastAPI, HTTPException, UploadFile, File

from models import Post, PostInDB

from pymilvus import Collection

import database
from clip_loader import load_clip_model, extract_text_features, extract_image_features

import io
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
    posts = await post_mongo.find({"rating": {"$in": ["g", "s"]}}).limit(limit).skip(skip).to_list(length=limit)
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

    # 在 Milvus 中搜索相似的图片
    search_params = {
        "data": text_features,
        "anns_field": "feature_vector",
        "param": {"metric_type": "COSINE", "index_type": "IVF_FLAT"},
        "limit": top_k,
        "output_fields": ["image_id"]
    }
    results = post_milvus.search(**search_params)

    image_ids = [hit.id for hit in results[0]]

    # 在 MongoDB 中查询图片信息
    posts = await post_mongo.find({"id": {"$in": image_ids}}).to_list(length=top_k)
    # 根据 image_ids 的顺序对 posts 进行排序
    posts.sort(key=lambda post: image_ids.index(post["id"]))

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
    search_params = {
        "data": image_features,
        "anns_field": "feature_vector",
        "param": {"metric_type": "COSINE", "index_type": "IVF_FLAT"},
        "limit": top_k,
        "output_fields": ["image_id"]
    }
    results = post_milvus.search(**search_params)

    image_ids = [hit.id for hit in results[0]]

    # 在 MongoDB 中查询图片信息
    posts = await post_mongo.find({"id": {"$in": image_ids}}).to_list(length=top_k)
    # 根据 image_ids 的顺序对 posts 进行排序
    posts.sort(key=lambda post: image_ids.index(post["id"]))

    return posts