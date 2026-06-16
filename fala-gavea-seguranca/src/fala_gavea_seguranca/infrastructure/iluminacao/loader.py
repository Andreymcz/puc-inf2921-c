"""Download e cache local do dataset de iluminação pública (ArcGIS Hub)."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx

# ArcGIS Hub v3 API requires the layer-index suffix (_0) on the dataset ID.
# Primary URL uses hub.arcgis.com; fallback uses opendata.arcgis.com.
_DATASET_ID = "5322126ff10e46249be878ddfd057cc5_0"
ARCGIS_GEOJSON_URL = (
    f"https://hub.arcgis.com/api/v3/datasets/{_DATASET_ID}/downloads/data"
    "?format=geojson&spatialRefId=4326"
)
_ARCGIS_FALLBACK_URL = (
    f"https://opendata.arcgis.com/api/v3/datasets/{_DATASET_ID}/downloads/data"
    "?format=geojson&spatialRefId=4326"
)
_DEFAULT_CACHE = Path(__file__).parents[4] / "data" / "iluminacao.geojson"

log = logging.getLogger(__name__)


def download_iluminacao(cache_path: Path = _DEFAULT_CACHE) -> None:
    """Baixa o GeoJSON de iluminação pública e salva no cache local."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    urls = [ARCGIS_GEOJSON_URL, _ARCGIS_FALLBACK_URL]
    last_exc: Exception | None = None
    for url in urls:
        try:
            log.info("Baixando dataset de iluminação de %s ...", url)
            with httpx.stream("GET", url, follow_redirects=True, timeout=60) as r:
                r.raise_for_status()
                with cache_path.open("wb") as f:
                    for chunk in r.iter_bytes():
                        f.write(chunk)
            log.info("Dataset salvo em %s", cache_path)
            return
        except httpx.HTTPStatusError as exc:
            log.warning("URL %s retornou %s, tentando próxima...", url, exc.response.status_code)
            last_exc = exc
    raise RuntimeError(f"Não foi possível baixar o dataset de iluminação. Último erro: {last_exc}")


def load_iluminacao_geojson(cache_path: Path = _DEFAULT_CACHE) -> dict:
    """Retorna o GeoJSON de iluminação como dict Python.

    Faz download automático se o cache não existir.
    """
    if not cache_path.exists():
        download_iluminacao(cache_path)
    with cache_path.open(encoding="utf-8") as f:
        return json.load(f)
