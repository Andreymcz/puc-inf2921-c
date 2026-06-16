# Research 000066 | FEATURE-F | 2026-06-16 16:35 UTC | Busca inteligente com IA — chat NL intent to API + frontend state

tags: nl-to-filters, intent-extraction, agentic-ui, architecture, ux

## User Brief

"busca inteligente com IA. quero usar um chat inteligente para definir minhas intenções e como quero filtrar/visualizar os dados. O chat deve converter as intenções do usuario em chamadas de api + mudança do estado do front end para a visualização da intenção do usuário."

## Agent Interpretation

O usuário quer adicionar ao `fala-gavea-seguranca` um painel de chat natural onde o delegado/analista digita uma intenção em linguagem natural (ex: "mostra relatos de furto da semana passada") e o sistema:
1. Extrai os filtros implícitos (categoria, status, janela temporal, tag, bbox)
2. Chama a API de relatórios com esses filtros
3. Atualiza o estado do mapa (marcadores filtrados) sem intervenção manual nos controles

## Files Analisados

- `fala-gavea-seguranca/static/app.js` — frontend Leaflet + filtros manuais (category/status)
- `fala-gavea-seguranca/src/.../presentation/api/routers/security_reports.py` — `GET /security_reports/geojson?category=&status=&since=&until=&tag=&lat_*=`
- `fala-gavea-seguranca/src/.../application/use_cases/send_chat_message.py` — chat RAG existente (texto apenas)
- `fala-gavea-seguranca/src/.../presentation/api/routers/chats.py` — endpoints de chat
- `fala-gavea-seguranca/src/.../domain/entities/security_report.py` — ReportCategory enum (9 valores)

---

## Q&A Log

**Q1: Qual é a melhor arquitetura para NL intent → chamada de API + mudança de estado frontend neste stack (vanilla JS + FastAPI + Ollama qwen3:8b)?**

### Candidatos avaliados

| | Arquitetura | Descrição |
|---|---|---|
| A | Action envelope | Endpoint de chat retorna `{message, action}` — LLM gera texto + filtros estruturados; frontend aplica |
| B | Intent endpoint separado | `POST /intents/parse` retorna apenas filtros; frontend decide se aplica (confirm step) |
| C | Client-side tool call | LLM retorna texto com tool call embutido (ex: `<tool_call>…</tool_call>`); frontend parseia |
| D | SSE streaming + action events | Tokens streamados + evento final com a ação |

---

### Análise por perspectiva

#### ARCH — Arquitetura

A alternativa A (action envelope) é a que melhor encaixa no padrão existente:
- O endpoint `POST /chats/{id}/messages` já existe e retorna uma resposta de texto
- Adicionar `action: null | ActionEnvelope` é aditivo e backward-compatible
- O campo `action` percorre a mesma cadeia limpa: use case de aplicação parseia o JSON do LLM → domínio valida os filtros → infraestrutura executa
- **Risco principal**: sem uma camada de validação explícita no application layer, JSON malformado do LLM chega ao frontend

A arquitetura C inverte a responsabilidade: o frontend passa a ser o trust boundary — incorreto para clean architecture.

A arquitetura D (SSE) tem custo de complexidade desproporcional ao benefício nesta fase; a resposta de extração de filtros é curta.

#### SEC — Segurança

O `action.payload` gerado pelo LLM é uma superfície de injeção de estado no frontend, mesmo usando modelo local:
- O usuário controla a entrada; o modelo pode ser induzido a gerar keys inesperadas no JSON
- O frontend **não deve** aplicar diretamente valores arbitrários do payload ao DOM
- Mitigação: **allowlisting server-side** — o application layer valida cada campo contra os enums e formatos conhecidos antes de retornar o action; se inválido, retorna `action: null`

#### UX — Experiência do usuário

Atualização silenciosa do mapa cria duas quebras de comunicabilidade:
- **IIa2 "O que aconteceu?"** — sem vínculo visual entre digitar no chat e os marcadores mudarem
- **Ib "Está bem assim."** — se o LLM errou a categoria, o analista pode não perceber

Solução: **chip de confirmação** inline acima do mapa mostrando os filtros extraídos ("Categoria: furto_roubo | Desde: 09/06/2026 | [Aplicar] [Descartar]") — aplica automaticamente apenas para consultas simples e sem ambiguidade; exige confirmação para queries multi-filtro ou com datas relativas.

#### API — Contrato de resposta

O schema de resposta deve ser uma **discriminated union nullable** desde o início:
```json
{
  "message": "Mostrando relatos de furto da última semana...",
  "action": {
    "type": "apply_filters",
    "payload": {
      "category": "furto_roubo",
      "status": null,
      "since": "2026-06-09T00:00:00Z",
      "until": null,
      "tag": null
    }
  }
}
```
Ou `"action": null` quando nenhum filtro foi identificado. Definir o type discriminator desde agora permite adicionar `zoom_map`, `highlight_cluster` etc. sem quebrar o frontend.

