# Plan 000061 | FEATURE-B | 2026-06-16 14:03 UTC | AI auto-categorização + curadoria pelo delegado | Review: light
plan_format_version: 1

## Brief

> roadmap-000056 Wave 1 Item 3 — `POST /{id}/auto_categorize` chama Ollama e salva sugestão em `ai_suggested_category`; `PATCH /{id}/category` permite ao delegado confirmar/corrigir a categoria.

## Agent Interpretation

Dois novos endpoints para o fluxo de curadoria de categoria:
1. **AI auto-categorização**: o cidadão ou operador solicita sugestão de categoria por IA → Ollama recebe o texto do relato + lista das 9 categorias válidas → retorna JSON com `category`, `confidence`, `justification` → salvo em `ai_suggested_category` (não altera `category` confirmada).
2. **Curadoria pelo delegado**: operador confirma ou corrige a categoria → `PATCH /{id}/category` atualiza `category` e zera `ai_suggested_category`.

**Depende de plan-000057** (Step 3) para o arquivo `infrastructure/ai/prompts.py::CATEGORIZE_PROMPT`. Se plan-000057 ainda não foi implementado, este plano deve criar o módulo `infrastructure/ai/` e o prompt.

---

## Scope

- **In scope**: campo `ai_suggested_category` na entidade + DB; use case `AutoCategorizeReport`; use case `SetReportCategory`; endpoints `POST /{id}/auto_categorize` e `PATCH /{id}/category`; integração com `ollama_client.py`; `ai_suggested_category` em `SecurityReportResponse`.
- **Out of scope**: Interface frontend para curadoria (Wave 2, plan-000063); exibição de confidence no response (retorna no corpo do auto-categorize mas não no schema de relato).

---

## Files

- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py` — campo `ai_suggested_category`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/repositories/security_report_repository.py` — abstract methods `update_category`, `update_ai_suggested_category`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/database/models.py` — coluna `ai_suggested_category`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/repositories/sqlalchemy_security_report_repository.py` — `update_category`, `update_ai_suggested_category`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/__init__.py` — create (empty; criado por plan-000057 Step 3, criar aqui se não existir)
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/prompts.py` — `CATEGORIZE_PROMPT` (criado por plan-000057 Step 3; criar aqui se não existir)
- `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/auto_categorize_report.py` — novo
- `fala-gavea-seguranca/src/fala_gavea_seguranca/application/use_cases/set_report_category.py` — novo
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/schemas/security_report_schemas.py` — `SecurityReportCategoryUpdate`, `AutoCategorizeResponse`, `ai_suggested_category` em `SecurityReportResponse`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/security_reports.py` — novos endpoints
- `fala-gavea-seguranca/tests/unit/application/test_auto_categorize.py` — novo
- `fala-gavea-seguranca/tests/integration/api/test_security_reports_api.py` — testes dos novos endpoints

---

## Steps

### Step 1: Verificar/criar `infrastructure/ai/prompts.py` e `__init__.py`

Verificar se `infrastructure/ai/prompts.py` existe (criado por plan-000057 Step 3). Se existir, apenas validar que `CATEGORIZE_PROMPT` está definido e compatível com `{text}` como variável. Se **não** existir, criar os arquivos:

**`infrastructure/ai/__init__.py`** — vazio.

**`infrastructure/ai/prompts.py`**:
```python
CATEGORIZE_PROMPT = """/nothink
Voce e um assistente especializado em seguranca publica urbana.
Categorize o relato abaixo escolhendo EXATAMENTE UMA das seguintes categorias:

- furto_roubo: Furtos, roubos, assaltos, tentativas de roubo
- iluminacao: Problemas de iluminacao publica (postes apagados, ruas escuras)
- transito: Transito caotico, acidentes, sinalizacao deficiente, pontos de onibus perigosos
- espaco_publico_inseguro: Espacos publicos inseguros ou abandonados (pracas, calcadas, paradas)
- vandalismo: Depredacao de patrimonio publico ou privado, pichacao
- moradores_situacao_rua: Concentracao de moradores em situacao de rua gerando inseguranca
- conflito_social: Conflito comunitario, tiroteio, tensao entre grupos, barricadas
- barulho_perturbacao: Barulho excessivo perturbando a ordem publica
- outro: Qualquer outro problema de seguranca que nao se encaixe nas categorias acima

Relato: {text}

Responda APENAS com JSON valido no formato:
{{"category": "<valor>", "confidence": "alta|media|baixa", "justification": "<max 1 frase>"}}
"""
```

