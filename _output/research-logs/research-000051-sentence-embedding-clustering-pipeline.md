# Research 000051 | FEATURE-X | 2026-06-15 20:43 | Sentence embedding clustering pipeline — high-dim vs two-pass UMAP
tags: clustering, umap, hdbscan, embeddings, architecture

## User Brief

> best pipeline for clustering sentences. im seing that we reduce using umap before HDBSCAN. can we cluster on hight dimensiion first them reduce to visualize?

Code under review: `fala-gavea/src/fala_gavea/pipeline/cluster.py` — `build_cluster_df()`.

## Agent Interpretation

The user noticed the current pipeline reduces with UMAP before (or alongside) HDBSCAN and wants to know whether the pipeline should instead cluster in the full high-dimensional embedding space (768d) and only reduce to 2D for visualization. Research extended to a 4-way comparison including the BERTopic two-pass UMAP pattern (shared intermediate dimension).

## Files

- `fala-gavea/src/fala_gavea/pipeline/cluster.py`
- `fala-gavea/src/fala_gavea/pipeline/embeddings.py`
- `fala-gavea/src/fala_gavea/pipeline/label_clusters.py`

---

## Q&A

### Q1: What is the best clustering pipeline for sentence embeddings when both quality clustering and visual alignment (scatter plot) are required?

**Short answer: the current code already clusters in high-dim (good), but the best approach is a two-pass UMAP with a shared intermediate dimension.**

#### Observation about the current code

The current `build_cluster_df` already does something important correctly: `clusterer.fit_predict(embeddings)` runs HDBSCAN on the original 768-dim embedding vectors, NOT on the 2D UMAP coordinates. So the user's question "can we cluster in high dimension first then reduce to visualize?" is already answered yes — the code already does this.

The real question is: is "cluster in full 768-dim + separate UMAP to 2D for viz" the best approach, or is there a better one?

#### Four approaches evaluated

| # | Name | Cluster space | Viz space | Semantic quality | Visual alignment |
|---|------|---------------|-----------|-----------------|-----------------|
| 1 | **Current** | 768-dim original | 2D UMAP (independent) | ++ | Poor |
| 2 | 2D clustering | 2D UMAP | 2D UMAP (same) | Poor | ++ |
| 3 | BERTopic independent | N-dim UMAP (min_dist=0) | 2D UMAP (independent) | +++ | Poor |
| 4 | **Shared intermediate** | N-dim UMAP (min_dist=0) | 2D UMAP (from N-dim) | +++ | ++ |

**Approach 4 (shared intermediate) is the recommended approach.**

#### Why visual alignment matters

US-GL-005 states the goal is "ver como as opiniões se agrupam semanticamente" via the scatter plot. In Approach 1 (current), HDBSCAN and UMAP are run independently on the same 768-dim embeddings. The 2D UMAP positions and the cluster labels are therefore derived from independent projections — cluster color boundaries in the scatter plot will not match spatial blobs visible to the user. A tight semantic cluster in 768D may appear spread or fragmented in 2D because `min_dist=0.1` is tuned for visual legibility, not cluster separation.

This is not a bug that can be fixed by tuning parameters. It is structural: two independent transforms of the same input space will produce different local neighborhoods.

#### Why not cluster in 2D (Approach 2)?

UMAP with `min_dist=0.1` aggressively distorts global distances to produce a legible scatter plot. HDBSCAN on these 2D coordinates finds density peaks in visual space, not semantic space. At N=100–500 (typical GaveaLab dataset), 2D UMAP frequently merges semantically distinct topics and splits coherent ones. Visual alignment is gained at the cost of semantic correctness. For a tool analyzing citizen relatos, semantic correctness is non-negotiable.

#### Why not just cluster in 768-dim (Approach 1/current)?

