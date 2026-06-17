# Roadmap 000070 | 2026-06-17 11:35 UTC | canal-digital-comunitario-seguranca-urbana

source: reflection-000069 -- feedback loop ausente na categorizacao por IA revelou lacuna estrutural que este roadmap fecha

## Source
- _output/reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md (read)
- fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py (read)
- fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/auto_categorize_report.py (read)
- fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/prompts.py (ref)
- fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/main.py (read)
- product-design/project/product-design-as-coded.md (read)
- product-design/project/product-design-as-intended.md (read)
- _output/roadmaps/roadmap-000056-filtros-mapa-tags-ai-category.md (read)

## Brief (verbatim)

Canal Digital Comunitario para Seguranca Urbana (Waze comunitario)
Desafio: Como aumentar a sensacao de seguranca no bairro por meio da ocupacao positiva do espaco publico?

Aplicativo ou canal digital para moradores, estudantes, trabalhadores e frequentadores da Gavea registrarem, comunicarem e acompanharem problemas urbanos que afetam a sensacao de seguranca -- iluminacao precaria, mobilidade, conservacao inadequada, pontos de risco e circulacao insegura.

Permite reportar situacoes organizadas por tipo de problema, localizacao e nivel de urgencia, facilitando a visualizacao das demandas e o encaminhamento para parceiros, instituicoes e orgaos publicos. Tambem acompanha respostas e divulga melhorias realizadas.

Transforma a percepcao individual de inseguranca em informacao coletiva e acionavel. Cria base compartilhada de demandas, fortalece corresponsabilidade entre populacao, instituicoes e poder publico, e estimula a ocupacao positiva do espaco publico.

O app funciona como um pipeline de categorizacao e encaminhamento de demandas. A IA atual como um colaborador na categorizacao dos relatos, clusterizacao (para categorizar e identificar relatos semelhantes). o app fornece um painel e dashboard com ferramentas para o humano ensinar a IA a categorizar as demandas. o humano pode escolher filtrar quais demandas quer trabalhar (filtro espacial, e filtros convencionais que sao originais do dado)

## Context

### O que ja existe (nao precisa ser construido)

| Componente | Status | Onde |
|---|---|---|
| `SecurityReport` com `category`, `ai_suggested_category`, `tags`, `status` | done | domain/entities/security_report.py |
| `POST /security_reports/{id}/auto_categorize` | done | routers/security_reports.py |
| `PATCH /security_reports/{id}/category` | done | routers/security_reports.py -- confirma/corrige e zera ai_suggested |
| Filtro temporal (`since`/`until`), espacial (bbox), por tag | done | backend + frontend |
| Busca semantica ChromaDB (`GET /search`) | done | vector_store/chroma_client.py |
| Chat NL intent-to-filter (plan-000068) | done | use_cases/send_chat_message.py |
| Mapa Leaflet + Alpine.js popup de curadoria | done | static/app.js + index.html |
| OllamaClient + CATEGORIZE_PROMPT (9 categorias) | done | infrastructure/llm/ + infrastructure/ai/prompts.py |
| Dados sementados (250 relatos fake da Gavea) | done | scripts/seed_reports.py |

### Lacuna identificada na reflection-000069

O par `(ai_suggested_category, category_confirmada_pelo_delegado)` ja existe no banco SQLite
mas nenhum codigo o captura como sinal de treino. Quando o delegado confirma ou corrige a
sugestao da IA via `PATCH /category`, o campo `ai_suggested_category` e zerado -- a informacao
de curadoria desaparece sem deixar rastro auditavel.

Consequencias:
- A IA nao aprende com as correcoes do delegado
- Nao e possivel medir a acuracia atual do modelo
- O prompt de categorizacao usa zero exemplos curados (zero-shot apenas)
- O projeto nao tem dataset de avaliacao para comparar modelos futuros

Este roadmap fecha essa lacuna em Wave 0 antes de qualquer feature nova.

### Decisoes de arquitetura

**D-A: Feedback loop como tabela de auditoria, nao campo no relato**
`CategoryCurationEvent` e uma tabela de log append-only (nunca update, nunca delete).
Cada curadoria cria uma linha nova. Isso permite historico completo e analise de drift.