- **Files**: `infrastructure/ai/__init__.py`, `infrastructure/ai/prompts.py`
- **Verify**: `uv run python -c "from fala_gavea_seguranca.infrastructure.ai.prompts import CATEGORIZE_PROMPT; print('OK')"` imprime OK
- **Tests**: N/A
- [ ] Done

### Step 2: Adicionar `ai_suggested_category` à entidade de domínio

Em `domain/entities/security_report.py`, adicionar campo:
```python
ai_suggested_category: ReportCategory | None = None
```

O campo é opcional (o relato nasce sem sugestão de IA). Não alterar `SecurityReport.create()` — o campo fica `None` por padrão.

- **Files**: `domain/entities/security_report.py`
- **Interface**: `SecurityReport.ai_suggested_category: ReportCategory | None`
- **Verify**: `uv run python -c "from fala_gavea_seguranca.domain.entities.security_report import SecurityReport; r = SecurityReport.create('t','iluminacao','u'); print(r.ai_suggested_category)"` imprime `None`
- [ ] Done

### Step 3: Adicionar coluna `ai_suggested_category` ao modelo DB e ao repositório

Em `infrastructure/database/models.py`, adicionar:
```python
ai_suggested_category = Column(SAEnum(ReportCategory), nullable=True)
```

Em `infrastructure/repositories/sqlalchemy_security_report_repository.py`:
- `_to_entity`: incluir `ai_suggested_category=ReportCategory(model.ai_suggested_category) if model.ai_suggested_category else None`
- `_to_model`: incluir `ai_suggested_category=entity.ai_suggested_category`
- Novo método `update_ai_suggested_category(self, id: str, category: ReportCategory | None) -> SecurityReport | None`
- Novo método `update_category(self, id: str, category: ReportCategory) -> SecurityReport | None` — atualiza `category` e zera `ai_suggested_category = None`

Declarar ambos como `@abstractmethod` no ABC `SecurityReportRepository`.

Deletar `app.db` e reiniciar para recriar schema.

- **Files**: `infrastructure/database/models.py`, `infrastructure/repositories/sqlalchemy_security_report_repository.py`, `domain/repositories/security_report_repository.py`
- **Verify**: reiniciar app; POST novo relato; verificar que `ai_suggested_category: null` no response
- [ ] Done

### Step 4: Criar use case `AutoCategorizeReport`

Criar `application/use_cases/auto_categorize_report.py`:

```python
from __future__ import annotations
import json
from dataclasses import dataclass
from ..domain.repositories.security_report_repository import SecurityReportRepository
from ..domain.entities.security_report import ReportCategory
from ..domain.exceptions import SecurityReportNotFoundError
from ..infrastructure.llm.ollama_client import chat_completion
from ..infrastructure.ai.prompts import CATEGORIZE_PROMPT


@dataclass
class AutoCategorizeResult:
    category: str
    confidence: str
    justification: str


class AutoCategorizeReport:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> AutoCategorizeResult:
        entity = self._repo.find_by_id(id)
        if entity is None:
            raise SecurityReportNotFoundError(f"Report {id} not found")

        prompt = CATEGORIZE_PROMPT.format(text=entity.text)
        raw = chat_completion([{"role": "user", "content": prompt}])

        try:
            data = json.loads(raw.strip())
            category_str = data["category"]
            category = ReportCategory(category_str)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Resposta inválida do modelo: {raw!r}") from e

        self._repo.update_ai_suggested_category(id, category)

        return AutoCategorizeResult(
            category=category.value,
            confidence=data.get("confidence", ""),
            justification=data.get("justification", ""),
        )
```

- **Files**: `application/use_cases/auto_categorize_report.py`
- **Interface**: `AutoCategorizeReport(repo).execute(id) -> AutoCategorizeResult`
- **Tests**: Step 6
- [ ] Done

### Step 5: Criar use case `SetReportCategory` e schemas

**`application/use_cases/set_report_category.py`**:
```python
from __future__ import annotations
from dataclasses import dataclass
from ..domain.repositories.security_report_repository import SecurityReportRepository
from ..domain.entities.security_report import ReportCategory, SecurityReport
from ..domain.exceptions import SecurityReportNotFoundError, InvalidInputError


@dataclass
class SetReportCategoryInput:
    id: str
    category: str


class SetReportCategory:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, input: SetReportCategoryInput) -> SecurityReport:
        try:
            category = ReportCategory(input.category)
        except ValueError:
            raise InvalidInputError(f"Categoria inválida: {input.category!r}")

        entity = self._repo.update_category(input.id, category)
        if entity is None:
            raise SecurityReportNotFoundError(f"Report {input.id} not found")
        return entity
```

