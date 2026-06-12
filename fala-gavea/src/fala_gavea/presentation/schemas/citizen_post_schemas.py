from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator


class CitizenPostCreate(BaseModel):
    text: str
    territory_level: str
    territory_name: str
    author_id: str

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text must not be empty")
        return v


class CitizenPostResponse(BaseModel):
    id: str
    text: str
    territory_level: str
    territory_name: str
    author_id: str
    created_at: datetime
    ai_labels: list[str]
    label_feedback: dict[str, dict]
    likes_count: int

    model_config = {"from_attributes": True}


class BulkCitizenPostsCreate(BaseModel):
    items: list[CitizenPostCreate]


class BulkCitizenPostsResponse(BaseModel):
    items: list[CitizenPostResponse]


class LikeRequest(BaseModel):
    user_id: str


class LikeResponse(BaseModel):
    post_id: str
    liked: bool
    likes_count: int


class LabelFeedbackRequest(BaseModel):
    label: str
    approved: bool
    user_id: str


class AiLabelsRequest(BaseModel):
    labels: list[str]


class LikeRecordResponse(BaseModel):
    user_id: str
    created_at: datetime


class PostLikesResponse(BaseModel):
    post_id: str
    likers: list[LikeRecordResponse]
