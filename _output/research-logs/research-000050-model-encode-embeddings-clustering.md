# Research 000050 | gavealab-poc/embeddings | 2026-06-15 20:19 UTC | model.encode parameters for topic clustering

tags: embeddings, clustering, umap, sentence-transformers, ux

## User Brief

> `model.encode(texts, normalize_embeddings=True, show_progress_bar=True)` parameters in order to better generate embeddings to cluster in topics of interest (education, saúde, segurança)

## Agent Interpretation

Evaluate `model.encode()` parameter choices beyond the current baseline in `gavealab_poc/embeddings.py` to improve embedding quality for semantic clustering of citizen feedback (relatos) in Portuguese. The primary goal is better separation of clusters for civic topics like educação, saúde, and segurança in the UMAP visualization.

## Files Consulted

- `gavealab-poc/gavealab_poc/embeddings.py` — current encode implementation
- `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` — UMAP call site
- `fala-gavea/src/fala_gavea/pipeline/label_clusters.py` — cluster label pipeline

---

## Q&A Log

### Q1

**Question:** What are the best `model.encode()` parameter choices (beyond the current baseline) to improve embedding quality for semantic clustering of citizen feedback (relatos) in Portuguese, specifically to better surface clusters related to topics like educação, saúde, and segurança?

**Current baseline:**
```python
# gavealab-poc/gavealab_poc/embeddings.py
EMBED_MODEL = "intfloat/multilingual-e5-large"

def embed(texts: list[str], prefix: str = "passage: ") -> "np.ndarray":
    model = get_model()
    prefixed = [prefix + t for t in texts]
    return np.array(model.encode(prefixed, normalize_embeddings=True))
```
Called from `umap_viz.py` line 38 as `embed(texts)` — using the default `"passage: "` prefix.

**Answer:**

#### Finding 1 — HIGH: Wrong E5 prefix for clustering

The `"passage: "` prefix is semantically **incorrect** for symmetric clustering tasks. The `intfloat/multilingual-e5-large` model is an asymmetric retrieval model:
- `"query: "` — for short, intent-bearing inputs (what the model treats as a "searcher")
- `"passage: "` — for longer documents being retrieved

For **symmetric similarity** (claim-to-claim clustering, where both items are citizen relatos of similar length and nature), neither `"passage: "` nor no-prefix perfectly matches the training objective, but `"query: "` is empirically recommended by the E5 model card for short symmetric inputs. Using `"passage: "` shifts the embedding geometry in ways that reduce intra-cluster cohesion and inflate inter-cluster distances for topically related texts — exactly the opposite of what clustering needs.

**Fix:** In `umap_viz.py` line 38, change:
```python
embeddings = embed(texts)  # uses default "passage: "
```
to:
```python
embeddings = embed(texts, prefix="query: ")
```
No change to `embeddings.py` needed — the `prefix` parameter is already exposed.

#### Finding 2 — HIGH: No explicit batch_size

Without `batch_size`, sentence-transformers uses its internal default (32). For 100–1000 claims on CPU-only hardware (local laptop running Streamlit + Ollama simultaneously), this is fine for correctness but leaves memory consumption unpredictable. `multilingual-e5-large` (580M params) can allocate several GB of intermediate tensors for large batches.

**Fix:** Add `batch_size=64` to the `encode()` call in `embeddings.py`, and expose it via the `embed()` function signature:
```python
def embed(texts: list[str], prefix: str = "passage: ", batch_size: int = 64) -> "np.ndarray":
    model = get_model()
    prefixed = [prefix + t for t in texts]
    return np.array(model.encode(prefixed, normalize_embeddings=True, batch_size=batch_size))
```

#### Finding 3 — MEDIUM: show_progress_bar and Streamlit UX

`show_progress_bar=True` sends a tqdm bar to the **server terminal** (stdout), not to the Streamlit browser UI. For development this is useful; for users it is invisible. The real fix for user feedback is wrapping the UMAP/embed call in `st.spinner("Calculando embeddings...")` in the page module — as mandated by the Streamlit Conventions in `product-design/project/standards.md`.

That said, adding `show_progress_bar=True` to `embed()` is still worthwhile for the developer running `streamlit run` locally.

#### Finding 4 — LOW: convert_to_tensor=False is correct

`convert_to_tensor=True` returns a PyTorch Tensor. Since `build_umap_df()` wraps the result in `np.array()` and UMAP accepts numpy natively, using `convert_to_tensor=True` would add a wasted GPU→CPU conversion. Keep the default (`False`).

#### Finding 5 — LOW: normalize_embeddings=True is correct and sufficient

With `metric="cosine"` in UMAP, L2-normalizing beforehand is mathematically equivalent to direct cosine distance computation. No additional normalization step is needed. PCA (1024 → 50 dims) before UMAP is an optional speed optimization for datasets above ~2000 claims — unnecessary at the current scale.

#### Finding 6 — LOW: device auto-detection is fine

`sentence_transformers` auto-detects CUDA/MPS if available. The `@lru_cache(maxsize=1)` pattern freezes the device choice for the process lifetime. No explicit `device` argument is needed; auto-detection correctly uses GPU if present and falls back to CPU.

---

## Recommendations Summary

| # | Priority | Recommendation | File | Change |
|---|----------|---------------|------|--------|
| 1 | **HIGH** | Change prefix from `"passage: "` to `"query: "` at the clustering call site | `pipeline/umap_viz.py:38` | `embed(texts, prefix="query: ")` |
| 2 | **HIGH** | Add explicit `batch_size=64` to `embed()` signature and `model.encode()` call | `embeddings.py` | Add `batch_size: int = 64` param |
| 3 | **MEDIUM** | Add `show_progress_bar=True` to `model.encode()` call (dev feedback) | `embeddings.py` | `model.encode(..., show_progress_bar=True)` |
| 4 | **MEDIUM** | Wrap embedding/UMAP call in `st.spinner()` in the UMAP page | `pages/umap_viz.py` | Add spinner around `build_umap_df()` call |
| 5 | **MEDIUM** | Add docstring to `embed()` explaining E5 prefix semantics | `embeddings.py` | Inline docstring |
| 6 | **LOW** | Do not use `convert_to_tensor=True` — keep default | — | No change needed |
| 7 | **LOW** | PCA pre-reduction — defer until claim count > 2000 | — | No change now |