Em `presentation/schemas/security_report_schemas.py`:
- Adicionar `class SecurityReportCategoryUpdate(BaseModel): category: str`
- Adicionar `class AutoCategorizeResponse(BaseModel): category: str; confidence: str; justification: str`
- Adicionar `ai_suggested_category: str | None` a `SecurityReportResponse`

- **Files**: `application/use_cases/set_report_category.py`, `presentation/schemas/security_report_schemas.py`
- [ ] Done

### Step 6: Adicionar endpoints ao router

Em `presentation/api/routers/security_reports.py`:

```python
@router.post("/{id}/auto_categorize", response_model=AutoCategorizeResponse)
def auto_categorize(
    id: str,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> AutoCategorizeResponse:
    try:
        result = AutoCategorizeReport(repo).execute(id)
        return AutoCategorizeResponse(
            category=result.category,
            confidence=result.confidence,
            justification=result.justification,
        )
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.patch("/{id}/category", response_model=SecurityReportResponse)
def set_category(
    id: str,
    body: SecurityReportCategoryUpdate,
    repo: SQLAlchemySecurityReportRepository = Depends(get_security_report_repo),
) -> SecurityReportResponse:
    try:
        entity = SetReportCategory(repo).execute(SetReportCategoryInput(id=id, category=body.category))
        return SecurityReportResponse(**entity.__dict__)
    except SecurityReportNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
```

Atualizar `get_geojson` para incluir `"ai_suggested_category": e.ai_suggested_category.value if e.ai_suggested_category else None` nas properties.

- **Files**: `presentation/api/routers/security_reports.py`
- **Verify**: `curl -X POST http://localhost:8000/security_reports/<id>/auto_categorize` com Ollama rodando; `curl -X PATCH .../category -d '{"category":"furto_roubo"}'`
- [ ] Done

### Step 7: Testes

**`tests/unit/application/test_auto_categorize.py`** (novo arquivo):
- `test_auto_categorize_success`: mock `find_by_id` retorna entidade; mock `chat_completion` retorna JSON válido; verifica `update_ai_suggested_category` chamado com `ReportCategory.FURTO_ROUBO`.
- `test_auto_categorize_invalid_json`: mock `chat_completion` retorna texto inválido; verifica `ValueError`.
- `test_auto_categorize_not_found`: mock `find_by_id` retorna `None`; verifica `SecurityReportNotFoundError`.
- `test_set_report_category_success`: mock `update_category` retorna entidade; verifica que zera `ai_suggested_category`.
- `test_set_report_category_invalid`: verifica `InvalidInputError` para categoria desconhecida.

**`tests/integration/api/test_security_reports_api.py`**:
- `test_patch_category`: cria relato; `PATCH /{id}/category` com `furto_roubo`; verifica response.
- `test_post_auto_categorize_no_ollama`: verifica 502 quando Ollama não está disponível (mock `chat_completion` levanta `RuntimeError`).

- **Files**: `tests/unit/application/test_auto_categorize.py`, `tests/integration/api/test_security_reports_api.py`
- **Verify**: `cd fala-gavea-seguranca && uv run pytest tests/ -k "categoriz" -v` passa
- [ ] Done

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | LLM call encapsulado no use case; não toca diretamente no router |
| DATA | Data Integrity | Adopted | `ai_suggested_category` nullable; `update_category` zera o campo (curadoria limpa) |
| SEC | Security | Adopted | Prompt não inclui input não-sanitizado além do texto do relato; resposta parseada como JSON (não avaliada) |
| TEST | Testability | Adopted | `chat_completion` mockável; testes isolados de Ollama |
| ERR | Error Handling | Adopted | 502 para Ollama inacessível; 422 para categoria inválida; 404 para relato não encontrado |

---

## Commit message

```
feat(security-report): AI auto-categorization + delegado curation

POST /security_reports/{id}/auto_categorize calls Ollama with
CATEGORIZE_PROMPT and stores ai_suggested_category (non-destructive).
PATCH /security_reports/{id}/category lets the delegado confirm or
correct the category, clearing the AI suggestion.

Requires plan-000057 (9-category enum + prompts.py) to be applied first.
Part of roadmap-000056 Wave 1 Item 3.
```
