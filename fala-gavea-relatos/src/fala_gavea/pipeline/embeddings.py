"""Embedding pipeline: encode citizen posts → store/retrieve from ChromaDB."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import chromadb
import numpy as np

EMBED_MODEL = "nomic-ai/nomic-embed-text-v1"
COLLECTION_NAME = "fala-gavea-posts"
DEFAULT_VECTORSTORE = Path(__file__).parent.parent.parent.parent / "vectorstore"


@lru_cache(maxsize=1)
def _get_model():  # type: ignore[return]
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL, trust_remote_code=True)


@lru_cache(maxsize=1)
def _get_collection(vectorstore_dir: Path) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(vectorstore_dir))
    return client.get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_and_store(posts: list[dict], vectorstore_dir: Path = DEFAULT_VECTORSTORE) -> None:
    """Encode post texts and upsert into ChromaDB. Idempotent."""
    if not posts:
        return
    model = _get_model()
    collection = _get_collection(vectorstore_dir)

    texts = [f"clustering: {p['text']}" for p in posts]
    ids = [p["id"] for p in posts]
    metadatas = [
        {"territory_name": p.get("territory_name", ""), "author_id": p.get("author_id", "")}
        for p in posts
    ]
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True, batch_size=64)
    collection.upsert(ids=ids, embeddings=vectors.tolist(), documents=texts, metadatas=metadatas)


def get_embeddings(post_ids: list[str], vectorstore_dir: Path = DEFAULT_VECTORSTORE) -> np.ndarray:
    """Retrieve stored vectors from ChromaDB by post ID."""
    collection = _get_collection(vectorstore_dir)
    result = collection.get(ids=post_ids, include=["embeddings"])
    return np.array(result["embeddings"])
