# Plan 000039 | FEATURE-F | 2026-06-11 18:07 UTC | fala-gavea: UMAP cluster visualization of posts + AI labels | Review: standard
# DONE | 2026-06-11 19:30 UTC |
plan_format_version: 1

## User Brief

fala-gavea: UMAP bottom-up cluster visualization of citizen posts with AI-generated labels. Fluxo: posts do banco → embeddings via nomic-embed-text-v1 → ChromaDB como vector store (coleção fala-gavea-posts) → UMAP 2D → HDBSCAN clustering → Ollama gera label por cluster → salva ai_labels nos posts → Plotly scatter interativo no Streamlit. Reusa a mesma stack do gavealab-poc (sentence-transformers, umap-learn, plotly, ollama). ChromaDB armazena embeddings por post_id. Nova página no app Streamlit: "Explorar Clusters".

## Agent Interpretation

Pipeline bottom-up de clusterização semântica com 5 etapas encadeadas:

```
GET /citizen_posts/           → lista todos os posts do banco
    ↓
pipeline/embeddings.py        → nomic-embed-text-v1 via sentence-transformers
                              → upsert em ChromaDB (coleção "fala-gavea-posts")
    ↓
pipeline/cluster.py           → UMAP 2D (cosine metric)
                              → sklearn HDBSCAN → cluster_id por post
    ↓
pipeline/label_clusters.py    → por cluster: top-5 posts → Ollama (qwen3:8b)
                              → gera label curto em pt-BR (2-4 palavras)
    ↓
POST /citizen_posts/{id}/ai_labels  → salva labels no banco via API
    ↓
Streamlit "Explorar Clusters" → Plotly scatter (x, y, cor=cluster_label, hover=texto+território)
```

**Diferença chave vs. gavealab-poc**: o gavealab-poc faz UMAP sobre *claims* (pós-extração LLM). Aqui fazemos UMAP diretamente sobre os *posts brutos* — os clusters emergem dos dados, os labels vêm depois. O LLM só entra para nomear clusters já formados, não para pré-definir temas.

**Onde o pipeline roda**: nos módulos `fala_gavea/pipeline/` importados diretamente pelo Streamlit (não via API REST). Apenas o `save ai_labels` passa pela API para respeitar o princípio de que toda persistência vai pelo FastAPI.

**ChromaDB**: `PersistentClient` em `fala-gavea/vectorstore/` (gitignored). Reutiliza a mesma abordagem do kb-qa.

**Modelo de embedding**: `nomic-ai/nomic-embed-text-v1` — mesmo do kb-qa, multilingual, MIT. O gavealab-poc usa `intfloat/multilingual-e5-large`; não misturamos os dois.

## Context

### What already exists

| Componente | Localização | Notas |
|-----------|------------|-------|
| `CitizenPost.ai_labels: list[str]` | `domain/entities/citizen_post.py` | Campo existe, nunca populado automaticamente |
| `CitizenPostModel.ai_labels` | `infrastructure/database/models.py` | JSON column |
| `GET /citizen_posts/` com paginação | `presentation/api/routers/citizen_posts.py` | `limit`/`offset` disponíveis |
| `app.py` com 4 páginas | `fala-gavea/app.py` | PAGES dict, helpers `api_get`/`api_post` |
| `umap_viz.py` (gavealab-poc) | `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` | Referência de implementação |
| `embeddings.py` (gavealab-poc) | `gavealab-poc/gavealab_poc/embeddings.py` | Usa `intfloat/multilingual-e5-large` |

### What must be added

