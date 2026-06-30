# DONE | 2026-06-28 20:52 UTC |
# Plan 000084 | plan/fala-gavea | 2026-06-28 20:36 UTC | Seed dataset para jornadas de agente e cidadão | Review: light
plan_format_version: 1
source: research-000080

## Brief

> source: research-000080 — montar seed dataset para as jornadas de agente e cidadão
> no fala-gavea: (R1) nova fase determinística de âncoras de jornada (CSV + script)
> rodando após os encaminhamentos, com âncoras `pendente` de iluminação (postes) +
> lixo + segurança datadas nos últimos 30 dias (demo fixa 2026-06-27); (R2) fixar o
> encaminhamento do citizen01 em `solucao_em_andamento` + comentário do agente, com
> opcional 2º encaminhamento `finalizado` para contraste; (R3) mix de estados para
> "meus relatos não resolvidos". Modelo de resolução atual (forwarding-level),
> datas fixas.

## Objetivo

Tornar **demonstráveis e determinísticas** duas jornadas no fala-gavea:

1. **Agente** — entra e vê *postes apagados/queimados* (e lixo/segurança) **reportados
   e não resolvidos** nos **últimos 30 dias**, para criar encaminhamento.
2. **Cidadão (citizen01)** — vê o **andamento da empresa responsável** no seu
   encaminhamento e **lista seus relatos não resolvidos** (com contraste entre
   pendente / em andamento / finalizado).

O gap é de **dados + determinismo da seed**, não de API (endpoints já existem — ver
research-000080 §A5).

## Contexto verificado

