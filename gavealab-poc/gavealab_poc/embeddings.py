from __future__ import annotations
from functools import lru_cache
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "intfloat/multilingual-e5-large"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL)


def embed(texts: list[str], prefix: str = "passage: ") -> "np.ndarray":
    import numpy as np
    model = get_model()
    prefixed = [prefix + t for t in texts]
    return np.array(model.encode(prefixed, normalize_embeddings=True))
