from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse

from fala_gavea_seguranca.infrastructure.iluminacao.loader import (
    _DEFAULT_CACHE,
    download_iluminacao,
    load_iluminacao_geojson,
)

router = APIRouter()


@router.get("/geojson")
def get_iluminacao_geojson() -> JSONResponse:
    """Retorna o GeoJSON do dataset de iluminação pública (cache local).

    Se o cache não existir, faz o download automaticamente.
    Retorna 503 se o download falhar.
    """
    try:
        geojson = load_iluminacao_geojson()
        return JSONResponse(content=geojson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Dataset de iluminação não disponível: {e}",
        )


@router.post("/refresh", status_code=status.HTTP_202_ACCEPTED)
def refresh_iluminacao(background_tasks: BackgroundTasks) -> dict:
    """Dispara re-download do dataset em background."""
    background_tasks.add_task(download_iluminacao, _DEFAULT_CACHE)
    return {"message": "Download iniciado em background."}