The curse of dimensionality: in very high dimensions, cosine distances between all pairs of vectors tend to concentrate — the contrast between nearest and farthest neighbors shrinks. This hurts HDBSCAN's density estimation. An intermediate dimensionality reduction to 5–50 dimensions (with `min_dist=0`, preserving local structure tightly) gives HDBSCAN a better-separated geometry to work with, while still retaining far more semantic information than a 2D reduction.

#### The recommended pipeline (Approach 4)

```python
N_INTERMEDIATE = 10  # 5–15 is well-motivated for short text at N=100–2000

# Step 1: reduce to intermediate dim — optimized for clustering (tight local structure)
reducer_cluster = umap.UMAP(
    n_components=N_INTERMEDIATE,
    n_neighbors=min(n_neighbors, len(posts) - 1),
    min_dist=0.0,          # tightly packed — maximizes cluster density
    metric="cosine",
    random_state=42,
)
embedding_intermediate = reducer_cluster.fit_transform(embeddings)  # (N, 10)

# Step 2: cluster in intermediate space
clusterer = HDBSCAN(min_cluster_size=min(min_cluster_size, max(2, len(posts) // 10)))
labels = clusterer.fit_predict(embedding_intermediate)

# Step 3: reduce intermediate to 2D for visualization
reducer_viz = umap.UMAP(
    n_components=2,
    n_neighbors=min(n_neighbors, len(posts) - 1),
    min_dist=0.1,          # spread for visual legibility
    metric="euclidean",    # intermediate space is Euclidean
    random_state=42,
)
coords = reducer_viz.fit_transform(embedding_intermediate)  # (N, 2)
```

Because both HDBSCAN and the 2D UMAP operate on `embedding_intermediate`, the 2D positions are derived from the same space that defined the clusters. Spatial blobs in the scatter plot will visually align with cluster color assignments.

#### Performance

At N=100–2000 with 768-dim inputs:
- Each UMAP call: 0.5–8s on CPU
- Running two UMAP passes: 1–16s total
- LLM labeling loop (per cluster): 3–30s per call

The extra UMAP pass is negligible vs. the LLM labeling step. No performance concern at these dataset sizes.

#### Side effect: label_clusters.py centroid selection

`_pick_representatives` in `label_clusters.py` selects representative posts by proximity to the 2D centroid of the cluster. Under Approach 4, 2D positions will align with clusters, so this continues to work correctly. Under Approach 1 (current), the 2D centroid of a cluster may not correspond to the actual cluster center — labels are generated from posts that happen to be near the visual centroid, not the semantic centroid.

---

## Recommendations Summary

1. **[HIGH] Adopt the two-pass UMAP shared intermediate pipeline (Approach 4)** — Replace the current pipeline in `cluster.py` with: 768-dim → N-dim UMAP (min_dist=0, for clustering) → HDBSCAN → N-dim → 2D UMAP (min_dist=0.1, for viz). Default `N_INTERMEDIATE=10`. This fixes the cluster-to-visual alignment gap and improves HDBSCAN clustering quality by avoiding the curse of dimensionality in 768-dim space.

2. **[HIGH] Fix `_pick_representatives` in `label_clusters.py`** — Under Approach 4, the 2D centroid will align with the semantic cluster, so the existing logic continues to work. But document explicitly that representative selection is proximity to the 2D visual centroid, not the cluster centroid in the intermediate space.

3. **[MEDIUM] Add `n_components_intermediate` as a named constant** — Add `N_COMPONENTS_INTERMEDIATE = 10` to the constants (in `cluster.py` or a shared constants file). Do not hardcode inline.

4. **[MEDIUM] Add a regression test for cluster-visual alignment** — With `random_state=42`, the pipeline is deterministic. A pytest test using synthetic 3-cluster 768-dim Gaussians can assert that mean intra-cluster 2D distance < mean inter-cluster 2D distance.

5. **[LOW] Do not cluster on 2D UMAP coords (Approach 2)** — Semantically incorrect for short text and HDBSCAN. Discard this approach.
