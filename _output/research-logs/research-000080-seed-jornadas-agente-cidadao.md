# Research 000080 | research/fala-gavea | 2026-06-27 02:30 UTC | Montar seed dataset para jornadas de agente e cidadão
tags: seed-data, fala-gavea, journeys, forwardings, demo-fixtures
spawned: plan-000084, plan-000084, research-000085

## User brief

> montar seed dataset considerando fluxos de jornadas agent e cidadao na plataforma.
> no caso do agente: entra e vai trabalhar em postes queimados reportados e não
> resolvidos nos últimos 30 dias. cidadao: post na rua dele ainda não foi resolvido,
> ele quer saber como está o andamento da empresa responsável. listar meus relatos
> nao resolvidos.

## Agent interpretation

A plataforma alvo é **fala-gavea** (FastAPI + SQLite, arquitetura limpa), não o
gavealab-poc/kb-qa descrito no design-intent do repo pai. O pedido é montar uma seed
que torne **demonstráveis** duas jornadas concretas:

1. **Jornada do agente** — agente público entra e precisa ver *postes apagados/queimados*
   (`Iluminacao publica`) **reportados e ainda não resolvidos** nos **últimos 30 dias**,
   para então criar encaminhamento.
2. **Jornada do cidadão** — cidadão cujo relato na rua dele **ainda não foi resolvido**
   quer (a) ver o **andamento da empresa responsável** (status + atualizações do
   encaminhamento) e (b) **listar seus relatos não resolvidos**.

A seed atual não garante esses fluxos: o volume recente é raso e os scripts de
encaminhamento/ciclo são aleatórios.

## Files

- [fala-gavea/src/fala_gavea/domain/entities/report.py](fala-gavea/src/fala_gavea/domain/entities/report.py) — `Report`, `ReportStatus` (pendente/em_analise/encaminhado/resolvido)
- [fala-gavea/src/fala_gavea/domain/entities/forwarding.py](fala-gavea/src/fala_gavea/domain/entities/forwarding.py) — `Forwarding`, `ForwardingStatus` (aguardando_solucao/solucao_em_andamento/finalizado)
- [fala-gavea/src/fala_gavea/application/use_cases/reports/bulk_create_reports.py](fala-gavea/src/fala_gavea/application/use_cases/reports/bulk_create_reports.py) — `created_at` vem da coluna `data` do CSV; status inicial sempre `pendente`
- [fala-gavea/src/fala_gavea/domain/repositories/report_repository.py](fala-gavea/src/fala_gavea/domain/repositories/report_repository.py) — `ReportFilters` (report_type_ids, statuses, author_id, since, until, bbox, text)
- [fala-gavea/scripts/seed_all.py](fala-gavea/scripts/seed_all.py) — orquestrador de 8 fases
- [fala-gavea/scripts/seed_forwardings.py](fala-gavea/scripts/seed_forwardings.py) — amostra **aleatória ~50%** dos pendentes
- [fala-gavea/scripts/seed_forwarding_lifecycle.py](fala-gavea/scripts/seed_forwarding_lifecycle.py) — split `idx%3` e **nota crítica** sobre resolução só no encaminhamento
- [fala-gavea/scripts/seed_citizen01.py](fala-gavea/scripts/seed_citizen01.py) — 10 relatos + 1 encaminhamento (CET-Rio/RioLuz) em `aguardando_solucao`
- [fala-gavea/seeds/relatos/PROMPT-gerar-seed.md](fala-gavea/seeds/relatos/PROMPT-gerar-seed.md) — prompt gerador do CSV (plan-000076)
- data/seed_relatos_fala_gavea_{200,5k}.csv — CSVs showcase/full

---

## Achados principais (estado atual)

### A1 — Resolução é modelada no ENCAMINHAMENTO, não no relato

