# Research 000085 | research/fala-gavea | 2026-06-28 21:28 UTC | Roteiro guiado de prints para as jornadas de usuário (Fala-Gávea)
source: research-080
tags: fala-gavea, journeys, screenshots, demo, ux, report-fase5

## User brief

> me ajude a gerar prints para as jornadas de usuário no fala-gavea.
> [+ texto do relatório final — Fase 5: Novo Fala-Gávea, descrevendo os dois
> segmentos: Cidadão/Morador e Agente Público]

**Decisões confirmadas (AskUserQuestion):**
- Método: **lista guiada** (o usuário tira os prints manualmente).
- Destino: **relatório final (Fase 5) — desktop web** (SPA como implementada).
- Features de IA: **incluir** (Ollama com `qwen3:8b` disponível em localhost:11434).

## Agent interpretation

A plataforma é **fala-gavea** (FastAPI clean-arch + React/Vite SPA), não o
gavealab-poc do design-intent do repo pai. O objetivo é um **roteiro passo-a-passo**
de capturas de tela que ilustrem, no relatório da Fase 5, as duas jornadas para as
quais a equipe já montou seed determinística (research-080 → plan/implement-084,
`seed_journey_anchors.py`, data de demo fixa **2026-06-27**):

1. **Jornada do Agente Público** — loga, monta a worklist de *postes apagados/queimados*
   (`Iluminação pública`) **pendentes nos últimos 30 dias**, explora por IA (chat NL +
   rankeador semântico + assistente de filtros), seleciona relatos na cesta e **cria um
   encaminhamento** institucional.
2. **Jornada do Cidadão/Morador** — `citizen01` registra um relato multimodal, **lista
   seus relatos não resolvidos** e **acompanha o andamento da empresa responsável**
   (status do encaminhamento + comentário de progresso do agente).

## Files

- [fala-gavea/frontend/src/App.tsx](fala-gavea/frontend/src/App.tsx) — rotas: `/`, `/report`, `/encaminhamentos`, `/agent`, `/admin`, `/login`, `/register`
- [fala-gavea/frontend/src/components/layout/Header.tsx](fala-gavea/frontend/src/components/layout/Header.tsx) — nav: Mapa, Novo relato, Meus relatos, Encaminhamentos, Gerenciar encaminhamentos, Ajuda, Cesta, Entrar/Sair
- [fala-gavea/frontend/src/features/workspace/WorkspacePage.tsx](fala-gavea/frontend/src/features/workspace/WorkspacePage.tsx) — workspace: FilterPanel + ViewToggleBar + grade de visões
- [fala-gavea/frontend/src/features/workspace/ViewToggleBar.tsx](fala-gavea/frontend/src/features/workspace/ViewToggleBar.tsx) — visões: Mapa, Tabela, Cesta*, Palavras-chave*, Similares, Chat*(IA) (* = agente/admin)
- [fala-gavea/frontend/src/features/workspace/FilterPanel.tsx](fala-gavea/frontend/src/features/workspace/FilterPanel.tsx) — filtros Tipo/Urgência/Status/Meus relatos/datas + Rankeador semântico + Assistente de filtros (IA)
- [fala-gavea/frontend/src/features/workspace/DateRangePresets.tsx](fala-gavea/frontend/src/features/workspace/DateRangePresets.tsx) — presets de data; **"Últ. 30 dias" é relativo ao relógio do sistema**
- [fala-gavea/frontend/src/features/workspace/views/ChatView.tsx](fala-gavea/frontend/src/features/workspace/views/ChatView.tsx) — chat NL sobre relatos (agente)
- [fala-gavea/frontend/src/features/workspace/views/CestaView.tsx](fala-gavea/frontend/src/features/workspace/views/CestaView.tsx) — cesta → "Criar encaminhamento"
- [fala-gavea/frontend/src/features/forwardings/PublicForwardingsPage.tsx](fala-gavea/frontend/src/features/forwardings/PublicForwardingsPage.tsx) — `/encaminhamentos` + "Meus encaminhamentos"
- [fala-gavea/frontend/src/features/report/ReportFormFields.tsx](fala-gavea/frontend/src/features/report/ReportFormFields.tsx) — formulário: tipo, urgência, descrição, localização, URL da foto
- [fala-gavea/scripts/seed_users.py](fala-gavea/scripts/seed_users.py) — contas de demo
- [fala-gavea/scripts/seed_journey_anchors.py](fala-gavea/scripts/seed_journey_anchors.py) + [data/seed_journey_anchors.csv](fala-gavea/data/seed_journey_anchors.csv) — 20 âncoras (10 iluminação + 5 lixo + 5 segurança), datas 2026-05-29..06-26
- [fala-gavea/scripts/seed_citizen01.py](fala-gavea/scripts/seed_citizen01.py) — 10 relatos do cidadão + encaminhamento A (em andamento + comentário) + B (finalizado)