**D-B: Few-shot injection no prompt, nao fine-tuning**
Usar os N pares curados mais recentes como exemplos no CATEGORIZE_PROMPT (few-shot).
Fine-tuning requer infraestrutura de treino que esta fora do escopo deste semestre.
O threshold para considerar few-shot util e >= 10 pares por categoria.

**D-C: Clustering de relatos via embeddings existentes no ChromaDB**
Os embeddings dos relatos ja estao no ChromaDB (indexados em criacao). Reutilizar via
`chromadb.get_collection().get(include=["embeddings"])` + UMAP + HDBSCAN. Sem re-embedding.

**D-D: Urgencia como campo manual (sem sugestao IA neste roadmap)**
`urgency: alta|media|baixa` e preenchido pelo cidadao no momento do relato.
Sugestao automatica de urgencia e future work (apos feedback loop estabilizado).

**D-E: Encaminhamento como campo simples, nao entidade separada**
`routed_to: str | None` e `routing_status: RoutingStatus | None` direto em `SecurityReport`.
Entidade `DemandRouting` separada (com historico) e future work para versao institucional.

---

## Wave Summary

### Wave 0 -- Feedback Loop: Captura de Curadoria (sequential)

> **Bloqueia Wave 1 e Wave 3.** Deve ser executado primeiro. O dataset de curadoria
> e pre-requisito para few-shot (Wave 1) e para as metricas do dashboard (Wave 3).

| # | ID | Title | Scope | Type | Plan | Status |
|---|-----|-------|-------|------|------|--------|
| 1 | curation-log | CategoryCurationEvent: tabela de log + registro no PATCH /category | backend | technical | plan-TBD | pending |
| 2 | few-shot | Few-shot injection: pares curados no CATEGORIZE_PROMPT | backend | technical | plan-TBD | pending |

**Item 1 -- CategoryCurationEvent:**

Novo modelo SQLAlchemy `CategoryCurationEventModel`:
```python
class CategoryCurationEventModel(Base):
    __tablename__ = "category_curation_events"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    report_id    = Column(String, ForeignKey("security_reports.id"), nullable=False)
    ai_suggested = Column(SAEnum(ReportCategory), nullable=True)   # valor antes da correcao
    human_choice = Column(SAEnum(ReportCategory), nullable=False)  # valor confirmado pelo delegado
    was_correction = Column(Boolean, nullable=False)               # True se human != ai_suggested
    curator_id   = Column(String, nullable=True)                   # author_id do curador (futuro auth)
    created_at   = Column(DateTime, nullable=False, default=datetime.utcnow)
```

Modificar `SetReportCategory.execute()`: antes de chamar `update_category`, ler o relato atual
para capturar `ai_suggested_category`; criar `CategoryCurationEvent` via novo repositorio
`CategoryCurationEventRepository.save(event)`.

Novos endpoints:
- `GET /curation_events?limit=100&offset=0` -- lista paginada com filtros `was_correction=true/false`
- `GET /curation_events/export` -- retorna JSONL (`{"ai_suggested":..,"human_choice":..,"text":..}`)
  para uso como dataset de avaliacao ou few-shot offline

Testes unitarios: `SetReportCategory` gera evento; `was_correction` e `True` quando categorias diferem.
Testes de integracao: `PATCH /category` gera curation_event; `GET /curation_events/export` retorna JSONL.

**Item 2 -- Few-shot injection:**

Modificar `AutoCategorizeReport.execute()`:
1. Antes de montar o prompt, chamar `CurationEventRepository.get_recent_examples(n=5)` que retorna
   pares `(text_excerpt, ai_suggested, human_choice)` onde `was_correction = True` (casos de correcao
   sao mais informativos que confirmacoes).
2. Se `len(examples) >= 3`, injetar bloco de exemplos no CATEGORIZE_PROMPT:

```
### Exemplos de correcoes anteriores:
Relato: "<text_excerpt>"  -> IA sugeriu: furto_roubo  -> Delegado corrigiu para: vandalismo
Relato: "<text_excerpt>"  -> IA sugeriu: transito     -> Delegado corrigiu para: iluminacao
...
```

3. Se `len(examples) < 3`, usar prompt original (zero-shot) sem degradar comportamento atual.

