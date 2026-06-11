from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from fala_gavea.application.use_cases.add_label_feedback import AddLabelFeedback, AddLabelFeedbackInput
from fala_gavea.application.use_cases.create_citizen_post import CreateCitizenPost, CreateCitizenPostInput
from fala_gavea.application.use_cases.delete_citizen_post import DeleteCitizenPost
from fala_gavea.application.use_cases.get_citizen_post import GetCitizenPost
from fala_gavea.application.use_cases.get_post_likes import GetPostLikes, GetPostLikesInput
from fala_gavea.application.use_cases.list_citizen_posts import ListCitizenPosts
from fala_gavea.application.use_cases.set_ai_labels import SetAiLabels, SetAiLabelsInput
from fala_gavea.application.use_cases.toggle_like import ToggleLike, ToggleLikeInput
from fala_gavea.domain.exceptions import CitizenPostNotFoundError, InvalidInputError
from fala_gavea.infrastructure.repositories.sqlalchemy_citizen_post_repository import (
    SQLAlchemyCitizenPostRepository,
)
from fala_gavea.presentation.api.dependencies import get_citizen_post_repo
from fala_gavea.presentation.schemas.citizen_post_schemas import (
    AiLabelsRequest,
    CitizenPostCreate,
    CitizenPostResponse,
    LabelFeedbackRequest,
    LikeRecordResponse,
    LikeRequest,
    LikeResponse,
    PostLikesResponse,
)

router = APIRouter()


@router.post("/", response_model=CitizenPostResponse, status_code=status.HTTP_201_CREATED)
def create_citizen_post(
    body: CitizenPostCreate,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> CitizenPostResponse:
    try:
        entity = CreateCitizenPost(repo).execute(
            CreateCitizenPostInput(
                text=body.text,
                territory_level=body.territory_level,
                territory_name=body.territory_name,
                author_id=body.author_id,
            )
        )
        return CitizenPostResponse(**entity.__dict__)
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/", response_model=list[CitizenPostResponse])
def list_citizen_posts(
    limit: int = 50,
    offset: int = 0,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> list[CitizenPostResponse]:
    entities = ListCitizenPosts(repo).execute(limit=limit, offset=offset)
    return [CitizenPostResponse(**e.__dict__) for e in entities]


@router.get("/{id}", response_model=CitizenPostResponse)
def get_citizen_post(
    id: str,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> CitizenPostResponse:
    try:
        entity = GetCitizenPost(repo).execute(id)
        return CitizenPostResponse(**entity.__dict__)
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_citizen_post(
    id: str,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> None:
    try:
        DeleteCitizenPost(repo).execute(id)
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{id}/likes", response_model=LikeResponse)
def toggle_like(
    id: str,
    body: LikeRequest,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> LikeResponse:
    try:
        entity = ToggleLike(repo).execute(ToggleLikeInput(post_id=id, user_id=body.user_id))
        liked = repo.has_liked(id, body.user_id)
        return LikeResponse(post_id=id, liked=liked, likes_count=entity.likes_count)
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{id}/likes", response_model=PostLikesResponse)
def get_post_likes(
    id: str,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> PostLikesResponse:
    try:
        records = GetPostLikes(repo).execute(GetPostLikesInput(post_id=id))
        return PostLikesResponse(
            post_id=id,
            likers=[LikeRecordResponse(user_id=r.user_id, created_at=r.created_at) for r in records],
        )
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{id}/ai_labels", response_model=CitizenPostResponse)
def set_ai_labels(
    id: str,
    body: AiLabelsRequest,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> CitizenPostResponse:
    try:
        entity = SetAiLabels(repo).execute(SetAiLabelsInput(post_id=id, labels=body.labels))
        return CitizenPostResponse(**entity.__dict__)
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{id}/label_feedback", response_model=CitizenPostResponse)
def add_label_feedback(
    id: str,
    body: LabelFeedbackRequest,
    repo: SQLAlchemyCitizenPostRepository = Depends(get_citizen_post_repo),
) -> CitizenPostResponse:
    try:
        entity = AddLabelFeedback(repo).execute(
            AddLabelFeedbackInput(post_id=id, label=body.label, approved=body.approved, user_id=body.user_id)
        )
        return CitizenPostResponse(**entity.__dict__)
    except CitizenPostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
