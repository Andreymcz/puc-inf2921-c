from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from fala_gavea_seguranca.application.use_cases.chat_use_cases import (
    CreateChatSession,
    CreateChatSessionInput,
    GetChatMessages,
    GetChatSession,
    ListChatSessions,
)
from fala_gavea_seguranca.application.use_cases.get_chat_insights import GetChatInsights
from fala_gavea_seguranca.application.use_cases.send_chat_message import SendChatMessage, SendChatMessageInput
from fala_gavea_seguranca.infrastructure.repositories.sqlalchemy_chat_repository import (
    SQLAlchemyChatMessageRepository,
    SQLAlchemyChatSessionRepository,
)
from fala_gavea_seguranca.presentation.api.dependencies import get_chat_message_repo, get_chat_session_repo
from fala_gavea_seguranca.presentation.schemas.chat_schemas import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    InsightPointResponse,
)

router = APIRouter()


@router.post("/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    body: ChatSessionCreate,
    repo: SQLAlchemyChatSessionRepository = Depends(get_chat_session_repo),
) -> ChatSessionResponse:
    entity = CreateChatSession(repo).execute(CreateChatSessionInput(title=body.title))
    return ChatSessionResponse(**entity.__dict__)


@router.get("/", response_model=list[ChatSessionResponse])
def list_chat_sessions(
    repo: SQLAlchemyChatSessionRepository = Depends(get_chat_session_repo),
) -> list[ChatSessionResponse]:
    return [ChatSessionResponse(**s.__dict__) for s in ListChatSessions(repo).execute()]


@router.get("/insights", response_model=list[InsightPointResponse])
def get_insights(
    session_ids: list[str] = Query(default=[]),
    msg_repo: SQLAlchemyChatMessageRepository = Depends(get_chat_message_repo),
) -> list[InsightPointResponse]:
    try:
        points = GetChatInsights(msg_repo).execute(session_ids=session_ids or None)
        return [InsightPointResponse(**p.__dict__) for p in points]
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/{session_id}", response_model=ChatSessionResponse)
def get_chat_session(
    session_id: str,
    repo: SQLAlchemyChatSessionRepository = Depends(get_chat_session_repo),
) -> ChatSessionResponse:
    entity = GetChatSession(repo).execute(session_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    return ChatSessionResponse(**entity.__dict__)


@router.get("/{session_id}/messages", response_model=list[ChatMessageResponse])
def get_chat_messages(
    session_id: str,
    msg_repo: SQLAlchemyChatMessageRepository = Depends(get_chat_message_repo),
) -> list[ChatMessageResponse]:
    return [ChatMessageResponse(**m.__dict__) for m in GetChatMessages(msg_repo).execute(session_id)]


@router.post("/{session_id}/messages", response_model=list[ChatMessageResponse])
def send_message(
    session_id: str,
    body: ChatMessageCreate,
    session_repo: SQLAlchemyChatSessionRepository = Depends(get_chat_session_repo),
    msg_repo: SQLAlchemyChatMessageRepository = Depends(get_chat_message_repo),
) -> list[ChatMessageResponse]:
    # Verify session exists
    if GetChatSession(session_repo).execute(session_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    try:
        user_msg, assistant_msg = SendChatMessage().execute(
            SendChatMessageInput(session_id=session_id, user_text=body.content, message_repo=msg_repo)
        )
        return [ChatMessageResponse(**user_msg.__dict__), ChatMessageResponse(**assistant_msg.__dict__)]
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
