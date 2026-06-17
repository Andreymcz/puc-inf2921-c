from __future__ import annotations

from fastapi import FastAPI

from ...infrastructure.database.session import create_tables
from .routers.citizen_posts import router


def create_app() -> FastAPI:
    app = FastAPI(title="Fala Gavea API", version="0.1.0")
    create_tables()
    app.include_router(router, prefix="/citizen_posts", tags=["citizen_posts"])
    return app


app = create_app()