1. **pyproject.toml** — dependências: `chromadb>=0.5`, `sentence-transformers>=3.0`, `umap-learn>=0.5`, `scikit-learn>=1.5`, `plotly>=5.0`, `einops>=0.8`
2. **`pipeline/embeddings.py`** — embed posts → ChromaDB (nomic-embed-text-v1)
3. **`pipeline/cluster.py`** — UMAP + HDBSCAN → DataFrame com x, y, cluster_id por post
4. **`pipeline/label_clusters.py`** — Ollama gera label por cluster a partir de posts representativos
5. **`application/use_cases/set_ai_labels.py`** + repository method — persiste ai_labels
6. **`presentation/api/routers/citizen_posts.py`** — novo endpoint `POST /{id}/ai_labels`
7. **`app.py`** — nova página `page_clusters()` + entrada no PAGES dict

## Files

| File | Change |
|------|--------|
| `fala-gavea/pyproject.toml` | Adicionar 6 dependências |
| `fala-gavea/src/fala_gavea/pipeline/__init__.py` | Criar (vazio) |
| `fala-gavea/src/fala_gavea/pipeline/embeddings.py` | Criar |
| `fala-gavea/src/fala_gavea/pipeline/cluster.py` | Criar |
| `fala-gavea/src/fala_gavea/pipeline/label_clusters.py` | Criar |
| `fala-gavea/src/fala_gavea/domain/repositories/citizen_post_repository.py` | Adicionar `set_ai_labels` abstract method |
| `fala-gavea/src/fala_gavea/infrastructure/repositories/sqlalchemy_citizen_post_repository.py` | Implementar `set_ai_labels` |
| `fala-gavea/src/fala_gavea/application/use_cases/set_ai_labels.py` | Criar |
| `fala-gavea/src/fala_gavea/presentation/schemas/citizen_post_schemas.py` | Adicionar `AiLabelsRequest` |
| `fala-gavea/src/fala_gavea/presentation/api/routers/citizen_posts.py` | Adicionar endpoint `POST /{id}/ai_labels` |
| `fala-gavea/app.py` | Adicionar `page_clusters()` e entrada no PAGES |
| `fala-gavea/.gitignore` | Adicionar `vectorstore/` se ausente |

---

## Steps

### Step 1 — Adicionar dependências ao pyproject.toml

**File:** `fala-gavea/pyproject.toml`

Adicionar ao array `dependencies`:
```toml
"chromadb>=0.5",
"sentence-transformers>=3.0",
"umap-learn>=0.5",
"scikit-learn>=1.5",
"plotly>=5.0",
"einops>=0.8",
```

`einops` é requerido pelo modelo `nomic-embed-text-v1`. `scikit-learn` fornece `sklearn.cluster.HDBSCAN` (disponível desde 1.3, sem dependência C separada). `plotly` para o scatter interativo.

Após editar: `uv sync` para instalar as novas dependências.

- **Files**: `fala-gavea/pyproject.toml`
- **Interface**: dependências disponíveis em `fala-gavea/.venv`

---

### Step 2 — Criar `pipeline/embeddings.py`

**File:** `fala-gavea/src/fala_gavea/pipeline/embeddings.py`

```python
"""Embedding pipeline: encode citizen posts → store/retrieve from ChromaDB."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "nomic-ai/nomic-embed-text-v1"
COLLECTION_NAME = "fala-gavea-posts"
DEFAULT_VECTORSTORE = Path(__file__).parent.parent.parent.parent / "vectorstore"


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
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

    texts = [f"search_document: {p['text']}" for p in posts]
    ids = [p["id"] for p in posts]
    metadatas = [
        {"territory_name": p.get("territory_name", ""), "author_id": p.get("author_id", "")}
        for p in posts
    ]
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    collection.upsert(ids=ids, embeddings=vectors.tolist(), documents=texts, metadatas=metadatas)


def get_embeddings(post_ids: list[str], vectorstore_dir: Path = DEFAULT_VECTORSTORE) -> np.ndarray:
    """Retrieve stored vectors from ChromaDB by post ID."""
    collection = _get_collection(vectorstore_dir)
    result = collection.get(ids=post_ids, include=["embeddings"])
    return np.array(result["embeddings"])
```

