# Plan 000068 | FEATURE-X | 2026-06-16 21:30 UTC | Chat NL intent-to-filter — busca inteligente com IA | Review: standard
plan_format_version: 1
source: research-000066 — NL intent extraction com action envelope, validação server-side, chip de confirmação

## Brief

> source: research-000066 — implementar busca inteligente com chat NL: action envelope no endpoint de chat existente, ParseFilterIntent use case com validação server-side, chip de confirmação no frontend vanilla JS + Leaflet

## Agent Interpretation

O analista quer digitar intenções em linguagem natural no mapa ("mostra relatos de furto da semana passada") e o sistema converter automaticamente em filtros da API (`category=furto_roubo&since=2026-06-09`) + atualização do mapa.

**Arquitetura escolhida (research-000066 Rec R1-R3):** Endpoint independente `POST /intents/parse` — recebe texto, chama Ollama com prompt estruturado, valida payload server-side, retorna `{message, action | null}`. Frontend em `index.html` tem painel de intent chat inline (sem navegar para `chat.html`). Antes de aplicar os filtros, mostra chips de confirmação.

**Por que endpoint separado (não modificar `/chats/`):** o `chat.html` existente depende de `POST /chats/{id}/messages` retornar `list[ChatMessageResponse]`. Manter separados preserva a RAG chat intacta e evita sessões de chat desnecessárias para o caso de uso de filtro rápido.

---

## Scope

- **In scope**: domínio `FilterParams`/`FilterAction`; use case `ParseFilterIntent` (LLM → JSON → validação); novo router `/intents`; painel de intent chat em `index.html` + lógica em `app.js`; testes unitários de `ParseFilterIntent`
- **Out of scope**: histórico persistido de intents; modificação de `chat.html` ou `SendChatMessage`; filtros de bbox por NL (já funciona via checkbox); streaming SSE

---

## Files

- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/filter_action.py` — **NEW** — `FilterParams`, `FilterAction` dataclasses
- `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/parse_filter_intent.py` — **NEW** — `ParseFilterIntent` use case
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/schemas/chat_schemas.py` — **MODIFY** — adicionar `FilterActionPayloadResponse`, `FilterActionResponse`, `ParseIntentRequest`, `ParseIntentResponse`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/intents.py` — **NEW** — `POST /intents/parse`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/main.py` — **MODIFY** — registrar `intents_router`
- `fala-gavea-seguranca/static/index.html` — **MODIFY** — adicionar `#intent-panel` no sidebar e `#filter-preview-bar` flutuante
- `fala-gavea-seguranca/static/app.js` — **MODIFY** — lógica do intent chat (sendIntent, renderIntentMessage, showFilterPreview, applyFilterFromChat)
- `fala-gavea-seguranca/tests/unit/application/test_parse_filter_intent.py` — **NEW** — testes unitários com mock de `chat_completion`

---

## Steps

### Step 1: Tipos de domínio — `FilterParams` e `FilterAction`

Criar `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/filter_action.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FilterParams:
    category: str | None = None
    status: str | None = None
    since: str | None = None   # ISO 8601 string; validado no use case
    until: str | None = None   # ISO 8601 string; validado no use case
    tag: str | None = None


@dataclass
class FilterAction:
    type: str           # "apply_filters"
    payload: FilterParams


@dataclass
class FilterIntentResult:
    message: str
    action: FilterAction | None
```

- **Files**: `domain/entities/filter_action.py`
- **Verify**: `python -c "from fala_gavea_seguranca.domain.entities.filter_action import FilterIntentResult"` sem erro

---

### Step 2: Use case `ParseFilterIntent`

Criar `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/parse_filter_intent.py`:

