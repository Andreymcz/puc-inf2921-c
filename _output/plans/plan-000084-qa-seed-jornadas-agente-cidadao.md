# QA Log — plan-000084 | Seed dataset para jornadas de agente e cidadão

> Companion Q&A record for plan-000084. The substantive Q&A (4 design decisions) lives
> in [research-000080](../research-logs/research-000080-seed-jornadas-agente-cidadao.md);
> this planning turn was non-interactive.

## Brief

source: research-000080 — montar seed dataset para as jornadas de agente e cidadão no
fala-gavea (âncoras determinísticas de iluminação/lixo/segurança não resolvidas nos
últimos 30 dias para o agente; encaminhamento do citizen01 em andamento + mix de
estados para "meus relatos não resolvidos").

## Q&A

**Q1:** "planeje"

**A1:** Gerado plan-000084 (single-plan, review light) com duas frentes:
(A) novo CSV `data/seed_journey_anchors.csv` + `scripts/seed_journey_anchors.py`
rodando como **última** fase do `seed_all.py` (âncoras permanecem `pendente`);
(B) extensão de `seed_citizen01.py` para fixar o forwarding A em `solucao_em_andamento`
+ comentário do agente e criar forwarding B `finalizado` + comentário, deixando
`created_ids[5:10]` pendente. Decisões herdadas da research-000080: resolução
forwarding-level, datas fixas (demo 2026-06-27), foco iluminação + lixo + segurança.

## Decisões de planejamento

- **CSV de âncoras separado** (não dentro do `PROMPT-gerar-seed.md`) — preserva
  determinismo e legibilidade; o prompt continua para o corpo estatístico.
- **Idempotência por `text`** no script de âncoras (guarda via `POST /reports/query`).
- **Pin do citizen01 na fase 4** (antes do lifecycle da fase 8) garante que os estados
  não sejam sobrescritos pelo `seed_forwarding_lifecycle`.