**Nota**: `nomic-embed-text-v1` requer `trust_remote_code=True`. O prefixo `search_document:` é necessário para o modelo nomic (instruction-tuned). Ao consultar, usar `search_query:` como prefixo. O `DEFAULT_VECTORSTORE` aponta para `fala-gavea/vectorstore/` relativo ao pacote instalado.

- **Files**: `fala-gavea/src/fala_gavea/pipeline/__init__.py` (criar vazio), `fala-gavea/src/fala_gavea/pipeline/embeddings.py`
- **Interface**: `embed_and_store(posts, vectorstore_dir?)`, `get_embeddings(post_ids, vectorstore_dir?)`

---

### Step 3 — Criar `pipeline/cluster.py`

**File:** `fala-gavea/src/fala_gavea/pipeline/cluster.py`

```python
"""UMAP projection + HDBSCAN clustering over post embeddings."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import umap
from sklearn.cluster import HDBSCAN

from .embeddings import DEFAULT_VECTORSTORE, embed_and_store, get_embeddings


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

    embed_and_store(posts, vectorstore_dir)
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
```

**Nota**: `min_cluster_size` é adaptativo — `max(5, N//10)` para datasets pequenos. HDBSCAN do scikit-learn (>= 1.3) não requer compilação C separada.

- **Files**: `fala-gavea/src/fala_gavea/pipeline/cluster.py`
- **Interface**: `build_cluster_df(posts, vectorstore_dir?, n_neighbors?, min_dist?, min_cluster_size?) -> pd.DataFrame`

---

### Step 4 — Criar `pipeline/label_clusters.py`

**File:** `fala-gavea/src/fala_gavea/pipeline/label_clusters.py`

```python
"""Generate cluster labels via Ollama LLM from representative posts."""
from __future__ import annotations

import json
import os

import httpx
import numpy as np
import pandas as pd

OLLAMA_URL = os.environ.get("FALA_GAVEA_OLLAMA_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("FALA_GAVEA_OLLAMA_MODEL", "qwen3:8b")

_LABEL_PROMPT = """\
Você recebeu os seguintes relatos de cidadãos do mesmo grupo temático.
Gere um label curto (2 a 4 palavras) em português que capture o tema principal desses relatos.
Responda APENAS com o label, sem explicação, sem pontuação extra.

Relatos:
{posts}

Label:"""


def _pick_representatives(group_df: pd.DataFrame, n: int = 5) -> list[str]:
    """Return n texts closest to the cluster centroid in UMAP space."""
    coords = group_df[["x", "y"]].values
    centroid = coords.mean(axis=0)
    dists = np.linalg.norm(coords - centroid, axis=1)
    idx = np.argsort(dists)[:n]
    return group_df.iloc[idx]["text"].tolist()


def label_clusters(df: pd.DataFrame) -> dict[int, str]:
    """Call Ollama once per cluster to generate a short label.

    Returns {cluster_id: label_str}. Noise cluster (-1) gets "Não classificado".
    """
    labels: dict[int, str] = {-1: "Não classificado"}
    cluster_ids = [c for c in df["cluster_id"].unique() if c != -1]

    for cid in sorted(cluster_ids):
        group = df[df["cluster_id"] == cid]
        samples = _pick_representatives(group)
        prompt = _LABEL_PROMPT.format(posts="\n".join(f"- {t}" for t in samples))
        try:
            resp = httpx.post(
                f"{OLLAMA_URL}/chat/completions",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=30,
            )
            resp.raise_for_status()
            label = resp.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            label = f"Cluster {cid}"
        labels[cid] = label

    return labels
```

- **Files**: `fala-gavea/src/fala_gavea/pipeline/label_clusters.py`
- **Interface**: `label_clusters(df: pd.DataFrame) -> dict[int, str]`
- **Config**: `FALA_GAVEA_OLLAMA_URL` (default `http://localhost:11434/v1`), `FALA_GAVEA_OLLAMA_MODEL` (default `qwen3:8b`)

---

### Step 5 — Adicionar `set_ai_labels` ao domínio e infraestrutura

