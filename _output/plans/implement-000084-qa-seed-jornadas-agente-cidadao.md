# Implement QA Log 000084 | 2026-06-28 20:54 UTC | Seed dataset para jornadas de agente e cidadão

> Brief: source: research-000080 — montar seed dataset para jornadas de agente e cidadão no fala-gavea (plan 000084)
> Mode: manual (5 steps, tightly-coupled seed tooling). Review: light.

## Resultado

5/5 passos concluídos. Mudanças no repositório `fala-gavea/` (seed/demo tooling, sem
código de domínio/persistência, sem novos endpoints, sem alteração de schema).

| Arquivo | Tipo |
|---|---|
| `fala-gavea/data/seed_journey_anchors.csv` | criado (20 âncoras curadas) |
| `fala-gavea/scripts/seed_journey_anchors.py` | criado (upload idempotente) |
| `fala-gavea/scripts/seed_all.py` | Fase 9 + `--skip-journey-anchors` + bloco de verificação |
| `fala-gavea/scripts/seed_citizen01.py` | forwarding A `solucao_em_andamento`+comentário, B `finalizado`+comentário, `[5:10]` pendente |
| `fala-gavea/seeds/relatos/SCHEMA.md` | doc das âncoras + demo date + payloads |
| `fala-gavea/CLAUDE.md` | linha de uso + fase + jornadas |

## Q&A / decisões de execução

**P: A coluna `texto_relato` do CSV é lida diretamente?**
R: Não. `routers/seed.py` mapeia `texto_relato→descricao`, `latitude→lat`, `longitude→lon`,
`user_id`/`id_cidadao→user_id` antes de chamar `BulkCreateReports`. Cabeçalho exato confirmado:
`user_id,texto_relato,latitude,longitude,data,topico,urgency`.

**P: Como garantir que as âncoras fiquem `pendente`?**
R: Rodando como Fase 9 (após o lifecycle/Fase 8). O amostrador aleatório de encaminhamentos
(Fase 3) já rodou; nunca vê as âncoras.

**P: O lifecycle (Fase 8) não sobrescreve os forwardings A/B do citizen01?**
R: Não. O pin acontece na Fase 4 (antes da Fase 8). O lifecycle só avança forwardings com
`status == aguardando_solucao`; A está em `solucao_em_andamento` e B em `finalizado`.

**P: Idempotência?**
R: `seed_journey_anchors.py` consulta `/reports/query {"text": "<frase canônica>", "limit": 1}`
e pula se `total > 0` (a menos de `--force`). `seed_citizen01.py` mantém a guarda existente
(`/forwardings/mine > 0 → skip`).

## Quality gate

- `ruff check` — limpo nos arquivos alterados (único erro restante é pré-existente em
  `train_topic_classifier.ipynb`, fora de escopo).
- `pyright` — 0 erros nos 3 scripts.
- `pytest` — **308 passed**.
- 3 critérios de aceitação `[~]` são verificações de runtime (exigem API + Ollama + `make seed`),
  garantidas por construção; a conferir na demo.
