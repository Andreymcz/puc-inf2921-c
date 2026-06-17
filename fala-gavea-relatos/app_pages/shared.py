from __future__ import annotations

import hashlib
import os

import httpx

API_URL: str = os.environ.get("FALA_GAVEA_API_URL", "http://localhost:8000")
POSTS_PER_PAGE: int = 20

_CITIZEN_NAMES: list[str] = [
    "Ana", "Carlos", "Fernanda", "João", "Mariana",
    "Pedro", "Luciana", "Rafael", "Beatriz", "Rodrigo",
    "Camila", "Diego", "Patricia", "André", "Juliana",
    "Marcos", "Vanessa", "Felipe", "Sandra", "Gustavo",
    "Renata", "Bruno", "Tatiana", "Eduardo", "Cristina",
    "Thiago", "Adriana", "Henrique", "Priscila", "Leonardo",
]


def citizen_name(user_id: str) -> str:
    idx = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % len(_CITIZEN_NAMES)
    return _CITIZEN_NAMES[idx]


def api_get(path: str, **params: object) -> list | dict:
    r = httpx.get(f"{API_URL}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, body: dict) -> dict:
    r = httpx.post(f"{API_URL}{path}", json=body, timeout=100)
    r.raise_for_status()
    return r.json()