**`domain/repositories/citizen_post_repository.py`** — adicionar método abstrato:

```python
@abstractmethod
def set_ai_labels(self, post_id: str, labels: list[str]) -> CitizenPost:
    """Replace the ai_labels list on a post."""
```

**`infrastructure/repositories/sqlalchemy_citizen_post_repository.py`** — implementar:

```python
def set_ai_labels(self, post_id: str, labels: list[str]) -> CitizenPost:
    with self._session() as session:
        model = session.get(CitizenPostModel, post_id)
        if model is None:
            raise ValueError(f"Post {post_id} not found")
        model.ai_labels = labels
        session.commit()
        session.refresh(model)
        return self._to_entity(model)
```

**`application/use_cases/set_ai_labels.py`** — criar:

```python
from __future__ import annotations
from dataclasses import dataclass
from ..domain.repositories.citizen_post_repository import CitizenPostRepository
from ..domain.entities.citizen_post import CitizenPost


@dataclass
class SetAiLabelsInput:
    post_id: str
    labels: list[str]


class SetAiLabels:
    def __init__(self, repo: CitizenPostRepository) -> None:
        self._repo = repo

    def execute(self, inp: SetAiLabelsInput) -> CitizenPost:
        return self._repo.set_ai_labels(inp.post_id, inp.labels)
```

- **Files**: `domain/repositories/citizen_post_repository.py`, `infrastructure/repositories/sqlalchemy_citizen_post_repository.py`, `application/use_cases/set_ai_labels.py`

---

### Step 6 — Adicionar endpoint `POST /{id}/ai_labels`

**`presentation/schemas/citizen_post_schemas.py`** — adicionar:

```python
class AiLabelsRequest(BaseModel):
    labels: list[str]
```

**`presentation/api/routers/citizen_posts.py`** — adicionar endpoint após `add_label_feedback`:

```python
@router.post("/{id}/ai_labels", response_model=CitizenPostResponse)
def set_ai_labels(
    id: str,
    body: AiLabelsRequest,
    repo: CitizenPostRepository = Depends(get_repository),
) -> CitizenPostResponse:
    use_case = SetAiLabels(repo)
    post = use_case.execute(SetAiLabelsInput(post_id=id, labels=body.labels))
    return CitizenPostResponse.model_validate(post.__dict__)
```

- **Files**: `presentation/schemas/citizen_post_schemas.py`, `presentation/api/routers/citizen_posts.py`
- **Interface**: `POST /citizen_posts/{id}/ai_labels` body `{"labels": ["label1", "label2"]}`

---

### Step 7 — Adicionar `page_clusters()` ao app.py

**File:** `fala-gavea/app.py`

Adicionar imports no topo:

```python
import plotly.express as px
from fala_gavea.pipeline.cluster import build_cluster_df
from fala_gavea.pipeline.label_clusters import label_clusters
```

Adicionar função antes do bloco `PAGES`:

