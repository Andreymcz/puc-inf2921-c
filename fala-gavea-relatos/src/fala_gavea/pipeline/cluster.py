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
    min_samples: int | None = None,
) -> pd.DataFrame:
    """Embed posts, project to 2D via UMAP, cluster with HDBSCAN.

    Returns DataFrame with columns:
        post_id, text, territory_name, author_id, x, y, cluster_id,
        cluster_label, membership_strength
    cluster_id = -1 means noise (unclustered).
    cluster_label is empty string — filled by label_clusters().
    membership_strength ∈ [0, 1]: how strongly the point belongs to its cluster
        (0 for noise points). Derived from HDBSCAN λ_p values per the
        stability-based cluster extraction described by Campello et al.

    Args:
        min_samples: Controls the k for mutual reachability distance (core
            distance). Higher values make the density estimate smoother and
            the algorithm more conservative about what counts as a cluster core,
            reducing noise sensitivity. Defaults to min_cluster_size when None.
    """
    if not posts:
        return pd.DataFrame(
            columns=[
                "post_id", "text", "territory_name", "author_id",
                "x", "y", "cluster_id", "cluster_label", "membership_strength",
            ]
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

    effective_min_cluster_size = min(min_cluster_size, max(2, len(posts) // 10))
    clusterer = HDBSCAN(
        min_cluster_size=effective_min_cluster_size,
        # min_samples is the k for core/mutual-reachability distance; controls
        # how conservative the noise floor is. Defaults to min_cluster_size.
        min_samples=min_samples,
        metric="cosine",
        # EOM (excess of mass) implements the stability-based flat cluster
        # extraction: select clusters that maximise total λ area in the
        # condensed tree, subject to the descendant constraint.
        cluster_selection_method="eom",
        alpha=1.0,
    )
    clusterer.fit(embeddings)
    labels = clusterer.labels_
    # probabilities_ gives the λ_p-derived membership strength ∈ [0,1] per
    # point; noise points (-1) have strength 0.
    strengths = clusterer.probabilities_

    df = pd.DataFrame({
        "post_id": ids,
        "text": [p["text"] for p in posts],
        "territory_name": [p.get("territory_name", "") for p in posts],
        "author_id": [p.get("author_id", "") for p in posts],
        "x": coords[:, 0],
        "y": coords[:, 1],
        "cluster_id": labels.tolist(),
        "cluster_label": "",
        "membership_strength": strengths.tolist(),
    })
    return df
