"""UMAP projection + HDBSCAN clustering over post embeddings."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import umap
from sklearn.cluster import HDBSCAN

from .embeddings import DEFAULT_VECTORSTORE, get_embeddings


def build_cluster_df(
    posts: list[dict],
    vectorstore_dir: Path = DEFAULT_VECTORSTORE,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    min_cluster_size: int = 5,
) -> pd.DataFrame:
    """Embed posts, project to 2D via UMAP, cluster with HDBSCAN.

    Returns DataFrame with columns:
        post_id, text, territory_name, author_id, x, y, cluster_id, cluster_label
    cluster_id = -1 means noise (unclustered).
    cluster_label is empty string — filled by label_clusters().
    """
    if not posts:
        return pd.DataFrame(
            columns=["post_id", "text", "territory_name", "author_id", "x", "y",
                     "cluster_id", "cluster_label"]
        )

    ids = [p["id"] for p in posts]
    embeddings = get_embeddings(ids, vectorstore_dir)

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=min(n_neighbors, len(posts) - 1),
        min_dist=min_dist,
        metric="cosine",
        random_state=42,
    )
    coords = reducer.fit_transform(embeddings)  # (N, 2)

    clusterer = HDBSCAN(min_cluster_size=min(min_cluster_size, max(2, len(posts) // 10)))
    labels = clusterer.fit_predict(embeddings)

    df = pd.DataFrame({
        "post_id": ids,
        "text": [p["text"] for p in posts],
        "territory_name": [p.get("territory_name", "") for p in posts],
        "author_id": [p.get("author_id", "") for p in posts],
        "x": coords[:, 0],
        "y": coords[:, 1],
        "cluster_id": labels.tolist(),
        "cluster_label": "",
    })
    return df
