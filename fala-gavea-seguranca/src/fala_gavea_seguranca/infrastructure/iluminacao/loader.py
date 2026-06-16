"""Download e cache local do dataset de iluminação pública (ArcGIS Hub)."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx

ARCGIS_GEOJSON_URL = (
    "https://opendata.arcgis.com/api/v3/datasets/"
    "5322126ff10e46249be878ddfd057cc5/downloads/data"
    "?format=geojson&spatialRefId=4326"
)
_DEFAULT_CACHE = Path(__file__).parents[4] / "data" / "iluminacao.geojson"

log = logging.getLogger(__name__)


def download_iluminacao(cache_path: Path = _DEFAULT_CACHE) -> None:
    """Baixa o GeoJSON de iluminação pública e salva no cache local."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    log.info("Baixando dataset de iluminação de %s ...", ARCGIS_GEOJSON_URL)
    with httpx.stream("GET", ARCGIS_GEOJSON_URL, follow_redirects=True, timeout=60) as r:
        r.raise_for_status()
        with cache_path.open("wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
    log.info("Dataset salvo em %s", cache_path)


def load_iluminacao_geojson(cache_path: Path = _DEFAULT_CACHE) -> dict:
    """Retorna o GeoJSON de iluminação como dict Python.

    Faz download automático se o cache não existir.
    """
    if not cache_path.exists():
        download_iluminacao(cache_path)
    with cache_path.open(encoding="utf-8") as f:
        return json.load(f)
