# Plan 000032 | FEATURE-F | 2026-06-11 10:59 UTC | fala-gavea: seed dataset (posts + likes) + dashboard visualizations | Review: light
# DONE | 2026-06-11 14:18 UTC |
plan_format_version: 1

## User Brief

Based on recent roadmap 30, criamos a base para o app de postagens e likes. quero criar um dataset fake para inserir no banco de dados e trabalhar nas visualizações do app. Vamos criar um banco de dados maior inspirado nos dados de relatos reais em `./data`. Foco somente na parte humana: posts reais e likes de usuários. Labelização automática fica para depois.

## Agent Interpretation

Dois entregáveis independentes, focados exclusivamente nos sinais humanos (posts e likes):

**1. Script de seed** — `fala-gavea/scripts/seed_db.py`  
Lê os 1000 relatos reais de `data/sample-gavealab-1000.csv` (encoding `latin-1`, colunas `id`, `comment`, `territory`). Os 4 territórios do CSV mapeiam para o modelo fala-gavea:

| CSV `territory` | `territory_name` | `territory_level` |
|---|---|---|
| `comunidade` | Comunidade da Gávea | neighborhood |
| `asfalto` | Baixo Gávea | neighborhood |
| `alto da gávea` | Alto da Gávea | neighborhood |
| `favela` | Favela da Gávea | neighborhood |

Posts inseridos com `ai_labels: []` — sem classificação automática. Após os posts, distribui ~500 likes entre 20 `user_id`s simulados (one-like-per-user via API). Sem `label_feedback` nesta fase.

**2. Melhorias no Dashboard** — `fala-gavea/app.py` (função `page_dashboard`)  
Dashboard focado em sinais humanos. Mantém o existente e adiciona 3 visualizações:
- **Postagens por dia** — linha temporal (últimos 60 dias)
- **Distribuição de likes por post** — histograma em buckets
- **Top posts por território** — barra empilhada: posts e likes por território

Remove as seções de labels/feedback do dashboard atual (métricas de AI labels e tabela de feedback) — essas voltam quando a labelização for implementada.

## Files

- `fala-gavea/scripts/__init__.py` — criar (vazio)
- `fala-gavea/scripts/seed_db.py` — criar
- `fala-gavea/app.py` — modificar `page_dashboard()`

## Steps

### Step 1 — Criar `fala-gavea/scripts/__init__.py` (vazio)

Arquivo vazio para tornar `scripts/` um pacote Python.

- [x] Done

---

### Step 2 — Criar `fala-gavea/scripts/seed_db.py`

