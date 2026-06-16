from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import chromadb
from chromadb import Collection
from sentence_transformers import SentenceTransformer

_EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-ai/nomic-embed-text-v1")
_VECTORSTORE_DIR = Path(os.environ.get("VECTORSTORE_DIR", "./vectorstore"))
_COLLECTION_NAME = "fala-gavea-seguranca"

_model: SentenceTransformer | None = None
_client: chromadb.PersistentClient | None = None
_collection: Collection | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_EMBED_MODEL, trust_remote_code=True)
    return _model


def _get_collection() -> Collection:
    global _client, _collection
    if _collection is None:
        _VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(_VECTORSTORE_DIR))
        _collection = _client.get_or_create_collection(
            name=_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def embed_text(text: str) -> list[float]:
    return _get_model().encode(text, normalize_embeddings=True).tolist()


def upsert_document(
    doc_id: str,
    text: str,
    metadata: dict[str, Any],
) -> None:
    col = _get_collection()
    embedding = embed_text(text)
    col.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
    )


def search(
    query: str,
    n_results: int = 5,
    where: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    col = _get_collection()
    if col.count() == 0:
        return []
    embedding = embed_text(query)
    kwargs: dict[str, Any] = {"query_embeddings": [embedding], "n_results": min(n_results, col.count())}
    if where:
        kwargs["where"] = where
    results = col.query(**kwargs)
    hits = []
    for i, doc_id in enumerate(results["ids"][0]):
        hits.append({
            "id": doc_id,
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return hits


def delete_document(doc_id: str) -> None:
    try:
        _get_collection().delete(ids=[doc_id])
    except Exception:
        pass