---

## Contexto técnico (o que printar e por quê)

**Contas de demo** (de `seed_users.py`):

| Papel | Login | Senha |
|---|---|---|
| Cidadão | `citizen01@gavea.br` | `citizen01pass` |
| Agente público | `agente@gavea.br` | `agente12345` |
| Admin | `admin@gavea.br` | `admin12345!` |

**Pré-requisitos para os prints (uma vez):**

```bash
# 1. Ollama rodando com o modelo (para as features de IA)
ollama serve            # se ainda não estiver no ar
ollama pull qwen3:8b

# 2. Backend (terminal 1) — JWT_SECRET_KEY + bootstrap admin obrigatórios
cd fala-gavea
uv run uvicorn fala_gavea.presentation.api.main:app --reload
#   garanta no .env: JWT_SECRET_KEY, FALA_GAVEA_ADMIN_EMAIL=admin@gavea.br,
#   FALA_GAVEA_ADMIN_PASSWORD=admin12345!, FALA_GAVEA_OLLAMA_URL/MODEL

# 3. Seed completo (terminal 2) — popula tudo, âncoras por último
make seed URL=http://localhost:8000
#   (equivale a uv run python scripts/seed_all.py --profile showcase)

# 4. Frontend (terminal 3)
cd frontend && npm run dev      # SPA em http://localhost:5173 (proxy → :8000)
```

> **Use http://localhost:5173 (Vite) para os prints** — hot-reload e a SPA completa.
> Os endpoints `/auth`, `/reports`, `/forwardings`, `/nl` são proxiados para :8000.

### ⚠️ Caveat crítico de reprodutibilidade (worklist do agente)

