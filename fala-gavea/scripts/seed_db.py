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

LIKES_PER_AUTHOR = 20


def load_csv() -> list[dict]:
    rows = []
    with open(DATA_FILE, encoding="utf-8") as f:
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
