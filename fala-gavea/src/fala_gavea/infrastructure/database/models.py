from sqlalchemy import JSON, Column, DateTime, Enum as SAEnum, ForeignKey, Integer, String

from .session import Base
from ...domain.entities.citizen_post import TerritoryLevel


class CitizenPostModel(Base):
    __tablename__ = "citizen_posts"

    id = Column(String, primary_key=True)
    text = Column(String, nullable=False)
    territory_level = Column(SAEnum(TerritoryLevel), nullable=False)
    territory_name = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    ai_labels = Column(JSON, nullable=False, default=list)
    label_feedback = Column(JSON, nullable=False, default=dict)
    likes_count = Column(Integer, nullable=False, default=0)


class LikeModel(Base):
    __tablename__ = "likes"

    user_id = Column(String, nullable=False, primary_key=True)
    post_id = Column(String, ForeignKey("citizen_posts.id"), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False)
