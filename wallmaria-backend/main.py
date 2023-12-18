from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from motor.motor_asyncio import AsyncIOMotorClient

# from odmantic import AIOEngine, Model, Field, ObjectId

POST_DOC_TYPE = "posts"

datetime = str

app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017/")
database = client["wallmaria"]
post_collection = database["posts"]

@app.get("/")
async def root():
    return {"message": "Hello Maria"}

class Post(BaseModel):
    id: int
    created_at: datetime
    uploader_id: int
    score: int
    source: str
    image_width: int
    image_height: int
    file_url: str
    large_file_url: str
    preview_file_url: str

class PostInDB(Post):
    type: str = POST_DOC_TYPE
    id: int
    created_at: datetime
    uploader_id: int
    score: int
    source: str
    md5: str
    last_comment_bumped_at: datetime | None
    rating: str
    image_width: int
    image_height: int
    tag_string: str
    fav_count: int
    file_ext: str
    last_noted_at: datetime | None
    parent_id: int | None
    has_children: bool
    approver_id: int | None
    tag_count_general: int
    tag_count_artist: int
    tag_count_character: int
    tag_count_copyright: int
    file_size: int
    up_score: int
    down_score: int
    is_pending: bool
    is_flagged: bool
    is_deleted: bool
    tag_count: int
    updated_at: datetime
    is_banned: bool
    pixiv_id: int | None
    last_commented_at: datetime | None
    has_active_children: bool
    bit_flags: int
    tag_count_meta: int
    has_large: bool
    has_visible_children: bool
    media_asset: dict | None
    tag_string_general: str
    tag_string_character: str
    tag_string_copyright: str
    tag_string_artist: str
    tag_string_meta: str
    file_url: str
    large_file_url: str
    preview_file_url: str

@app.get("/posts/{id}", response_model=Post)
async def get_post_by_id(id: int):
    # post = await engine.find_one(PostInDB, PostInDB.id == id)
    # if post is None:
    #     raise HTTPException(404)
    # return Post(**post.model_dump())
    post = await post_collection.find_one({"id": id})
    if post is None:
        raise HTTPException(404)
    return Post(**post)

@app.get("/posts", response_model=list[Post])
async def get_posts(limit: int = 10, skip: int = 0):
    # query = PostInDB.rating == 'g' or PostInDB.rating == 'e'
    # posts = await engine.find(PostInDB, query, limit=limit, skip=skip)
    # return [Post(**post.model_dump()) for post in posts]
    posts = await post_collection.find().to_list(length=limit)
    return [Post(**post) for post in posts]