- **Resolução é forwarding-level** (decisão: manter). `ReportStatus.resolvido` não tem
  transição; relatos vão `pendente → encaminhado`. "Não resolvido" =
  `pendente`/`em_analise`, ou `encaminhado` cujo forwarding ≠ `finalizado`
  ([seed_forwarding_lifecycle.py:8-12](fala-gavea/scripts/seed_forwarding_lifecycle.py#L8-L12)).
- **Datas só entram via CSV em massa.** `BulkCreateReports` honra a coluna `data`
  ([bulk_create_reports.py:92-98](fala-gavea/src/fala_gavea/application/use_cases/reports/bulk_create_reports.py#L92-L98));
  `POST /reports` ao vivo grava `created_at=now`. → Âncoras datadas no passado **exigem**
  o endpoint `POST /admin/seed/relatos` (CSV).
- **Convenção API-only de seed** (fala-gavea constitution/CLAUDE.md): scripts de seed
  falam com a API via httpx; **nada de escrita direta no DB**.
- **Ordem das fases em [seed_all.py](fala-gavea/scripts/seed_all.py):** 1 users, 2 relatos,
  3 forwardings (amostra aleatória ~50% dos pendentes), 4 citizen01, 5 votes,
  6 comments, 7 saved-filters, 8 lifecycle. → Âncoras inseridas **após a fase 3**
  permanecem `pendente` (o amostrador aleatório nunca as vê).
- **Endpoints confirmados:** worklist do agente `POST /reports/query`
  (`report_type_ids`+`statuses`+`since`, [report_repository.py:10-20](fala-gavea/src/fala_gavea/domain/repositories/report_repository.py#L10-L20));
  andamento do cidadão `GET /reports/{id}/forwardings` e `GET /forwardings/mine`;
  comentário `POST /forwardings/{id}/comments` `{"text":...}`; status
  `PATCH /forwardings/{id}/status` `{"status":...}`.
- **Header CSV do endpoint:** `user_id,texto_relato,latitude,longitude,data,topico,urgency`
  (`id_cidadao` é alias de `user_id`). Tópicos exatos (sem acento):
  `Iluminacao publica`, `Lixo e conservacao`, `Seguranca e circulacao`, etc.
- **Bounding box Gávea:** lat -22.975 … -22.953 | lon -43.235 … -43.205.
- **Demo date fixa:** 2026-06-27 → janela de âncoras **2026-05-29 … 2026-06-26**.

## Estratégia

Duas frentes independentes que, juntas, cobrem as duas jornadas:

**Frente A — âncoras do agente (R1):** um CSV curado separado
(`data/seed_journey_anchors.csv`) + um script de fase nova
(`scripts/seed_journey_anchors.py`) que faz upload via `POST /admin/seed/relatos`,
rodando como **última fase** do `seed_all.py`. Por entrar depois da fase 3, as âncoras
ficam garantidamente `pendente`. CSV separado (não mistura com o corpo estatístico do
`PROMPT-gerar-seed.md`, preservando determinismo e legibilidade).

**Frente B — andamento do cidadão (R2/R3):** estender `seed_citizen01.py` para fixar,
de forma determinística, o estado dos encaminhamentos do citizen01 e dar um **mix** de
estados aos relatos dele. Como o pin acontece na fase 4 (antes da fase 8 lifecycle),
o `seed_forwarding_lifecycle` (que só avança forwardings em `aguardando_solucao`)
**não sobrescreve** os estados fixados.

### Composição das âncoras (20 linhas)

| Tópico | Qtd | Conteúdo | Status resultante |
|---|---|---|---|
| `Iluminacao publica` | 10 | postes apagados/queimados em ruas da Gávea (foco do brief) | `pendente` |
| `Lixo e conservacao` | 5 | acúmulo/coleta irregular | `pendente` |
| `Seguranca e circulacao` | 5 | trechos sem iluminação/pontos de risco | `pendente` |

- Datas espalhadas em 2026-05-29 … 2026-06-26; lat/lon espalhados pelo bounding box;
  urgência variada; **voz em 1ª pessoa**; ~6-8 `user_id` sintéticos
  (`anchor01`…`anchorNN` → autores `anchorNN@seed.gavea.br`).

### Estado final do citizen01 (10 relatos, criados na fase 4)

| Relatos (índices) | Encaminhamento | Status forwarding | Significado p/ "meus relatos não resolvidos" |
|---|---|---|---|
| [0,1,2] (+2 de outros) | A (CET-Rio / RioLuz) | `solucao_em_andamento` + comentário do agente | **não resolvido** (em andamento) |
| [3,4] | B (RioLuz) | `finalizado` + comentário de conclusão | resolvido (contraste) |
| [5..9] | — (sem encaminhamento) | `pendente` | **não resolvido** |

Resultado visível: 5 pendente + 3 em andamento = **8 não resolvidos**; 2 resolvidos.

## Passos de implementação

1. **Criar `fala-gavea/data/seed_journey_anchors.csv`** — 20 linhas curadas, cabeçalho
   exato `user_id,texto_relato,latitude,longitude,data,topico,urgency`. Comentário de
   cabeçalho não é suportado por CSV puro → documentar a "demo date" no script/SCHEMA, não
   no CSV. Conteúdo conforme tabela "Composição das âncoras".
   - Docs: SCHEMA.md (nota sobre o arquivo de âncoras)

2. **Criar `fala-gavea/scripts/seed_journey_anchors.py`** — espelhando o estilo de
   `seed_relatos.py`:
   - args: `--url`, `--csv` (default `data/seed_journey_anchors.csv`), `--user`/`--password`
     (admin), `--force`.
   - login admin → guarda de idempotência: `POST /reports/query` com
     `{"text": "<frase-âncora canônica>", "limit": 1}`; se `total > 0` e sem `--force`,
     imprime "journey anchors already present — skipping" e retorna.
   - upload via `POST /admin/seed/relatos` (multipart, igual ao `seed_relatos.py`);
     imprimir `inserted/skipped/errors`.
   - type annotations em todas as funções públicas.
   - Docstring com a demo date e a nota "datas fixas; regerar se a demo mudar de mês".
   - Docs: README.md / CLAUDE.md (linha de uso `seed_journey_anchors.py`)

3. **Wire da fase no `fala-gavea/scripts/seed_all.py`** — adicionar **Fase 9
   (última, após lifecycle)** "Journey anchors" + flag `--skip-journey-anchors`. Rodar
   após a fase 8 garante que as âncoras nunca sejam encaminhadas/avançadas. Atualizar o
   bloco final "Verify showcase features" com as duas jornadas (payload do agente +
   passos do cidadão).
   - Docs: CLAUDE.md (seção Build & Run / make seed)

4. **Estender `fala-gavea/scripts/seed_citizen01.py`** (dentro do mesmo `with httpx.Client`,
   após criar o forwarding A e ainda com `headers_agente`):
   a. `PATCH /forwardings/{A}/status` → `{"status": "solucao_em_andamento"}`.
   b. `POST /forwardings/{A}/comments` (como agente) → comentário de **andamento** concreto
      (ex.: "Equipe RioLuz esteve em campo em 24/06; vistoria concluída, troca das lâmpadas
      programada para o próximo ciclo de manutenção.").
   c. Criar **forwarding B** como agente a partir de `created_ids[3:5]`
      (`report_ids`=[idx3, idx4], institution "RioLuz"), `PATCH .../status` →
      `{"status": "finalizado"}`, e `POST .../comments` → comentário de **conclusão**
      (ex.: "Serviço concluído: lâmpadas substituídas e rede testada. Encaminhamento
      finalizado.").
   d. Deixar `created_ids[5:10]` sem encaminhamento (permanecem `pendente`).
   e. Atualizar o bloco de summary/"To verify in the app" para refletir o mix de estados
      (8 não resolvidos / 2 resolvidos) e a leitura do andamento.
   - Mantém a guarda de idempotência existente (`/forwardings/mine` > 0 → skip).
   - Docs: N/A (script self-documenting)

5. **Atualizar docs de seed (R4/R5)** — em `fala-gavea/seeds/relatos/SCHEMA.md` e
   `fala-gavea/CLAUDE.md`: mencionar o arquivo de âncoras e a fase, a demo date fixa, e
   os **payloads exatos** de verificação das jornadas (query do agente com
   `report_type_ids`/`statuses`/`since`; `GET /reports/{id}/forwardings` do cidadão).
   - Docs: SCHEMA.md, CLAUDE.md

## Critérios de aceitação

- [x] `data/seed_journey_anchors.csv` existe, cabeçalho exato de 7 colunas, 20 linhas,
      tópicos válidos (sem acento), datas em 2026-05-29…2026-06-26, lat/lon no bounding box.
      *(validado por script: 20 linhas, 10/5/5, todas as datas/coords/ascii OK).*
- [x] `scripts/seed_journey_anchors.py` sobe o CSV via `POST /admin/seed/relatos`, é
      idempotente (guarda por `text` via `/reports/query`), aceita `--force`, e tem type
      annotations. *(ruff + pyright limpos).*
- [x] `seed_all.py` roda "Journey anchors" como **última** fase (Fase 9, após lifecycle),
      com `--skip-journey-anchors`.
- [~] Após `make seed` (showcase), `POST /reports/query` retorna **≥10** relatos. **Runtime**
      — requer API + Ollama no ar; CSV garante 10 linhas `Iluminacao publica` `pendente`.
- [x] citizen01 tem forwarding A em `solucao_em_andamento` **com comentário** de agente
      e forwarding B em `finalizado` **com comentário**; `created_ids[5:10]` ficam `pendente`.
      *(implementado e revisado em seed_citizen01.py).*
- [~] `GET /reports/{id}/forwardings` devolve `solucao_em_andamento`. **Runtime** — coberto
      pelo PATCH de status em seed_citizen01.py.
- [~] `POST /reports/query` com `author_id=<citizen01>` mix coerente. **Runtime** —
      8 não resolvidos (5 pendente + 3 em andamento) / 2 finalizados, por construção.
- [x] Lifecycle (fase 8) **não** altera os forwardings A/B do citizen01 (já fora de
      `aguardando_solucao`). *(verificado contra o filtro `status == aguardando_solucao`
      em seed_forwarding_lifecycle.py; pin acontece na fase 4, antes da fase 8).*
- [x] SCHEMA.md/CLAUDE.md documentam a fase de âncoras, a demo date e os payloads de demo.

## Verificação

- `cd fala-gavea && uv run ruff check scripts/ && uv run pyright scripts/seed_journey_anchors.py`
  (se pyright cobrir scripts; senão só ruff).
- Subir a API com bootstrap admin; `make seed` (perfil showcase); conferir contagens:
  - Agente: query da worklist (acima) → ≥10 iluminação não resolvidas na janela.
  - Cidadão: login citizen01 → "Meus relatos" mostra 10; `/encaminhamentos` mostra A
    (em andamento, com comentário) e B (finalizado, com comentário).
- Re-rodar a fase de âncoras sem `--force` → "already present — skipping" (idempotência).
- `cd fala-gavea && uv run pytest` (garantir que nada quebrou; os scripts de seed não têm
  testes automatizados — verificação por execução).

## Fora de escopo

- Adicionar transição `ReportStatus.resolvido` / novo endpoint (decisão: manter modelo
  forwarding-level; ver research-000080 §A1 e plan-000183).
- Lógica de UI para o filtro "não resolvido" via join relato→encaminhamento (concern de
  frontend/consulta; aqui só garantimos os **dados**). Registrar como nota.
- Datas relativas ao seed-time (decisão: datas fixas / demo pontual).
- Reescrever o `PROMPT-gerar-seed.md` (continuação do plan-000076); aqui as âncoras são um
  CSV curado separado.
- Escrita direta no DB (viola a convenção API-only).

## Notas / riscos

- **Staleness das datas fixas (aceito):** a janela de 30 dias é relativa ao relógio; com
  demo date fixa em 2026-06-27, demos muito depois de jul/2026 verão a worklist encolher.
  Mitigação documentada: regerar/deslocar as datas do CSV de âncoras se a demo mudar de mês.
- **Idempotência por `text`:** depende de `ReportFilters.text` (LIKE). Escolher uma frase
  âncora canônica suficientemente única (ex.: rua + detalhe específico) para evitar falso
  positivo com o corpo estatístico.
- **"Meus relatos não resolvidos" no front:** sob o modelo atual, `report.status` sozinho
  não distingue resolvido; a distinção exige join com o forwarding. A seed entrega o mix
  de estados; a leitura correta no UI é responsabilidade do frontend (fora de escopo).
- **Ordem é crítica:** se alguém mover a fase de âncoras para antes da fase 3, elas serão
  encaminhadas pelo amostrador aleatório e a worklist do agente esvazia. Manter como
  última fase.

## Review (light)

- Tooling de seed/demo: sem código de domínio/persistência, sem novos endpoints, sem
  alteração de schema. Risco baixo.
- Conformidade: scripts falam só com a API (convenção API-only ✓); type annotations ✓;
  tópicos/cabeçalho conferidos contra `seed.py`/`SCHEMA.md` ✓.
- Determinismo: âncoras como última fase (nunca encaminhadas); pin do citizen01 na fase 4
  (antes do lifecycle) — ambos verificados contra a ordem real de `seed_all.py`.

## Resumo da implementação (manual mode, 2026-06-28 20:52 UTC)

**5/5 passos concluídos.** Todos os arquivos no repositório `fala-gavea/`.

| # | Passo | Arquivos |
|---|-------|----------|
| 1 | CSV de âncoras (20 linhas: 10 iluminação + 5 lixo + 5 segurança) | `data/seed_journey_anchors.csv` (criado) |
| 2 | Script de upload idempotente | `scripts/seed_journey_anchors.py` (criado) |
| 3 | Fase 9 + `--skip-journey-anchors` + bloco de verificação das jornadas | `scripts/seed_all.py` |
| 4 | citizen01: forwarding A `solucao_em_andamento`+comentário, forwarding B `finalizado`+comentário, `[5:10]` `pendente` | `scripts/seed_citizen01.py` (helpers `_create_forwarding`/`_set_forwarding_status`/`_add_forwarding_comment`) |
| 5 | Docs: arquivo de âncoras, demo date fixa, payloads de verificação | `seeds/relatos/SCHEMA.md`, `CLAUDE.md` |

**Contratos de API confirmados em código** antes de implementar: header CSV mapeado em
`routers/seed.py` (`texto_relato→descricao`, `latitude→lat`, `longitude→lon`,
`user_id`/`id_cidadao`); `/reports/query` expõe `text`/`since`/`statuses`/`report_type_ids`/
`author_id`/`total`; comentários em `POST /forwardings/{id}/comments` `{"text"}` (1–500);
status em `PATCH /forwardings/{id}/status` `{"status"}`.

**Frase âncora canônica** (guarda de idempotência): *"Tres postes consecutivos apagados na
Rua Professor Saboia Ribeiro"* — substring da linha 1 do CSV; sem colisão com os textos do
citizen01.

**Quality gate:** `ruff check` (limpo nos arquivos alterados; o único erro restante é
pré-existente em `train_topic_classifier.ipynb`, fora de escopo), `pyright` 0 erros nos 3
scripts, `pytest` **308 passed**. `py_compile` OK.

**Verificações de runtime pendentes (3 critérios `[~]`):** exigem API + Ollama no ar +
`make seed`. Garantidas por construção (CSV/lógica), a conferir na demo. Nota de fora de
escopo do plano: a leitura "não resolvido" no front (join relato→forwarding) é
responsabilidade do frontend.

**Nota:** o working tree do `fala-gavea` tinha mudanças de frontend não relacionadas
(`ForwardingsPage.tsx`, `PublicForwardingsPage.tsx`, `api.ts`) anteriores a este plano —
não fazem parte deste commit.