```python
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone  # datetime also used in _validate_payload guard

from fala_gavea_seguranca.domain.entities.filter_action import FilterAction, FilterIntentResult, FilterParams
from fala_gavea_seguranca.infrastructure.llm.ollama_client import chat_completion

log = logging.getLogger(__name__)

_VALID_CATEGORIES = frozenset({
    "furto_roubo", "iluminacao", "transito", "espaco_publico_inseguro",
    "vandalismo", "moradores_situacao_rua", "conflito_social",
    "barulho_perturbacao", "outro",
})
_VALID_STATUSES = frozenset({"pendente", "em_analise", "resolvido"})

_SYSTEM_PROMPT = """/nothink
Você é um assistente de análise de segurança pública da Gávea.

Quando o analista descrever o que quer visualizar no mapa, extraia os filtros e responda APENAS com JSON válido:
{{
  "message": "<resposta em português, 1-2 frases descrevendo o que será mostrado>",
  "action": {{
    "type": "apply_filters",
    "payload": {{
      "category": null ou um de: "furto_roubo","iluminacao","transito","espaco_publico_inseguro","vandalismo","moradores_situacao_rua","conflito_social","barulho_perturbacao","outro",
      "status": null ou um de: "pendente","em_analise","resolvido",
      "since": null ou data ISO 8601 (ex: "2026-06-09T00:00:00Z"),
      "until": null ou data ISO 8601,
      "tag": null ou texto exato da tag
    }}
  }}
}}

Se a mensagem for conversacional ou não tiver intenção de filtrar o mapa, use "action": null.
HOJE É: {today}. Datas relativas: "semana passada"=desde {week_ago}; "mês passado"=desde {month_ago}.
Responda APENAS com JSON, sem markdown, sem explicações extras."""


@dataclass
class ParseFilterIntentInput:
    text: str
    now: datetime | None = None  # injetável em testes


class ParseFilterIntent:
    def __init__(self, llm_fn=chat_completion) -> None:
        self._llm = llm_fn

    def execute(self, inp: ParseFilterIntentInput) -> FilterIntentResult:
        now = inp.now or datetime.now(tz=timezone.utc)
        week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
        month_ago = (now - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
        today = now.strftime("%Y-%m-%d")

        system = _SYSTEM_PROMPT.format(today=today, week_ago=week_ago, month_ago=month_ago)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": inp.text},
        ]

        try:
            raw = self._llm(messages)
        except RuntimeError:
            raise

        # Parse JSON — strip markdown fences if present
        text = raw.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:])
            text = text.rsplit("```", 1)[0].strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            log.warning("ParseFilterIntent: JSON inválido: %s", e)
            return FilterIntentResult(message=raw, action=None)

        message = data.get("message", "")
        raw_action = data.get("action")
        if not raw_action or not isinstance(raw_action, dict):
            return FilterIntentResult(message=message, action=None)

        payload_raw = raw_action.get("payload", {})
        validated = _validate_payload(payload_raw)
        if validated is None:
            return FilterIntentResult(message=message, action=None)

        return FilterIntentResult(
            message=message,
            action=FilterAction(type="apply_filters", payload=validated),
        )


def _validate_payload(raw: dict) -> FilterParams | None:
    category = raw.get("category")
    status = raw.get("status")
    since = raw.get("since")
    until = raw.get("until")
    tag = raw.get("tag")

    if category is not None and category not in _VALID_CATEGORIES:
        log.warning("ParseFilterIntent: categoria inválida '%s' — ignorada", category)
        category = None
    if status is not None and status not in _VALID_STATUSES:
        log.warning("ParseFilterIntent: status inválido '%s' — ignorado", status)
        status = None
    if since is not None:
        try:
            datetime.fromisoformat(since.replace("Z", "+00:00"))
        except ValueError:
            log.warning("ParseFilterIntent: since inválido '%s' — ignorado", since)
            since = None
    if until is not None:
        try:
            datetime.fromisoformat(until.replace("Z", "+00:00"))
        except ValueError:
            log.warning("ParseFilterIntent: until inválido '%s' — ignorado", until)
            until = None
    if tag is not None and not isinstance(tag, str):
        tag = None

    # Guard: faixa de datas invertida produz zero resultados silenciosamente — rejeitar
    if since is not None and until is not None:
        try:
            if datetime.fromisoformat(since.replace("Z", "+00:00")) > datetime.fromisoformat(until.replace("Z", "+00:00")):
                log.warning("ParseFilterIntent: since > until ('%s' > '%s') — ambos ignorados", since, until)
                since = None
                until = None
        except ValueError:
            pass  # já validados acima; defensivo

    # Se todos null, não há filtro útil
    if all(v is None for v in [category, status, since, until, tag]):
        return None

    return FilterParams(category=category, status=status, since=since, until=until, tag=tag)
