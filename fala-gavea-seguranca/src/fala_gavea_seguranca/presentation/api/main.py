from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ...infrastructure.database.session import create_tables
from .routers.chats import router as chats_router
from .routers.iluminacao import router as iluminacao_router
from .routers.security_reports import router as reports_router


def create_app() -> FastAPI:
    app = FastAPI(title="Fala Gávea - Segurança API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    create_tables()
    app.include_router(reports_router, prefix="/security_reports", tags=["security_reports"])
    app.include_router(chats_router, prefix="/chats", tags=["chats"])
    app.include_router(iluminacao_router, prefix="/iluminacao", tags=["iluminacao"])

    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")

        @app.get("/")
        def root() -> FileResponse:
            return FileResponse("static/index.html")

    except Exception:
        # static/ not present during tests — skip silently
        pass

    return app


app = create_app()