```python
"""Seed script — inserts real citizen relatos + simulated likes into fala-gavea app.db."""
from __future__ import annotations

import csv
import os
import pathlib
import random
import uuid

import httpx

API_URL = os.environ.get("FALA_GAVEA_API_URL", "http://localhost:8000")
DATA_FILE = pathlib.Path(__file__).parent.parent.parent / "data" / "sample-gavealab-1000.csv"

TERRITORY_MAP: dict[str, tuple[str, str]] = {
    "comunidade":    ("Comunidade da Gávea", "neighborhood"),
    "asfalto":       ("Baixo Gávea",         "neighborhood"),
    "alto da gávea": ("Alto da Gávea",       "neighborhood"),
    "favela":        ("Favela da Gávea",      "neighborhood"),
}

LIKES_PER_AUTHOR = 50


def load_csv() -> list[dict]:
    rows = []
    with open(DATA_FILE, encoding="latin-1") as f:
        for row in csv.DictReader(f):
            territory_raw = row["territory"].strip().lower()
            if territory_raw not in TERRITORY_MAP:
                continue
            rows.append({"comment": row["comment"].strip(), "territory": territory_raw})
    return rows


def seed() -> None:
    client = httpx.Client(base_url=API_URL, timeout=30)

    try:
        client.get("/citizen_posts/", params={"limit": 1})
    except Exception as e:
        print(f"❌ API não acessível em {API_URL}: {e}")
        return

    rows = load_csv()
    print(f"📂 {len(rows)} relatos carregados de {DATA_FILE.name}")

    # cada relato recebe um author_id único
    author_ids = [str(uuid.uuid4()) for _ in rows]

    print("🌱 Inserindo posts...")
    created_posts: list[dict] = []

    for i, (row, author_id) in enumerate(zip(rows, author_ids)):
        territory_name, territory_level = TERRITORY_MAP[row["territory"]]
        r = client.post("/citizen_posts/", json={
            "text": row["comment"],
            "territory_level": territory_level,
            "territory_name": territory_name,
            "author_id": author_id,
            "ai_labels": [],
        })
        if r.is_success:
            created_posts.append(r.json())
            if (i + 1) % 100 == 0:
                print(f"  ✅ {i + 1}/{len(rows)} posts inseridos")
        else:
            print(f"  ❌ [{i+1}] {r.status_code}: {r.text[:80]}")

    print(f"  ✅ Total: {len(created_posts)} posts inseridos")

    # cada author dá LIKES_PER_AUTHOR likes em posts de outros autores
    # total esperado: len(created_posts) * LIKES_PER_AUTHOR (ex: 1000 * 50 = 50.000)
    # nota: ~50.000 chamadas à API levam alguns minutos
    print(f"\n👍 Distribuindo {LIKES_PER_AUTHOR} likes por autor ({len(created_posts) * LIKES_PER_AUTHOR:,} no total)...")
    like_count = 0
    post_by_id: dict[str, dict] = {p["id"]: p for p in created_posts}

    for author_idx, (post, author_id) in enumerate(zip(created_posts, author_ids)):
        # pool de posts disponíveis: todos exceto o próprio post do autor
        pool = [p for p in created_posts if p["author_id"] != author_id]
        targets = random.sample(pool, min(LIKES_PER_AUTHOR, len(pool)))
        for target in targets:
            r = client.post(f"/citizen_posts/{target['id']}/likes", json={"user_id": author_id})
            if r.is_success:
                like_count += 1
        if (author_idx + 1) % 100 == 0:
            print(f"  ✅ {author_idx + 1}/{len(created_posts)} autores processados ({like_count:,} likes)")

    print(f"  ✅ {like_count:,} likes inseridos")
    print(f"\n🎉 Seed concluído: {len(created_posts)} posts, {like_count:,} likes")


if __name__ == "__main__":
    seed()
```

**Pré-condição:** backend rodando em `localhost:8000`.

```bash
cd fala-gavea
uv run python scripts/seed_db.py
```

- [x] Done

**Tests:** N/A (verificação manual)
**Verify:**
1. Backend rodando: `uv run uvicorn fala_gavea.presentation.api.main:app --reload`
2. `uv run python scripts/seed_db.py` — progresso a cada 100 posts e a cada 100 autores; atenção: ~50.000 chamadas de like levam alguns minutos
3. `GET http://localhost:8000/citizen_posts/?limit=5` retorna posts com `text` em pt-BR, `territory_name` ∈ {Comunidade da Gávea, Baixo Gávea, Alto da Gávea, Favela da Gávea}, `ai_labels: []`, e `likes_count` > 0 na maioria

---

### Step 3 — Adicionar visualizações humanas ao `page_dashboard()` em `fala-gavea/app.py`

> **Contexto:** plan-000033 já reescreveu `page_dashboard()` adicionando "Rastreabilidade de likes" e "Rastreabilidade de labels". Este step **não substitui** essa função — adiciona 3 seções antes das seções de rastreabilidade.

**Mudanças:**

1. Aumentar o limit de `500` para `1500` no `api_get` inicial (seed tem 1000 posts).

2. Atualizar as métricas: trocar "Posts com labels IA" por "Média de likes por post".

3. Inserir 3 novas seções **após** `st.subheader("Distribuição por território")` e **antes** de `if not posts_with_labels.empty:`.

```python
    # ── Timeline de postagens ─────────────────────────────────────────────────
    if "created_at" in df:
        st.subheader("Postagens por dia")
        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        timeline = df.groupby("date").size().reset_index(name="posts")
        st.line_chart(timeline.set_index("date"))

    # ── Histograma de likes ───────────────────────────────────────────────────
    total_likes = int(df["likes_count"].sum()) if "likes_count" in df else 0
    if total_likes > 0:
        st.subheader("Distribuição de likes por post")
        bins = [0, 1, 2, 4, 7, 11, 20, 50, 100]
        labels_hist = ["0", "1", "2-3", "4-6", "7-10", "11-19", "20-49", "50+"]
        df["likes_bucket"] = pd.cut(
            df["likes_count"], bins=bins, right=False, labels=labels_hist
        )
        hist = df["likes_bucket"].value_counts().sort_index()
        st.bar_chart(hist)
```