Adicionar campo `few_shot_count: int` na `AutoCategorizeResponse` para auditoria.

Testes: mock de `get_recent_examples` com 0, 3, e 5 exemplos; verificar que prompt e montado
corretamente e que `few_shot_count` reflete o numero de exemplos injetados.

---

### Wave 1 -- Urgencia e Encaminhamento (parallel, depends on Wave 0 Item 1)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 3 | urgency | Campo urgency (alta/media/baixa) no relato + filtro + frontend | cross | technical | plan-TBD | curation-log | pending |
| 4 | routing | Campo routed_to + routing_status + endpoint de encaminhamento | backend | technical | plan-TBD | curation-log | pending |

**Item 3 -- Urgencia:**

Domain:
- Novo enum `ReportUrgency(str, Enum): ALTA="alta", MEDIA="media", BAIXA="baixa"`
- Campo `urgency: ReportUrgency = ReportUrgency.MEDIA` em `SecurityReport` (default media)
- `SecurityReport.create()` recebe `urgency: ReportUrgency = ReportUrgency.MEDIA`

DB:
- Nova coluna `urgency = Column(SAEnum(ReportUrgency), nullable=False, default="media")`
- Como o projeto usa `create_all()` sem Alembic: deletar `app.db` e reiniciar no dev

API:
- `SecurityReportCreate` recebe campo `urgency: str = "media"` (validado contra enum)
- `SecurityReportResponse` passa a incluir `urgency: str`
- Filtro `?urgency=alta` no `GET /geojson` e `GET /`
- `ReportFilter` recebe `urgency: ReportUrgency | None`

Frontend (`static/app.js` + `static/index.html`):
- Campo `<select id="f-urgency">` no formulario de novo relato (alta/media/baixa)
- Filtro `<select id="filter-urgency">` na sidebar
- Icone de urgencia no marker: alta=vermelho, media=laranja, baixa=azul (substituir cor plana atual)
- `URGENCY_COLORS` e `URGENCY_LABELS` como constantes em `app.js`
- `buildQueryString()` inclui `urgency=<valor>` quando selecionado
- GeoJSON feature passa `urgency` nas propriedades; popup exibe badge colorido

Testes: filtro por urgency retorna apenas relatos do nivel correto.

**Item 4 -- Encaminhamento:**

Domain:
- Novo enum `RoutingStatus(str, Enum): PENDENTE="pendente", ENCAMINHADO="encaminhado", EM_ATENDIMENTO="em_atendimento", RESOLVIDO="resolvido", ARQUIVADO="arquivado"`
- Campos em `SecurityReport`: `routed_to: str | None = None`, `routing_status: RoutingStatus | None = None`, `routed_at: datetime | None = None`

DB:
- Colunas: `routed_to VARCHAR nullable`, `routing_status SAEnum(RoutingStatus) nullable`, `routed_at DATETIME nullable`

API:
- `POST /security_reports/{id}/route` -- body `{"routed_to": "9a Delegacia de Policia", "routing_status": "encaminhado"}`
  retorna `SecurityReportResponse`; 404 se ausente
- `PATCH /security_reports/{id}/routing_status` -- body `{"routing_status": "resolvido"}`
  para atualizacoes posteriores ao encaminhamento inicial
- `SecurityReportResponse` passa a incluir `routed_to`, `routing_status`, `routed_at`
- Filtro `?routing_status=encaminhado` no listing endpoint

Use cases: `RouteReport(RouteReportInput(id, routed_to, routing_status))`, `UpdateRoutingStatus`.

Testes unitarios: `RouteReport` salva `routed_to` e seta `routed_at = now()`; `UpdateRoutingStatus` rejeita
relato nao encaminhado com `InvalidInputError`.

---

### Wave 2 -- Cluster Semantico no Mapa (sequential, depends on Wave 0)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 5 | cluster-backend | UMAP + HDBSCAN sobre embeddings do ChromaDB + endpoint /cluster | backend | technical | plan-TBD | curation-log | pending |
| 6 | cluster-frontend | Layer de clusters no mapa Leaflet (cores, painel lateral) | frontend | technical | plan-TBD | cluster-backend | pending |

