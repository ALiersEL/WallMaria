from pydantic import BaseModel, Field
from bson import ObjectId

POST_DOC_TYPE = "posts"

datetime = str
# from datetime import datetime

class Post(BaseModel):
    id: int
    created_at: datetime
    uploader_id: int
    score: int
    source: str
    image_width: int
    image_height: int
    tag_string_character: str
    tag_string_copyright: str
    tag_string_artist: str
    file_url: str
    large_file_url: str
    preview_file_url: str

from typing import Any
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)

class PostInDB(Post):
    type: str = POST_DOC_TYPE
    p_id: PyObjectId | None = Field(alias="_id", default=None)
    md5: str
    last_comment_bumped_at: datetime | None
    rating: str
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

class UploadResponse(BaseModel):
    token: str

class TagInfo(BaseModel):
    type: str
    name: str
    preview_url: str
    source: str
    occurrences: int