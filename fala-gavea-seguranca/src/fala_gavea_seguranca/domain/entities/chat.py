from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChatSession:
    id: str
    title: str
    created_at: datetime


@dataclass
class ChatMessage:
    id: str
    session_id: str
    role: str  # "user" | "assistant"
    content: str
    created_at: datetime
    sources: list[dict] = field(default_factory=list)