**Item 5 -- Cluster backend:**

Novo modulo `infrastructure/clustering/report_cluster.py`:
- `compute_report_clusters(vectorstore_dir, n_neighbors=15, min_cluster_size=5) -> list[ReportCluster]`
- Acessa a colecao ChromaDB existente (`fala-gavea-seguranca-reports`); chama `.get(include=["embeddings","ids"])`.
- UMAP 2D (cosine, random_state=42, n_neighbors=min(n_neighbors, len-1)); HDBSCAN clustering.
- Retorna `ReportCluster(cluster_id: int, report_ids: list[str], label: str, centroid_x: float, centroid_y: float)`.
- `label` = categoria predominante entre os relatos do cluster (moda de `category`).

Novo endpoint:
- `GET /security_reports/clusters` -- calcula clusters on-the-fly (ou retorna cache em `st.session_state`
  equivalente: LRU cache de 10 minutos via `functools.lru_cache` com TTL manual).
  Response: `{"clusters": [{"cluster_id": 0, "label": "iluminacao", "report_ids": [...], "size": 12}]}`

Novo campo em `SecurityReportModel` (opcional, nao persiste automaticamente):
- O cluster e calculado dinamicamente -- nao armazenado no DB. O GeoJSON endpoint aceita
  `?with_clusters=true` e retorna `cluster_id` como propriedade de cada feature (calcula na requisicao).

Testes: mock ChromaDB; `compute_report_clusters` retorna pelo menos 1 cluster para 10 relatos fake.

**Item 6 -- Cluster frontend:**

`static/app.js`:
- Novo `clusterLayerGroup = L.layerGroup()` separado dos markers normais.
- Checkbox `#toggle-clusters` "Mostrar clusters semanticos" na sidebar.
- Quando ativado: `GET /security_reports/geojson?with_clusters=true` e colorir markers por `cluster_id`
  usando paleta de 10 cores fixas (`CLUSTER_COLORS[]`). Quando desativado: voltar ao esquema por urgencia.
- Painel lateral colapsavel `#cluster-panel`: lista clusters com nome (`label`), contagem, e botao
  "Filtrar por este cluster" (aplica `cluster_id` como filtro -- nao e um filtro de backend,
  e client-side: filtra os markers carregados).

`static/index.html`: checkbox + painel de clusters na sidebar abaixo dos filtros existentes.

---

### Wave 3 -- Dashboard de Curadoria (frontend, depends on Wave 0 + Wave 2)

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 7 | curation-dashboard | Pagina /dashboard.html: metricas IA, tabela pendentes, exportar | frontend | design+technical | plan-TBD | few-shot + cluster-backend | pending |
| 8 | routing-panel | Painel de encaminhamento no dashboard: filtro por status, bulk update | frontend | technical | plan-TBD | routing + curation-dashboard | pending |

**Item 7 -- Dashboard de curadoria:**

Nova pagina estatica `static/dashboard.html` + secao em `app.js` (ou `dashboard.js` separado).

Secoes:
1. **Metricas de acuracia** (cards no topo):
   - Total de relatos com sugestao IA: `GET /curation_events?limit=1000` count
   - Taxa de acerto: `(total - was_correction) / total * 100`%
   - Distribuicao por categoria: mini-barchart (categorias x % de correcao)
   - `few_shot_count` medio das ultimas 24h (da AutoCategorizeResponse -- se logado)

2. **Tabela de pendentes** (relatos com `ai_suggested_category != null`):
   - `GET /security_reports?ai_suggested_only=true&limit=50` (novo filtro backend)
   - Colunas: texto (truncado 80 chars), IA sugeriu, Confirmar (botao verde), Corrigir (dropdown)
   - Confirmar chama `PATCH /{id}/category` com o valor sugerido
   - Corrigir mostra `<select>` inline com as 9 categorias, entao `PATCH /{id}/category`
   - Bulk: checkbox "selecionar todos" + botao "Confirmar selecionados"

3. **Exportar dataset**:
   - Botao "Baixar pares curados (.jsonl)" chama `GET /curation_events/export`
   - Exibe contagem: "N pares disponiveis para exportacao"

