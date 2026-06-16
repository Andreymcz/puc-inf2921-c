# Plan 000062 | FEATURE-B | 2026-06-16 14:03 UTC | Backend: filtro temporal `until` | Review: light
plan_format_version: 1

## Brief

> roadmap-000056 Wave 1 Item 4 — Adicionar parâmetro `until: datetime | None` ao `ReportFilter` e expor `?until=` nos endpoints `GET /security_reports/geojson` e `GET /security_reports/`.

## Agent Interpretation

O endpoint `GET /security_reports/geojson` já expõe `?since=` para filtrar relatos a partir de uma data. A demanda é simétricamente adicionar `?until=` para filtrar relatos criados **até** uma data (`created_at <= until`), habilitando a janela temporal no frontend (plan-000063). É o plano mais simples do Wave 1 — apenas 3 arquivos, sem novos use cases.

---

## Scope

- **In scope**: `until: datetime | None` em `ReportFilter`; filtro `created_at <= until` na query SQLAlchemy; parâmetro `until` nos endpoints `GET /geojson` e `GET /`.
- **Out of scope**: Interface frontend para seleção de datas (Wave 2, plan-000063).

---

## Files

- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/repositories/security_report_repository.py` — adicionar `until: datetime | None = None` a `ReportFilter`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/repositories/sqlalchemy_security_report_repository.py` — aplicar filtro `until`
- `fala-gavea-seguranca/src/fala_gavea_seguranca/presentation/api/routers/security_reports.py` — parâmetro `until` nos dois endpoints
- `fala-gavea-seguranca/tests/unit/application/test_security_report_use_cases.py` — teste do filtro since+until

---

## Steps

### Step 1: Adicionar `until` ao `ReportFilter`

Em `domain/repositories/security_report_repository.py`, adicionar campo ao dataclass:
```python
until: datetime | None = None
```

- **Files**: `domain/repositories/security_report_repository.py`
- **Interface**: `ReportFilter.until: datetime | None`
- **Verify**: importar sem erro
- **Tests**: Step 3
- [ ] Done

### Step 2: Aplicar filtro `until` na query SQLAlchemy

Em `infrastructure/repositories/sqlalchemy_security_report_repository.py`, dentro de `find_all`, após o bloco `if filters.since`:
```python
if filters.until:
    q = q.filter(SecurityReportModel.created_at <= filters.until)
```

- **Files**: `infrastructure/repositories/sqlalchemy_security_report_repository.py`
- **Interface**: `find_all(filters=ReportFilter(until=datetime(...)))` aplica `created_at <= until`
- **Verify**: teste de integração (Step 3)
- [ ] Done

### Step 3: Expor `?until=` nos endpoints do router

Em `presentation/api/routers/security_reports.py`:

Para `get_geojson` e `list_security_reports`, adicionar parâmetro:
```python
until: datetime | None = Query(None),
```

E incluir no `ReportFilter(since=since, until=until, ...)`.

O padrão é idêntico ao `since` já existente — apenas adicionar o parâmetro paralelo.

- **Files**: `presentation/api/routers/security_reports.py`
- **Interface**: `GET /security_reports/geojson?since=2026-01-01T00:00:00&until=2026-06-01T00:00:00`
- **Verify**: `curl 'http://localhost:8000/security_reports/geojson?since=2026-01-01&until=2026-03-31'` retorna apenas relatos no intervalo
- [ ] Done

### Step 4: Testes

Em `tests/unit/application/test_security_report_use_cases.py` (ou novo `test_filters.py`):
- `test_filter_since_until_range`: cria 3 relatos com `created_at` em Jan, Mar e Jun; filtra `since=Feb` e `until=Apr`; verifica que apenas o relato de Mar é retornado.
- `test_filter_until_only`: cria relatos em Jan e Jun; `until=Mar`; apenas Jan retornado.

Em `tests/integration/api/test_security_reports_api.py`:
- `test_geojson_until_filter`: cria relato antigo e recente; `?until=<data entre eles>`; verifica que apenas o antigo retorna.

- **Files**: `tests/unit/application/test_security_report_use_cases.py`, `tests/integration/api/test_security_reports_api.py`
- **Verify**: `cd fala-gavea-seguranca && uv run pytest tests/ -k "until or filter" -v` passa
- [ ] Done

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | Mudança mínima — apenas estende o padrão `since` existente |
| DATA | Data Integrity | Adopted | Filtro via SQLAlchemy ORM; `created_at` já é indexável |
| TEST | Testability | Adopted | Testável com `tmp_path` e SQLite em memória |

---

## Commit message

```
feat(security-report): add ?until= temporal filter to geojson and list endpoints

Add until: datetime | None to ReportFilter and apply created_at <= until
filter in the SQLAlchemy repository. Expose ?until= query param on
GET /security_reports/geojson and GET /security_reports/.

Part of roadmap-000056 Wave 1 Item 4.
```