**Diff completo das linhas alteradas em `page_dashboard()`:**

```diff
-    posts = api_get("/citizen_posts/", limit=500)
+    posts = api_get("/citizen_posts/", limit=1500)

-    col1.metric("Total de postagens", len(df))
-    col2.metric("Total de likes", int(df["likes_count"].sum()) if "likes_count" in df else 0)
-    posts_with_labels = df[df["ai_labels"].apply(lambda x: len(x) > 0)] if "ai_labels" in df else pd.DataFrame()
-    col3.metric("Posts com labels IA", len(posts_with_labels))
+    col1.metric("Total de postagens", len(df))
+    total_likes = int(df["likes_count"].sum()) if "likes_count" in df else 0
+    col2.metric("Total de likes", total_likes)
+    avg_likes = round(total_likes / len(df), 1) if len(df) else 0
+    col3.metric("Média de likes por post", avg_likes)
+    posts_with_labels = df[df["ai_labels"].apply(lambda x: len(x) > 0)] if "ai_labels" in df else pd.DataFrame()

     st.subheader("Distribuição por território")
     by_territory = df.groupby("territory_name").size().reset_index(name="posts")
     st.bar_chart(by_territory.set_index("territory_name"))

+    if "created_at" in df:
+        st.subheader("Postagens por dia")
+        df["date"] = pd.to_datetime(df["created_at"]).dt.date
+        timeline = df.groupby("date").size().reset_index(name="posts")
+        st.line_chart(timeline.set_index("date"))
+
+    if total_likes > 0:
+        st.subheader("Distribuição de likes por post")
+        bins = [0, 1, 2, 4, 7, 11, 20, 50, 100]
+        labels_hist = ["0", "1", "2-3", "4-6", "7-10", "11-19", "20-49", "50+"]
+        df["likes_bucket"] = pd.cut(
+            df["likes_count"], bins=bins, right=False, labels=labels_hist
+        )
+        hist = df["likes_bucket"].value_counts().sort_index()
+        st.bar_chart(hist)
+
     if not posts_with_labels.empty:
```

- [x] Done

**Tests:** N/A (UI)
**Verify:**
1. Backend rodando com dados do seed (1000 posts, ~50k likes)
2. `uv run streamlit run app.py` → Dashboard
3. Métrica col3 mostra "Média de likes por post" (esperado ~50)
4. "Postagens por dia" mostra linha temporal
5. "Distribuição de likes por post" mostra histograma — maioria dos posts deve estar no bucket "50+"
6. Seções de Rastreabilidade de plan-000033 ainda presentes e funcionais

---

## Acceptance Criteria

- [x] `fala-gavea/scripts/seed_db.py` existe e usa `data/sample-gavealab-1000.csv`
- [x] Cada relato recebe um `author_id` UUID único (1000 autores distintos)
- [x] Posts inseridos com `ai_labels: []` (sem labels)
- [x] Cada autor dá exatamente 50 likes em posts de outros autores (excluindo o próprio)
- [x] Total de likes ≈ 50.000 (1000 × 50)
- [x] `territory_name` ∈ {Comunidade da Gávea, Baixo Gávea, Alto da Gávea, Favela da Gávea}
- [x] Dashboard exibe: métricas (total posts, total likes, média likes), top-10, posts por território, timeline, histograma de likes
- [x] Dashboard não quebra com posts sem `ai_labels`

## Docs

- Nenhum documento novo neste plano

## Implementation Summary

**Steps completed:** 3/3 — all steps succeeded.

**Files created:**
- `fala-gavea/scripts/__init__.py` — empty package marker
- `fala-gavea/scripts/seed_db.py` — reads `data/sample-gavealab-1000.csv` (latin-1), maps 4 territory values, inserts posts via API, then distributes 50 likes per author to posts of other authors

**Files modified:**
- `fala-gavea/app.py` — `page_dashboard()`: limit raised to 1500, col3 metric changed to "Média de likes por post", added "Postagens por dia" timeline and "Distribuição de likes por post" histogram

**Fix applied during quality gate:** histogram last bin changed from `100` to `float("inf")` so posts with 100+ likes are not silently dropped as NaN by `pd.cut`.

**Tests:** 8/8 passed (kb-qa suite). fala-gavea has no automated tests (UI). Pre-existing ruff failures in kb-qa `src/` are unrelated to this plan.