#### TEST — Testabilidade

O LLM produz saídas não-determinísticas. Estratégia em dois níveis:
1. **Testes unitários** (CI-safe): injetar `MockIntentParser` que retorna payloads fixos → cobrir (a) query válida, (b) JSON malformado → `action: null`, (c) enum inválido → `action: null`, (d) datas relativas
2. **Golden-set de integração** (local, `make test-llm`): 8-10 queries fixas em pt-BR com filtros esperados, rodando contra o Ollama real; não gateado no CI

---

### Prompt Engineering para extração de filtros

Com qwen3:8b (Ollama), usar JSON mode ou prompt com instrução explícita de formato. Exemplo de system prompt:

```
Você é um assistente de análise de segurança pública da Gávea.
Quando o usuário descrever o que quer ver no mapa, extraia os filtros e responda em JSON:
{
  "message": "<sua resposta em português>",
  "action": {
    "type": "apply_filters",
    "payload": {
      "category": null | "furto_roubo"|"iluminacao"|"transito"|"espaco_publico_inseguro"|"vandalismo"|"moradores_situacao_rua"|"conflito_social"|"barulho_perturbacao"|"outro",
      "status": null | "pendente"|"em_analise"|"resolvido",
      "since": null | "YYYY-MM-DDTHH:MM:SSZ",
      "until": null | "YYYY-MM-DDTHH:MM:SSZ",
      "tag": null | "<texto exato da tag>"
    }
  } | null
}
Se a pergunta for conversacional (sem intenção de filtro), use "action": null.
Hoje é {current_date}. Use datas relativas ("semana passada" = desde {last_week_date}).
```

Usar `/nothink` no começo do prompt para desativar chain-of-thought e acelerar a resposta.

---

### Design de implementação recomendado

```
Backend (Python / clean arch):
  application/use_cases/parse_filter_intent.py
    ParseFilterIntent.execute(text, current_date) -> FilterIntentResult
      FilterIntentResult(message: str, action: FilterAction | None)
      FilterAction = {type: "apply_filters", payload: FilterParams}
      FilterParams = {category?, status?, since?, until?, tag?}
    
  Validation step: cada campo do payload validado contra ReportCategory enum / ReportStatus enum
  → action: None se qualquer campo inválido

  presentation/schemas/chat_schemas.py
    ChatMessageResponse += action: FilterActionResponse | None  (Pydantic)

Frontend (vanilla JS):
  function applyAction(action):
    if (action?.type === 'apply_filters') {
      showFilterPreview(action.payload)  // chips de confirmação
    }
  
  function showFilterPreview(payload):
    renderChips(payload)   // ex: "Categoria: Furto/Roubo  Desde: 09/06"
    btn-apply.onclick = () => { applyFiltersFromPayload(payload); loadReports(); }
    btn-discard.onclick = () => { hidePreview(); }
  
  function applyFiltersFromPayload(payload):
    document.getElementById('filter-category').value = payload.category || ''
    document.getElementById('filter-status').value = payload.status || ''
    // since/until → novos campos de data nos filtros
```

---

## Recomendações

| # | Prioridade | Recomendação |
|---|-----------|--------------|
| R1 | ALTA | Adotar Arquitetura A (action envelope) com validação server-side — `FilterParamsValidator` no application layer rejeita enums inválidos/datas malformadas e retorna `action: null`; o frontend sempre exibe o texto |
| R2 | ALTA | Adicionar chip de confirmação antes de aplicar filtros do chat — renderizar filtros extraídos como chips clicáveis acima do mapa; aplicação automática só para queries simples (1 filtro, enum exato) |
| R3 | ALTA | Definir desde já a resposta como discriminated union nullable (`action: null \| FilterActionEnvelope`) com Pydantic — impede que ações futuras (zoom_map, highlight_cluster) quebrem o contrato |
| R4 | MÉDIA | Criar `MockIntentParser` para testes unitários CI-safe; separar golden-set de integração (Ollama real) em `make test-llm` |
| R5 | MÉDIA | Adicionar loading state explícito no chat panel (spinner + input desabilitado durante LLM call ~1-4s no CPU) |
| R6 | MÉDIA | Não implementar Arquitetura D (SSE) nesta fase — custo de complexidade em vanilla JS não justificado para respostas curtas de filtro |
| R7 | BAIXA | Adicionar placeholder no input do chat ("Ex: relatos de furto desta semana no bairro X") e fallback textual quando `action: null` |

### Decisão central

**Use Arquitetura A** (action envelope no endpoint de chat existente) com:
- `ParseFilterIntent` como use case separado (chamado por `SendChatMessage`)
- Validação server-side do payload antes de retornar
- Chip de confirmação no frontend (não aplicação automática)

O trade-off chave: auto-apply é mais fluido mas cria problemas de controle do usuário. Confirmação explícita é levemente mais trabalhosa para o analista, mas é essencial num contexto de análise de segurança pública onde filtros errados levam a conclusões erradas.