Novo filtro backend: `?ai_suggested_only=true` em `GET /security_reports` -- retorna apenas relatos
onde `ai_suggested_category IS NOT NULL`. Adicionado a `ReportFilter` e ao repo SQLAlchemy.

**Item 8 -- Painel de encaminhamento:**

Segunda secao do `dashboard.html`:

1. **Metricas de encaminhamento** (cards):
   - Total por `routing_status`
   - % resolvidos nos ultimos 30 dias

2. **Tabela de relatos encaminhados** (`GET /security_reports?routing_status=encaminhado`):
   - Colunas: categoria, urgencia, encaminhado_para, data, status, acoes (atualizar status)
   - Dropdown inline para mudar routing_status (`PATCH /{id}/routing_status`)
   - Filtro por categoria, urgencia, routing_status na sidebar do dashboard

Link `/dashboard` acessivel a partir do mapa principal (botao "Painel de Curadoria" no header).

---

## Execution Instructions

### Wave 0 (sequential) -- executar primeiro, nao tem dependencias externas
Execute um de cada vez:
```
/implement plan-TBD  # curation-log: CategoryCurationEvent + registro no PATCH /category
/implement plan-TBD  # few-shot: injecao de exemplos curados no CATEGORIZE_PROMPT
```

### Wave 1 (parallel -- 2 plans) -- depende de Wave 0 Item 1 (curation-log)
Ambos podem rodar em paralelo apos `curation-log` estar done:
```
# Sessao A:
/implement plan-TBD  # urgency: campo urgencia no relato + filtro + frontend

# Sessao B (paralela):
/implement plan-TBD  # routing: campo routed_to + routing_status + endpoints
```

### Wave 2 (sequential -- 2 plans) -- depende de Wave 0
Execute em ordem:
```
/implement plan-TBD  # cluster-backend: UMAP + HDBSCAN + endpoint /clusters
/implement plan-TBD  # cluster-frontend: layer de clusters no mapa Leaflet
```

### Wave 3 (sequential -- 2 plans) -- depende de Wave 0 (Item 2) + Wave 2
Execute em ordem:
```
/implement plan-TBD  # curation-dashboard: /dashboard.html metricas + tabela pendentes + exportar
/implement plan-TBD  # routing-panel: secao de encaminhamento no dashboard
```

---

## Notes para os planos individuais

- **DB sem Alembic**: o projeto usa `Base.metadata.create_all()` no startup. Novas tabelas e colunas
  aparecem automaticamente em bancos novos. Para bancos existentes de dev: deletar `app.db` e reiniciar.
  O seed script (`seed_reports.py`) deve ser re-executado apos reinicio.

- **ChromaDB collection name**: verificar o nome exato da colecao em `infrastructure/vector_store/chroma_client.py`
  antes de implementar o cluster-backend. O codigo atual usa a colecao de busca semantica.

- **Few-shot threshold**: Item 2 deve verificar `len(examples) >= 3` antes de injetar. Com 0-2 exemplos,
  usar prompt zero-shot original. Isso garante que o comportamento atual nao regride com dataset vazio.

- **Urgency default**: `MEDIA` foi escolhido como default para nao alarmar cidadaos que nao classificam
  manualmente. O seed script pode ser atualizado para distribuir urgencias (40% baixa, 45% media, 15% alta).

- **Routing destinos sugeridos** (para o frontend): 9a Delegacia, COMLURB, RioLuz, CET-Rio,
  Secretaria de Ordem Publica, SMO, Defesa Civil. Expor como lista hardcoded no frontend ate que
  uma API de instituicoes seja construida.

- **Cluster cache**: o endpoint `/clusters` e computacionalmente pesado (UMAP). Usar `lru_cache` com
  TTL de 10 minutos (contador manual `_cluster_cache_time`). Invalidar quando novo relato e criado
  (ou aceitar stale por 10 min -- aceitavel para PoC).

- **Testes de integracao**: cada plano de backend deve incluir testes para os novos endpoints.
  O projeto ja tem `tests/integration/api/` -- seguir o padrao existente.

- **Link do dashboard**: adicionar `<a href="/dashboard">Painel de Curadoria</a>` no header do
  `index.html` como link direto. O item 7 serve `dashboard.html` via `StaticFiles`.
