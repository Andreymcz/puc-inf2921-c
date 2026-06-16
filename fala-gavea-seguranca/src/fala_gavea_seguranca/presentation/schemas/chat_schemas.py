from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ChatSessionCreate(BaseModel):
    title: str


class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
    sources: list[dict]

    model_config = {"from_attributes": True}


class InsightPointResponse(BaseModel):
    session_id: str
    text: str
    x: float
    y: float