A seed de âncoras é datada **2026-05-29 … 2026-06-26** (janela de 30 dias antes da
data de demo fixa **2026-06-27**). Mas o preset **"Últ. 30 dias" do FilterPanel é
calculado a partir do relógio do sistema** ([DateRangePresets.tsx:28-32](fala-gavea/frontend/src/features/workspace/DateRangePresets.tsx#L28-L32)).
Hoje (2026-06-28) ainda pega ~19 das 20 âncoras — **funciona**. Mas se você printar
com a data do sistema muito depois de ~2026-07-26, a janela desliza e a worklist
**esvazia**. Mitigações, em ordem de preferência:

1. Tirar os prints com a data do sistema próxima de **2026-06-27/28** (ideal).
2. Em vez do preset, usar **datas personalizadas** no FilterPanel: De `28/05/2026`
   Até `27/06/2026` (sempre pega todas as âncoras, independente do relógio).
3. Re-seedar deslocando as datas do CSV (ver `seeds/relatos/SCHEMA.md`).

---

## ROTEIRO DE PRINTS

> Convenção: cada print tem um **ID** (sugestão de nome de arquivo), o **passo**, e
> **"o que deve aparecer"** (o que a seed garante na tela). Resolução sugerida:
> janela do browser ~**1440×900**, zoom 100%, tema claro. Esconda a barra de
> favoritos para um enquadramento limpo.

### Jornada A — Agente Público (loop de curadoria → encaminhamento)

**Narrativa:** *o agente entra, isola os postes apagados não resolvidos dos últimos
30 dias, usa a IA para entender o padrão territorial, monta a cesta e encaminha ao
órgão responsável.*

| # | Print (arquivo sugerido) | Passo | O que deve aparecer |
|---|---|---|---|
| A1 | `A1-login-agente.png` | Acesse `/login`, faça login como `agente@gavea.br` | Tela de login preenchida (oculte a senha se preferir) |
| A2 | `A2-workspace-agente.png` | Após login, vá em **Mapa** (`/`) | Workspace do agente: painel de filtros à esquerda, barra de visões (Mapa, Tabela, **Cesta**, **Palavras-chave**, Similares, **Chat ✨**), mapa da Gávea com vários pins |
| A3 | `A3-filtro-iluminacao-30d.png` | No FilterPanel: **Tipo = Iluminação pública**, **Status = Pendente**, datas **Últ. 30 dias** (ou personalizadas 28/05→27/06) → **Aplicar** | Chips ativos ("Status: Pendente", "De/Até"), contador "≈10 relatos", mapa/tabela só com postes apagados recentes |
| A4 | `A4-tabela-worklist.png` | Ative a visão **Tabela** | Lista das âncoras de iluminação (ex.: *"Três postes consecutivos apagados na Rua Professor Saboia Ribeiro…"*, *"Poste queimado há mais de duas semanas… Rua Marquês de São Vicente…"*), com urgência/data — a worklist concreta |
| A5 | `A5-palavras-chave.png` | Ative **Palavras-chave** (TF-IDF) | Termos extraídos do subconjunto filtrado ("poste", "apagado", "escuro", "lâmpada"…) — evidência do padrão territorial sem ler tudo |
| A6 | `A6-chat-ia.png` | Ative **Chat ✨** e pergunte: *"Qual o padrão dos relatos de iluminação na Gávea nos últimos 30 dias?"* | Resposta do assistente (Ollama) + chips de relatos citados (`#xxxxxxxx`) — **prova da IA**. (Aguarde a resposta antes de capturar) |
| A7 | `A7-rankeador-semantico.png` | No FilterPanel, campo **Rankeador semântico**: *"rua escura e perigosa à noite"* → Aplicar | Relatos reordenados por similaridade semântica (mostre o tooltip ⓘ se quiser explicar) |
| A8 | `A8-selecao-cesta.png` | Na Tabela/Mapa, selecione ~3-4 relatos de iluminação (vão para a Cesta; contador no header) | Itens marcados; badge "Cesta (N)" no topo |
| A9 | `A9-cesta-similares.png` | Abra a visão **Cesta** | Relatos da cesta + painel **"Relatos similares abertos"** (IA sugere pendentes parecidos fora da cesta, com score) |
| A10 | `A10-criar-encaminhamento.png` | Clique **"Criar encaminhamento (N)"** | Dialog de criação: campo Órgão/instituição + solução proposta + lista de relatos vinculados |
| A11 | `A11-encaminhamento-criado.png` | Preencha (ex.: Órgão **RioLuz**, solução "Substituição das lâmpadas…") e confirme | Toast de sucesso / encaminhamento criado |
| A12 | `A12-gerenciar-encaminhamentos.png` | Vá em **Gerenciar encaminhamentos** (`/agent`) | Lista de encaminhamentos do agente, incluindo o recém-criado + os da seed (CET-Rio/RioLuz em andamento; RioLuz finalizado), com seletor de status |

### Jornada B — Cidadão/Morador (registro → transparência → acompanhamento)

**Narrativa:** *o cidadão registra um problema na rua dele de forma simples, vê seus
relatos não resolvidos e acompanha o que a empresa responsável já fez.*

| # | Print (arquivo sugerido) | Passo | O que deve aparecer |
|---|---|---|---|
| B1 | `B1-login-cidadao.png` | Faça login como `citizen01@gavea.br` (ou mostre `/register` para "cadastro simples") | Tela de login/registro do cidadão |
| B2 | `B2-novo-relato.png` | Vá em **Novo relato** (`/report`) | Formulário multimodal: **Tipo de problema**, **Urgência** (Alta/Média/Baixa com cor), **Descrição**, **Localização** ("Usar minha localização" + lat/lon), **URL da foto** — registro texto+foto+geo |
| B3 | `B3-relato-preenchido.png` | Preencha um relato novo (ex.: "Poste apagado na minha rua…", urgência Alta, clique "Usar minha localização") | Formulário preenchido com coordenadas resolvidas; botão de enviar |
| B4 | `B4-relato-enviado.png` | Envie | Confirmação/toast de relato registrado (protocolo/feedback de sucesso) |
| B5 | `B5-meus-relatos.png` | Clique em **Meus relatos** (`/?meus_relatos=1`) | Workspace filtrado por autor = citizen01: os 10 relatos da seed + o novo (mapa/tabela). Chip "Meus relatos" ativo |
| B6 | `B6-meus-relatos-pendentes.png` | Adicione **Status = Pendente** e Aplicar | Subconjunto não resolvido ("listar meus relatos não resolvidos" do brief) |
| B7 | `B7-encaminhamentos-meus.png` | Vá em **Encaminhamentos** (`/encaminhamentos`) e marque **"Meus encaminhamentos"** | Tabela (Órgão / Relatos / Status / Data): **CET-Rio / RioLuz — Em andamento** e **RioLuz — Finalizado** |
| B8 | `B8-andamento-empresa.png` | Expanda o encaminhamento **CET-Rio / RioLuz (Em andamento)** | A solução proposta + **comentário do agente**: *"Equipe RioLuz esteve em campo em 24/06; vistoria concluída, troca das lâmpadas programada…"* — **o "andamento da empresa responsável"** |
| B9 | `B9-encaminhamento-finalizado.png` | Expanda o encaminhamento **RioLuz (Finalizado)** | Comentário de conclusão: *"Serviço concluído: lâmpadas substituídas e rede testada em campo…"* — contraste resolvido vs. não resolvido |
| B10 | `B10-ajuda-ia.png` (opcional) | No header, clique **Ajuda** e pergunte *"Como acompanho meu relato?"* | Dialog "Ajuda da plataforma ✨" com resposta do assistente RAG sobre a própria plataforma (2ª feature de IA, voltada ao cidadão) |

### Capa/contexto (opcional, mas útil no relatório)

| # | Print | Passo | Uso |
|---|---|---|---|
| C1 | `C0-mapa-publico.png` | Deslogado, abra `/` (Mapa público) | Mapa colaborativo da Gávea com clusterização — abre a seção "canal comunitário" |
| C2 | `C0-encaminhamentos-publico.png` | Deslogado, `/encaminhamentos` | Transparência pública dos encaminhamentos — fecha o loop de feedback |

---

## Recomendações

| # | Prioridade | Recomendação |
|---|---|---|
| R1 | HIGH | Antes de printar, **fixar a janela temporal** da worklist do agente: usar datas personalizadas (28/05→27/06/2026) em vez do preset "Últ. 30 dias", OU printar com o relógio do sistema próximo de 2026-06-27. Caso contrário a Jornada A pode aparecer vazia. |
| R2 | HIGH | Rodar o **seed completo + confirmar Ollama no ar** antes da sessão de prints. As features de IA (A6 chat, A7 rankeador, A9 similares, B10 ajuda) dependem do modelo respondendo; capture só **após** a resposta carregar. |
| R3 | MEDIUM | Printar em **localhost:5173 (Vite)**, janela ~1440×900, zoom 100%, tema claro, sem barra de favoritos — consistência visual no relatório. Nomear os arquivos pelo ID do roteiro (A1…B10) para casar 1:1 com a narrativa das jornadas. |
| R4 | MEDIUM | Mapear cada print às **dores/ganhos** do relatório Fase 5: registro multimodal → B2/B3; validação coletiva/transparência → B7-B9 + C2; padrões territoriais/ferramentas visuais → A4/A5; busca em linguagem natural → A6/A7; encaminhamento rastreável → A10-A12. |
| R5 | LOW | Se quiser **reprodutibilidade total** depois (re-tirar prints sem cliques manuais), considerar um script Playwright dirigindo exatamente este roteiro — fora do escopo atual (você optou por lista guiada), mas o roteiro acima já é o storyboard pronto para automatizar. |
| R6 | LOW | Anomalia de harness observada: `reserve_id.py` entregou o ID global **84**, já usado por `plan-000084` (colisão). Usei **085** para esta pesquisa. Vale verificar o contador de IDs (`_output`) antes da próxima reserva. |

## Q&A log

**Q1 (2026-06-28):** me ajude a gerar prints para as jornadas de usuário no fala-gavea
(relatório Fase 5; segmentos Cidadão/Morador e Agente Público).

**A1:** As duas jornadas já têm seed determinística (research-080/plan-084). Entreguei
um **roteiro guiado de 12 prints (Agente) + 10 prints (Cidadão) + 2 de contexto**,
ancorado nas rotas, contas e labels reais da SPA e nos dados que a seed garante em tela.
Decisões do usuário: lista guiada (print manual), destino relatório Fase 5 desktop web,
incluir features de IA (Ollama disponível). Caveat crítico: o preset "Últ. 30 dias" é
relativo ao relógio — usar datas personalizadas 28/05→27/06/2026 para garantir a
worklist do agente. Pré-requisitos: backend + seed completo + Ollama + frontend Vite.

## Recommendations summary

1. **(HIGH)** Fixar janela temporal da worklist (datas personalizadas 28/05→27/06) antes de printar a Jornada A.
2. **(HIGH)** Seed completo + Ollama no ar; capturar features de IA só após a resposta carregar.
3. **(MEDIUM)** Printar em localhost:5173, 1440×900, tema claro; nomear arquivos pelos IDs do roteiro.
4. **(MEDIUM)** Mapear cada print às dores/ganhos do relatório Fase 5.
5. **(LOW)** Roteiro serve de storyboard para futura automação Playwright.
6. **(LOW)** Corrigir/verificar o contador global de IDs (colisão 84).