```python
def page_clusters() -> None:
    st.header("🗺️ Explorar Clusters")
    st.caption("Clusterização semântica dos posts via UMAP + HDBSCAN. Labels gerados por IA.")

    if "cluster_df" not in st.session_state:
        st.session_state.cluster_df = None

    col1, col2 = st.columns([1, 4])
    with col1:
        run_btn = st.button("🔄 Gerar Clusters", use_container_width=True)
        save_btn = st.button(
            "💾 Salvar Labels",
            disabled=st.session_state.cluster_df is None,
            use_container_width=True,
        )

    if run_btn:
        with st.spinner("Buscando posts..."):
            posts = api_get("/citizen_posts/", limit=500, offset=0)
        if not posts:
            st.warning("Nenhum post encontrado.")
            return

        with st.spinner("Calculando embeddings e clusters (pode levar alguns minutos)..."):
            df = build_cluster_df(posts)

        with st.spinner("Gerando labels com IA..."):
            cluster_labels = label_clusters(df)
            df["cluster_label"] = df["cluster_id"].map(cluster_labels)

        st.session_state.cluster_df = df
        st.success(f"{len(posts)} posts clusterizados em {df['cluster_id'].nunique() - (1 if -1 in df['cluster_id'].values else 0)} clusters.")

    df = st.session_state.cluster_df
    if df is not None:
        fig = px.scatter(
            df,
            x="x",
            y="y",
            color="cluster_label",
            hover_data={"text": True, "territory_name": True, "x": False, "y": False},
            title="Clusters de Posts — Espaço Semântico (UMAP)",
            labels={"cluster_label": "Cluster", "x": "UMAP-1", "y": "UMAP-2"},
        )
        fig.update_traces(marker=dict(size=6, opacity=0.7))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Resumo dos clusters")
        summary = (
            df.groupby("cluster_label")
            .agg(posts=("post_id", "count"), exemplo=("text", "first"))
            .reset_index()
            .rename(columns={"cluster_label": "Cluster", "posts": "Posts", "exemplo": "Exemplo"})
        )
        st.dataframe(summary, use_container_width=True)

        if save_btn:
            with st.spinner("Salvando labels nos posts..."):
                errors = 0
                for _, row in df.iterrows():
                    if row["cluster_id"] == -1:
                        continue
                    try:
                        api_post(f"/citizen_posts/{row['post_id']}/ai_labels",
                                 {"labels": [row["cluster_label"]]})
                    except Exception:
                        errors += 1
            if errors:
                st.warning(f"Labels salvos com {errors} erros.")
            else:
                st.success("Labels salvos com sucesso!")
```

Adicionar ao dict `PAGES`:

```python
"🗺️ Explorar Clusters": page_clusters,
```

- **Files**: `fala-gavea/app.py`
- **UX**: botão "Gerar Clusters" roda o pipeline; scatter Plotly com hover; tabela de resumo por cluster; botão "Salvar Labels" persiste via API

---

### Step 8 — Atualizar .gitignore

**File:** `fala-gavea/.gitignore` (criar se ausente)

Verificar se `vectorstore/` está na lista. Adicionar se ausente:

```
vectorstore/
```

- **Files**: `fala-gavea/.gitignore`

---

## Test Plan

- [ ] `uv sync` completa sem erros na pasta `fala-gavea/`
- [ ] Iniciar backend: `uvicorn fala_gavea.presentation.api.main:app --reload`
- [ ] Iniciar Streamlit: `streamlit run fala-gavea/app.py`
- [ ] Página "Explorar Clusters" aparece na sidebar
- [ ] Clicar "Gerar Clusters" com banco seedado: progresso visível, scatter aparece
- [ ] Hover sobre pontos mostra texto e território
- [ ] Tabela de resumo lista clusters com contagem e exemplo
- [ ] "Salvar Labels" posta ai_labels via API; "Validar Labels" mostra os labels salvos
- [ ] `GET /citizen_posts/` retorna posts com `ai_labels` preenchidos após salvar
- [ ] Reclusterizar: novo clique em "Gerar Clusters" sobrescreve resultado anterior em session_state
- [ ] Posts com cluster_id = -1 (noise) não são enviados para a API de labels

## Notes

- O primeiro run baixa o modelo `nomic-ai/nomic-embed-text-v1` (~274 MB). O `st.spinner` avisa que pode demorar.
- O ChromaDB em `vectorstore/` é idempotente: reclusterizar não duplica embeddings (upsert por post_id).
- `FALA_GAVEA_OLLAMA_MODEL` e `FALA_GAVEA_OLLAMA_URL` controlam qual modelo gera os labels.
- `n_neighbors=15` é o default do UMAP; com <50 posts pode precisar ser reduzido. O código adapta automaticamente via `min(n_neighbors, len(posts) - 1)`.
- Para datasets grandes (>1000 posts), considerar amostrar aleatoriamente antes de rodar UMAP+HDBSCAN.
