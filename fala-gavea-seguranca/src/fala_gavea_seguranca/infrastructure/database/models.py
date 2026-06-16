from sqlalchemy import Column, DateTime, Enum as SAEnum, Float, ForeignKey, JSON, String, Text

from .session import Base
from ...domain.entities.security_report import ReportCategory, ReportStatus


class SecurityReportModel(Base):
    __tablename__ = "security_reports"

    id = Column(String, primary_key=True)
    text = Column(String, nullable=False)
    category = Column(SAEnum(ReportCategory), nullable=False)
    status = Column(SAEnum(ReportStatus), nullable=False, default=ReportStatus.PENDENTE)
    author_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    territory_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    ai_labels = Column(JSON, nullable=False, default=list)


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    sources = Column(JSON, nullable=False, default=list)