`ReportStatus.resolvido` existe no enum mas **não tem transição de API**. Relatos vão
`pendente → encaminhado` (ao serem encaminhados) e param ali
([seed_forwarding_lifecycle.py:8-12](fala-gavea/scripts/seed_forwarding_lifecycle.py#L8-L12)).
"Resolução" só existe via `ForwardingStatus.finalizado`. **Consequência direta:**
"relato não resolvido" não pode ser lido do `report.status` — é preciso olhar o
encaminhamento vinculado.

**Decisão do usuário:** manter o modelo atual (resolução no encaminhamento), sem criar
transição `resolvido`. Logo, para as jornadas, *não resolvido* =
`status ∈ {pendente, em_analise}` **ou** `encaminhado` cujo forwarding ≠ `finalizado`.

### A2 — Datas entram via CSV; relatos criados ao vivo são "agora"

`BulkCreateReports` honra a coluna `data` (ISO) → `created_at`
([bulk_create_reports.py:92-98](fala-gavea/src/fala_gavea/application/use_cases/reports/bulk_create_reports.py#L92-L98)).
Já `POST /reports` (cidadão/agente ao vivo) **não aceita data** → `created_at = now`.
Portanto, a única forma de ter relatos datados "há N dias" é pelo **CSV em massa**.

### A3 — Volume recente é raso para a jornada do agente

Janela de 30 dias relativa a hoje (2026-06-27) = 2026-05-28 … 2026-06-26:

| CSV | linhas | intervalo de datas | linhas últimos 30d | **Iluminação últimos 30d** |
|---|---|---|---|---|
| showcase 200 (default) | 200 | 2025-06-18 … 2026-06-14 | 9 | **1** |
| full 5k | 5000 | 2025-06-18 … 2026-06-18 | 114 | 13 |

O perfil **showcase** (padrão de demo) entrega **1 relato de iluminação** na janela →
a jornada do agente é praticamente vazia. O 5k tem 13, mas é ruído estatístico
não-curado e sua data mais recente (2026-06-18) já está 9 dias defasada.

### A4 — Seed de encaminhamentos/ciclo é não-determinístico

`seed_forwardings` encaminha uma **amostra aleatória de ~50%** dos pendentes agrupada
por tipo; `seed_forwarding_lifecycle` distribui estados por `idx%3`. O encaminhamento do
citizen01 começa em `aguardando_solucao` e **pode ou não** ser avançado. Logo, o
"andamento da empresa responsável" que o cidadão vê **não é garantido** — às vezes
estará parado em `aguardando_solucao`, sem progresso para mostrar.

### A5 — Os endpoints das jornadas já existem

- **Agente — worklist de postes não resolvidos últimos 30d:**
  `POST /reports/query` com `report_type_ids=[<id Iluminacao>]`,
  `statuses=["pendente","em_analise"]`, `since="2026-05-28"`. `ReportFilters` suporta
  todos esses campos ([report_repository.py:10-20](fala-gavea/src/fala_gavea/domain/repositories/report_repository.py#L10-L20)).
- **Cidadão — andamento da empresa:** `GET /reports/{id}/forwardings` (status +
  proposed_solution + institution) e `GET /forwardings/mine`.
- **Cidadão — listar meus relatos:** `POST /reports/query` com `author_id=<citizen01>`
  (+ `statuses`). ⚠️ `GET /reports/mine` é **só para relatos anônimos** (anonymous_token),
  não serve para cidadão logado ([reports.py:342-347](fala-gavea/src/fala_gavea/presentation/api/routers/reports.py#L342-L347)).

**Conclusão:** o gap **não é de API** — é de **dados/determinismo da seed**.

---

## Recomendações

### R1 (HIGH) — Fase determinística de "âncoras de jornada" inserida APÓS encaminhamentos

Criar `scripts/seed_journey_anchors.py` + `data/seed_journey_anchors.csv` e rodá-lo como
**última fase** do `seed_all.py` (depois de `seed_forwardings`/`lifecycle`). Como as
âncoras entram *depois* da amostragem aleatória, elas permanecem `pendente` —
garantindo a worklist do agente **sem tocar no amostrador aleatório**.

Conteúdo das âncoras (datas fixas na janela 2026-05-28 … 2026-06-26, espalhadas pelo
bbox da Gávea, voz em 1ª pessoa, status `pendente`):

- **~10 `Iluminacao publica`** — postes apagados/queimados (foco do brief).
- **~5 `Lixo e conservacao`** + **~5 `Seguranca e circulacao`** — para a jornada do
  agente generalizar além de iluminação (decisão: iluminação + 1-2 eixos).

Por que datas fixas: decisão do usuário (demo pontual). Documentar a "data de demo"
(2026-06-27) no cabeçalho do CSV/script e que as âncoras devem ser **regeradas** se a
demo mudar de data (a janela de 30d é relativa ao relógio).

### R2 (HIGH) — Tornar o "andamento" do citizen01 determinístico

Estender `seed_citizen01.py` (ou nova fase pós-lifecycle) para, ao final:
1. `PATCH /forwardings/{id}/status` → **`solucao_em_andamento`** no encaminhamento
   CET-Rio/RioLuz do citizen01;
2. `POST` de **comentário do agente** narrando progresso concreto (ex.: "Equipe RioLuz
   esteve em campo em 24/06; vistoria concluída, troca das lâmpadas programada para o
   próximo ciclo"). Isso é exatamente o "andamento da empresa responsável" que o
   cidadão consulta.
3. (Opcional, recomendado) criar um **2º encaminhamento** do citizen01 já em
   **`finalizado`** + comentário de conclusão, para dar **contraste** entre relato
   resolvido vs. não resolvido na lista.

### R3 (MEDIUM) — Explicitar o gap "resolução-no-relato" e dar mix de estados ao citizen01

Sob o modelo atual (A1), "meus relatos não resolvidos" **não é filtrável por
`report.status`** (nenhum relato fica `resolvido`). Para a jornada ler corretamente:
- A lista deve **fazer join relato → encaminhamento** e tratar `finalizado` como
  "resolvido" (regra de UI/consulta, não de domínio).
- A seed deve dar ao citizen01 um **mix** de estados para o contraste ficar visível:
  relatos `pendente` (sem encaminhamento) + relatos em encaminhamento
  `solucao_em_andamento` (R2) + 1 relato em encaminhamento `finalizado` (R2.3).

Registrar isto como limitação conhecida (ligada ao plan-000183, que adiou a transição
`resolvido`). Se no futuro quiserem filtro por status do relato, reabrir a decisão de
adicionar `ReportStatus.resolvido`.

### R4 (MEDIUM) — Alinhar o PROMPT-gerar-seed com as âncoras de jornada

Atualizar [PROMPT-gerar-seed.md](fala-gavea/seeds/relatos/PROMPT-gerar-seed.md)
(continuação do plan-000076) para emitir, além do corpo estatístico, um **bloco de
âncoras recentes**: cluster `Iluminacao publica` "poste apagado/queimado" com datas nos
últimos 30 dias relativos à **data de demo fixada** (pinada no prompt). Manter
cabeçalho de 7 colunas e lista de tópicos idênticos a `seed.py`/`SCHEMA.md`. Alternativa
limpa: manter as âncoras num CSV separado (R1) e deixar o PROMPT só para o corpo
estatístico — evita misturar dados curados com gerados.

### R5 (LOW) — Reprodutibilidade e documentação de demo

- Garantir a ordem em `seed_all.py`: âncoras como **última** fase (após forwardings,
  lifecycle, citizen01) para preservarem `pendente`.
- Documentar no README/seed os **payloads exatos** das duas jornadas (query do agente
  com `since`/`report_type_ids`; `/reports/{id}/forwardings` do cidadão) e as contas de
  demo (agente@gavea.br, citizen01@gavea.br), para a banca reproduzir em 2 cliques.

---

## Recommendations summary

| # | Prioridade | Recomendação |
|---|---|---|
| R1 | HIGH | Nova fase `seed_journey_anchors` (CSV + script) rodando **após** os encaminhamentos → âncoras `pendente` de iluminação + lixo + segurança nos últimos 30 dias (datas fixas). |
| R2 | HIGH | Fixar o andamento do citizen01: PATCH encaminhamento → `solucao_em_andamento` + comentário do agente; opcional 2º encaminhamento `finalizado`. |
| R3 | MEDIUM | Explicitar que "não resolvido" exige join relato→encaminhamento; dar mix de estados ao citizen01; registrar limitação (plan-000183). |
| R4 | MEDIUM | Atualizar PROMPT-gerar-seed (plan-000076) para âncoras recentes de iluminação, ou separar âncoras em CSV próprio. |
| R5 | LOW | Ordem de fases + documentar payloads/contas das jornadas para reprodução na demo. |

## Q&A log

**Q1 (2026-06-27):** montar seed dataset considerando fluxos de jornadas agent e cidadao
(agente: postes queimados não resolvidos últimos 30 dias; cidadão: andamento da empresa
+ listar relatos não resolvidos).

**A1:** O gap não é de API (os endpoints existem) e sim de **dados + determinismo** da
seed. Quatro achados travam as jornadas hoje: (A1) resolução só no encaminhamento, não
no relato; (A2) datas só entram via CSV em massa; (A3) o showcase tem só 1 relato de
iluminação nos últimos 30 dias; (A4) encaminhamentos/ciclo são aleatórios, então o
"andamento" do cidadão não é garantido. Recomenda-se: R1 fase determinística de âncoras
(`pendente`, datas fixas na janela de 30d, iluminação + lixo + segurança) inserida APÓS
o amostrador aleatório; R2 fixar o encaminhamento do citizen01 em `solucao_em_andamento`
com comentário de andamento (e opcionalmente um `finalizado` para contraste); R3
explicitar e seedar o mix de estados para "meus relatos não resolvidos"; R4 alinhar o
PROMPT-gerar-seed; R5 documentar ordem de fases e payloads de demo.

**Decisões confirmadas (AskUserQuestion):** entregável = dados + fixtures de jornada;
"não resolvido" = modelo atual (encaminhamento); datas = fixas (demo pontual,
hoje=2026-06-27); foco = iluminação + 1-2 outros eixos.