```

- **Files**: `application/use_cases/parse_filter_intent.py`
- **Verify**: importar sem erro; `_validate_payload({"category": "invalido"})` retorna `None`

---

### Step 3: Schema Pydantic — tipos de resposta

Em `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/schemas/chat_schemas.py`, adicionar `from pydantic import Field` ao import existente e depois adicionar ao fim:

```python
class FilterActionPayloadResponse(BaseModel):
    category: str | None = None
    status: str | None = None
    since: str | None = None
    until: str | None = None
    tag: str | None = None


class FilterActionResponse(BaseModel):
    type: str
    payload: FilterActionPayloadResponse


class ParseIntentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


class ParseIntentResponse(BaseModel):
    message: str
    action: FilterActionResponse | None = None
```

- **Files**: `presentation/schemas/chat_schemas.py`
- **Verify**: importar sem erro

---

### Step 4: Router `/intents`

Criar `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/intents.py`:

```python
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from fala_gavea_seguranca.application.use_cases.parse_filter_intent import ParseFilterIntent, ParseFilterIntentInput
from fala_gavea_seguranca.presentation.schemas.chat_schemas import (
    FilterActionPayloadResponse,
    FilterActionResponse,
    ParseIntentRequest,
    ParseIntentResponse,
)

router = APIRouter()


@router.post("/parse", response_model=ParseIntentResponse, status_code=status.HTTP_200_OK)
def parse_intent(body: ParseIntentRequest) -> ParseIntentResponse:
    try:
        result = ParseFilterIntent().execute(ParseFilterIntentInput(text=body.text))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    action_resp = None
    if result.action:
        p = result.action.payload
        action_resp = FilterActionResponse(
            type=result.action.type,
            payload=FilterActionPayloadResponse(
                category=p.category,
                status=p.status,
                since=p.since,
                until=p.until,
                tag=p.tag,
            ),
        )

    return ParseIntentResponse(message=result.message, action=action_resp)
```

- **Files**: `presentation/api/routers/intents.py`
- **Verify**: importar sem erro

---

### Step 5: Registrar router em `main.py`

Em `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/main.py`:

Adicionar import:
```python
from .routers.intents import router as intents_router
```

Adicionar `include_router` após `chats_router`:
```python
app.include_router(intents_router, prefix="/intents", tags=["intents"])
```

- **Files**: `presentation/api/main.py`
- **Verify**: `uv run uvicorn fala_gavea_seguranca.presentation.api.main:app --reload` sobe sem erro; `curl -X POST http://localhost:8000/intents/parse -H "Content-Type: application/json" -d '{"text":"mostra relatos de furto"}'` retorna JSON com `message` e `action`

---

### Step 6: Frontend HTML — painel de intent chat em `index.html`

Em `fala-gavea-seguranca/static/index.html`:

**a) Adicionar `#intent-panel` no `#sidebar`, após `#search-panel` e antes de `#iluminacao-panel`:**

```html
<div id="intent-panel">
  <h2>Busca com IA</h2>
  <div id="intent-messages" aria-live="polite" aria-label="Respostas da IA"></div>
  <div class="intent-input-row">
    <label for="intent-input" class="sr-only">Descreva o que quer visualizar</label>
    <input type="text" id="intent-input"
           placeholder="Ex: relatos de furto desta semana..."
           onkeydown="handleIntentKey(event)" />
    <button id="btn-send-intent" onclick="sendIntent()" aria-label="Enviar">➤</button>
  </div>
</div>
```

**b) Adicionar `#filter-preview-bar` fora do sidebar (logo antes de `</body>`):**

```html
<div id="filter-preview-bar" class="hidden">
  <span id="filter-preview-chips"></span>
  <button id="btn-apply-intent-filter" onclick="applyFilterFromChat()">✓ Aplicar</button>
  <button id="btn-discard-intent-filter" onclick="discardChatFilter()" aria-label="Descartar filtro sugerido">✕</button>
</div>
```

**c) Adicionar ao `style.css` (se ausente):**

```css
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0;
           overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
```

- **Files**: `static/index.html`
- **Verify**: layout renderizado no browser sem erros de console

---

### Step 7: Frontend JS — lógica do intent chat em `app.js`

Adicionar ao final de `fala-gavea-seguranca/static/app.js`:

```javascript
// ── Intent Chat ──────────────────────────────────────────────────────────────

const CATEGORY_LABELS_FULL = {
  furto_roubo: 'Furto/Roubo', iluminacao: 'Iluminação', transito: 'Trânsito',
  espaco_publico_inseguro: 'Espaço Inseguro', vandalismo: 'Vandalismo',
  moradores_situacao_rua: 'Moradores em Situação de Rua',
  conflito_social: 'Conflito/Tensão', barulho_perturbacao: 'Barulho/Perturbação',
  outro: 'Outro',
};

let pendingIntentAction = null;

function handleIntentKey(e) {
  if (e.key === 'Enter') { e.preventDefault(); sendIntent(); }
}

async function sendIntent() {
  const input = document.getElementById('intent-input');
  const text = input.value.trim();
  if (!text) return;

  const btn = document.getElementById('btn-send-intent');
  input.disabled = true;
  btn.disabled = true;
  btn.textContent = '…';

  renderIntentMessage('user', text);
  input.value = '';

  try {
    const res = await fetch('/intents/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    renderIntentMessage('assistant', data.message || 'Sem resposta.');
    if (data.action?.type === 'apply_filters') {
      showFilterPreview(data.action.payload);
    }
  } catch (e) {
    renderIntentMessage('assistant', 'Erro de rede: ' + e.message);
  } finally {
    input.disabled = false;
    btn.disabled = false;
    btn.textContent = '➤';
    input.focus();
  }
}

function renderIntentMessage(role, text) {
  const container = document.getElementById('intent-messages');
  const div = document.createElement('div');
  div.className = 'intent-msg intent-msg--' + role;
  div.textContent = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function showFilterPreview(payload) {
  pendingIntentAction = payload;
  const chips = [];
  if (payload.category) chips.push('Categoria: ' + (CATEGORY_LABELS_FULL[payload.category] || payload.category));
  if (payload.status) chips.push('Status: ' + payload.status.replace('_', ' '));
  if (payload.since) chips.push('De: ' + new Date(payload.since).toLocaleDateString('pt-BR'));
  if (payload.until) chips.push('Até: ' + new Date(payload.until).toLocaleDateString('pt-BR'));
  if (payload.tag) chips.push('Tag: ' + payload.tag);

  document.getElementById('filter-preview-chips').textContent = chips.join('  |  ');
  document.getElementById('filter-preview-bar').classList.remove('hidden');
}

function applyFilterFromChat() {
  if (!pendingIntentAction) return;
  const p = pendingIntentAction;

  document.getElementById('filter-category').value = p.category || '';
  document.getElementById('filter-status').value = p.status || '';

  const fromEl = document.getElementById('filter-date-from');
  const toEl = document.getElementById('filter-date-to');
  if (fromEl) fromEl.value = p.since ? p.since.slice(0, 10) : '';
  if (toEl) toEl.value = p.until ? p.until.slice(0, 10) : '';

  const tagEl = document.getElementById('filter-tag');
  if (tagEl) tagEl.value = p.tag || '';

  discardChatFilter();
  loadReports();
}

function discardChatFilter() {
  pendingIntentAction = null;
  document.getElementById('filter-preview-bar').classList.add('hidden');
}
```

- **Files**: `static/app.js`
- **Verify**: digitar "mostra relatos de furto" no painel → chip aparece → clicar Aplicar → mapa filtra por `furto_roubo`

---

### Step 8: Testes unitários — `ParseFilterIntent`

Criar `fala-gavea-seguranca/tests/unit/application/test_parse_filter_intent.py`:

```python
from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from fala_gavea_seguranca.application.use_cases.parse_filter_intent import ParseFilterIntent, ParseFilterIntentInput


def _mock_llm(response: str):
    def _fn(messages, model=None):
        return response
    return _fn


def _make_input(text: str = "mostra relatos de furto", now=None):
    return ParseFilterIntentInput(
        text=text,
        now=now or datetime(2026, 6, 16, 12, 0, 0, tzinfo=timezone.utc),
    )


def test_valid_category_intent():
    payload = json.dumps({
        "message": "Mostrando relatos de furto e roubo.",
        "action": {"type": "apply_filters", "payload": {"category": "furto_roubo"}},
    })
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input())
    assert result.action is not None
    assert result.action.payload.category == "furto_roubo"
    assert result.message == "Mostrando relatos de furto e roubo."


def test_invalid_category_returns_none_action():
    payload = json.dumps({
        "message": "...",
        "action": {"type": "apply_filters", "payload": {"category": "categoria_inexistente"}},
    })
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input())
    assert result.action is None  # payload todo null → None


def test_conversational_message_no_action():
    payload = json.dumps({"message": "Não entendi, pode reformular?", "action": None})
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input("olá"))
    assert result.action is None


def test_malformed_json_falls_back():
    uc = ParseFilterIntent(llm_fn=_mock_llm("isso não é json"))
    result = uc.execute(_make_input())
    assert result.action is None
    assert "isso não é json" in result.message


def test_markdown_fences_stripped():
    payload = "```json\n" + json.dumps({"message": "ok", "action": None}) + "\n```"
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input())
    assert result.action is None
    assert result.message == "ok"


def test_since_until_extracted():
    payload = json.dumps({
        "message": "Relatos da semana passada.",
        "action": {"type": "apply_filters", "payload": {
            "category": None, "status": None,
            "since": "2026-06-09T00:00:00Z", "until": None, "tag": None,
        }},
    })
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input("relatos da semana passada"))
    assert result.action is not None
    assert result.action.payload.since == "2026-06-09T00:00:00Z"


def test_invalid_date_ignored():
    payload = json.dumps({
        "message": "ok",
        "action": {"type": "apply_filters", "payload": {"since": "not-a-date"}},
    })
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input())
    assert result.action is None


def test_ollama_unreachable_raises():
    def _fail(messages, model=None):
        raise RuntimeError("Ollama não está acessível")
    uc = ParseFilterIntent(llm_fn=_fail)
    with pytest.raises(RuntimeError, match="Ollama"):
        uc.execute(_make_input())


def test_inverted_date_range_ignored():
    """Emenda C: since > until → ambos nullificados → action None."""
    payload = json.dumps({
        "message": "ok",
        "action": {"type": "apply_filters", "payload": {
            "since": "2026-06-30T00:00:00Z",
            "until": "2026-06-01T00:00:00Z",
        }},
    })
    uc = ParseFilterIntent(llm_fn=_mock_llm(payload))
    result = uc.execute(_make_input())
    assert result.action is None  # datas invertidas → payload todo null → None
```

Teste de input vazio (Emenda A) é coberto pelo Pydantic `min_length=1` na validação do endpoint — verificado via teste de integração opcional.

- **Files**: `tests/unit/application/test_parse_filter_intent.py`
- **Verify**: `cd fala-gavea-seguranca && uv run pytest tests/unit/application/test_parse_filter_intent.py -v` — 9 testes passam

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | Endpoint separado `/intents/parse` preserva RAG chat intacto; clean arch respeitada (domain → app → presentation) |
| SEC | Security | Adopted | Allowlisting server-side em `_validate_payload()`; `Field(max_length=500)` em `ParseIntentRequest` (Emenda A); `action: null` em caso de falha; DOM atualizado via `textContent` (XSS-safe) |
| UX | UX / Communicability | Adopted | Chip de confirmação antes de aplicar filtros (Rec R2 da research-000066); spinner + input disabled durante LLM call |
| A11Y | Accessibility | Adopted | `aria-live="polite"` em `#intent-messages`; `aria-label` em botões de ícone; `<label class="sr-only">` para input (Emenda B) |
| API | API Design | Adopted | Discriminated union nullable (`action: null | FilterActionResponse`) estável; backwards compatible com `chat.html` |
| TEST | Testability | Adopted | `ParseFilterIntent` aceita `llm_fn` injetável; 9 testes CI-safe sem Ollama real; guard `since > until` testado (Emenda C) |

---

## Commit message

```
feat(intent): chat NL intent-to-filter — POST /intents/parse + painel inline no mapa

Add ParseFilterIntent use case: LLM extracts structured filter params from
NL text, validates each field against domain enums/ISO dates server-side,
returns null action on validation failure.

New POST /intents/parse endpoint returns {message, action|null}.
index.html gains inline intent chat panel + filter preview chips bar.
app.js adds sendIntent, showFilterPreview, applyFilterFromChat.

source: research-000066
```
