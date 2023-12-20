from fastapi import FastAPI, HTTPException

from motor.motor_asyncio import AsyncIOMotorClient

from models import Post, PostInDB

# from odmantic import AIOEngine, Model, Field, ObjectId

app = FastAPI()

client = AsyncIOMotorClient("mongodb://root:wallmaria_root@localhost:27017/")
database = client["wallmaria"]
post_collection = database["posts"]

@app.get("/")
async def root():
    return {"message": "Hello Maria"}

@app.get("/posts/{id}", response_model=Post)
async def get_post_by_id(id: int):
    post = await post_collection.find_one({"id": id})
    if post is None:
        raise HTTPException(404)
    return Post(**post)

@app.get("/posts", response_model=list[Post])
async def get_posts(limit: int = 10, skip: int = 0):
    posts = await post_collection.find({"rating": {"$in": ["g", "s"]}}).limit(limit).skip(skip).to_list(length=limit)
    return posts