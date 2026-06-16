"""Download e cache local do dataset de iluminação pública (ArcGIS Feature Service)."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx

# ArcGIS REST Feature Service — Pontos de Iluminação Pública (Postes), Niterói/RJ
# Item: https://www.arcgis.com/home/item.html?id=5322126ff10e46249be878ddfd057cc5
_FEATURE_SERVICE_URL = (
    "https://services8.arcgis.com/TpaOLI1HCh5AcRQB/arcgis/rest/services"
    "/Grouplayer_SECONSER_ILUMPUB_AGOL/FeatureServer/10/query"
)
_PAGE_SIZE = 2000  # service maxRecordCount
_DEFAULT_CACHE = Path(__file__).parents[4] / "data" / "iluminacao.geojson"

log = logging.getLogger(__name__)


def download_iluminacao(cache_path: Path = _DEFAULT_CACHE) -> None:
    """Baixa todos os pontos de iluminação via ArcGIS REST e salva em cache GeoJSON."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    features: list[dict] = []
    offset = 0
    with httpx.Client(follow_redirects=True, timeout=60) as client:
        while True:
            params = {
                "where": "1=1",
                "outFields": "*",
                "f": "geojson",
                "outSR": "4326",
                "resultOffset": offset,
                "resultRecordCount": _PAGE_SIZE,
            }
            log.info("Baixando iluminação: offset=%d ...", offset)
            r = client.get(_FEATURE_SERVICE_URL, params=params)
            r.raise_for_status()
            page = r.json()
            batch = page.get("features", [])
            features.extend(batch)
            if len(batch) < _PAGE_SIZE:
                break
            offset += _PAGE_SIZE
    geojson = {"type": "FeatureCollection", "features": features}
    cache_path.write_text(json.dumps(geojson), encoding="utf-8")
    log.info("Dataset salvo em %s (%d features)", cache_path, len(features))


def load_iluminacao_geojson(cache_path: Path = _DEFAULT_CACHE) -> dict:
    """Retorna o GeoJSON de iluminação como dict Python.

    Faz download automático se o cache não existir.
    """
    if not cache_path.exists():
        download_iluminacao(cache_path)
    with cache_path.open(encoding="utf-8") as f:
        return json.load(f)
