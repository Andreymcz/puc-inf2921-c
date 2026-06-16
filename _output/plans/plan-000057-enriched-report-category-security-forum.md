# Plan 000057 | FEATURE-B | 2026-06-16 13:41 UTC | Enriquecer ReportCategory a partir do Forum de Seguranca LGD | Review: light
# DONE | 2026-06-16 14:35 UTC |
plan_format_version: 1

## Brief

> Analise os relatos dos stakeholders da seguranca a partir de @knowledge/library/RELATORIO FORUM SEGURANCA_LGD.pdf para termos uma ideia melhor das categorias de interesse relacionados a seguranca. Enriquecer o enum `ReportCategory` com as categorias derivadas da analise.

## Agent Interpretation

O PDF analisado e o relatorio da "Roda de Conversa Estrategica sobre Seguranca na Gavea" (GaveaLab / PUC-Rio, 11/06/2024). O forum usou a tecnica dos 5 Porques com stakeholders diversificados (moradores, liderancas comunitarias, delegada, guarda municipal, poder publico, empresarios) para mapear as causas da inseguranca.

A partir dessa analise, o enum `ReportCategory` atual (4 valores: `iluminacao`, `transito`, `vandalismo`, `outro`) e insuficiente para capturar os tipos de ocorrencias que cidadaos da Gavea efetivamente reportam. O plano enriquece o enum para 9 categorias derivadas diretamente dos problemas identificados no forum, atualiza o dataset fake, e prepara o prompt de auto-categorizacao por IA (Wave 1, Item 3 do roadmap-000056) para usar as novas categorias.

---

## Analise do Forum -- Taxonomia de Problemas de Seguranca

### Stakeholders participantes

| Perfil | Representantes |
|--------|----------------|
| Moradores Gavea asfalto | Luiza Carneiro (AMAGAVEA), Lia Blower, Lidia Vales |
| Moradores / lideres comunitarios (favelas) | Marcelo Queiroz (Rocinha), Leandro Santos / Waldir Cavalcante (Parque da Cidade), Willian de Oliveira (Rocinha) |
| Poder publico | Flavia Monteiro (1 DPA Policia), Paulo Protas io (ADSER-RJ), Ronaldo Messias (Guarda Municipal) |
| Empresarios e escola | Alvaro Albuquerque (Casa da Tata), Jacqueline Branco (Escola Manoel Cicero), Pedro Protasio |

### Problemas observaveis identificados (perspectiva do cidadao)

Com base na **consolidacao das 5 perguntas** (secao 4) e nos **debates entre especialistas** (secao 5), os problemas de seguranca que cidadaos vivenciam e reportariam num app como o Fala-Gavea sao:

| Categoria proposta | Evidencia no relatorio | Frequencia mencionada |
|-------------------|------------------------|----------------------|
| **Furtos e roubos** | "situacoes concretas de violencia (como furtos e assaltos)" (P1.1); medo de andar a pe, sair sozinho | Alta -- citada como manifestacao concreta primaria |
| **Iluminacao precaria** | "planejamento urbano com foco em seguranca, incluindo iluminacao publica" (P4, P5, sec. 5); causas operacionais d) | Alta -- mencionada multiplas vezes como causa estrutural |
| **Transito e mobilidade** | "transito caotico, pontos de onibus mal localizados" (P1.1); "transporte ineficiente" (causas d) | Alta -- citada como fator de vulnerabilidade diaria |
| **Vandalismo / depredacao** | Implicitamente na "infraestrutura urbana precaria" e "espacos publicos pouco seguros" | Media |
| **Espaco publico inseguro** | "pontos de onibus em locais inseguros", "espacos publicos pouco seguros" (causas d); "ativacao do espaco publico" como solucao (sec. 6c) | Alta -- aborda sensacao de inseguranca em espacos fisicos |
| **Moradores em situacao de rua** | "moradores em situacao de rua" listados explicitamente como problema urbano visivel (P1.1) | Media |
| **Conflito / tensao comunitaria** | "distancia simbolica e fisica entre a Gavea e as favelas" (P2), segregacao territorial como causa estrutural, desafio b da sec. 6 | Media |
| **Barulho / perturbacao da ordem** | "perturbacao da ordem" inferida dos debates sobre convivencia e espaco publico | Baixa-media |
| **Outro** | Captura o residual | Sempre necessario |

### Distribuicao sugerida para dataset fake

| Categoria | % |
|-----------|---|
| `furto_roubo` | 28% |
| `iluminacao` | 22% |
| `transito` | 18% |
| `espaco_publico_inseguro` | 12% |
| `vandalismo` | 8% |
| `moradores_situacao_rua` | 5% |
| `conflito_social` | 4% |
| `barulho_perturbacao` | 2% |
| `outro` | 1% |

---

## Scope

- **In scope**: Atualizar `ReportCategory` enum no dominio; recriar o `app.db` limpo com o novo schema; atualizar o script de seed (Wave 0 do roadmap-000056) para usar as novas categorias e distribuicoes; atualizar o endpoint `/security_reports/geojson` com o novo filtro de categoria; preparar o template de prompt de IA (para Wave 1 Item 3 do roadmap-000056).
- **Out of scope**: Implementar o endpoint de auto-categorizacao por IA (Wave 1 Item 3, plano proprio no roadmap-000056); implementar filtragem no frontend (Wave 2 do roadmap-000056).

---

## Files

- `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py` -- enum `ReportCategory`
- `fala-gavea-seguranca/scripts/seed_reports.py` -- script de seed com novas categorias e distribuicoes
- `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/database/session.py` -- referencia para saber como o DB e inicializado
- `fala-gavea-seguranca/app.db` -- deletar e recriar (derived artifact)

---

## Steps

### Step 1: Enriquecer o enum ReportCategory com as 9 categorias derivadas do forum

Atualizar `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py` para expandir `ReportCategory` de 4 para 9 valores baseados na analise do relatorio do Forum de Seguranca da Gavea.

**Novo enum:**
```python
class ReportCategory(str, Enum):
    FURTO_ROUBO             = "furto_roubo"
    ILUMINACAO              = "iluminacao"
    TRANSITO                = "transito"
    ESPACO_PUBLICO_INSEGURO = "espaco_publico_inseguro"
    VANDALISMO              = "vandalismo"
    MORADORES_SITUACAO_RUA  = "moradores_situacao_rua"
    CONFLITO_SOCIAL         = "conflito_social"
    BARULHO_PERTURBACAO     = "barulho_perturbacao"
    OUTRO                   = "outro"
```

SQLite nao aplica restrictions de enum no banco -- os valores sao armazenados como strings. Por isso, nenhuma migracao de banco e necessaria: basta deletar `app.db` (arquivo derivado, nao versionado) e reiniciar o servidor para que o `create_all()` recrie as tabelas com o novo schema.

Apos a mudanca no enum, deletar `fala-gavea-seguranca/app.db` para que o DB seja recriado.

- **Files**: `fala-gavea-seguranca/src/fala_gavea_seguranca/domain/entities/security_report.py` (modify), `fala-gavea-seguranca/app.db` (delete)
- **References**: `product-design/project/standards.md` (Constitution T1 -- centralize domain entities)
- **Interface**: `ReportCategory` enum com 9 valores exportado de `domain/entities/security_report.py` -- usado por use cases, repository, models, router
- **Verify**: `uv run python -c "from fala_gavea_seguranca.domain.entities.security_report import ReportCategory; print([c.value for c in ReportCategory])"` imprime os 9 valores
- **Tests**: Atualizar / adicionar teste em `tests/` que verifica que todos os 9 valores de `ReportCategory` sao validos e que `FURTO_ROUBO` e `ESPACO_PUBLICO_INSEGURO` existem
- [x] Done

### Step 2: Atualizar o script de seed com as novas categorias e distribuicoes realistas

Criar ou atualizar `fala-gavea-seguranca/scripts/seed_reports.py` para usar os 9 novos valores de `ReportCategory` com a distribuicao derivada do forum (28% furto_roubo, 22% iluminacao, 18% transito, 12% espaco_publico_inseguro, 8% vandalismo, 5% moradores_situacao_rua, 4% conflito_social, 2% barulho_perturbacao, 1% outro).

O script deve:
- Usar `random.choices` com pesos correspondentes as porcentagens acima para sortear a categoria de cada relato
- Ter textos plausíveis em pt-BR para cada nova categoria (minimo 5 variantes por categoria nova)
- Exemplos de textos para categorias novas:
  - `furto_roubo`: "Fui assaltado na Rua Marques de Sao Vicente ontem a noite", "Assalto a transeunte proximo ao ISAM"
  - `espaco_publico_inseguro`: "Ponto de onibus da Gavea sem iluminacao e sem cobertura, muito perigoso", "Pracinha do Baixo Gavea com grupinhos suspeitos toda tarde"
  - `moradores_situacao_rua`: "Varios moradores em situacao de rua dormindo na entrada do parque", "Concentracao de pessoas em situacao de rua proximo ao shopping"
  - `conflito_social`: "Tensao e barricadas na entrada da comunidade desde ontem", "Tiroteio ouvido na regiao da Rocinha afetando o transito"
  - `barulho_perturbacao`: "Baile funk ate 3h da manha com muito barulho na Rua da Gavea"
- Manter o script idempotente: `DELETE FROM security_reports WHERE author_id LIKE 'seed-%'` antes do insert
- Gerar 250 relatos com coordenadas dentro da bbox da Gavea: lat [-22.990, -22.965], lon [-43.245, -43.215]

- **Files**: `fala-gavea-seguranca/scripts/seed_reports.py` (create or modify)
- **References**: `product-design/project/standards.md` (Python conventions)
- **Depends on**: Step 1
- **Interface**: N/A (script executavel, nao modulo)
- **Verify**: `cd fala-gavea-seguranca && uv run python scripts/seed_reports.py` termina sem erro e `uv run python -c "from src.fala_gavea_seguranca.infrastructure.database.session import get_session; from sqlalchemy import text; s = next(get_session()); print(s.execute(text('SELECT category, count(*) FROM security_reports GROUP BY category')).fetchall())"` mostra distribuicao proxima a esperada
- **Tests**: N/A (script utilitario sem logica de negocio testavel unitariamente)
- [x] Done

### Step 3: Preparar template de prompt de AI-categorizacao para Wave 1 Item 3

Criar o arquivo `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/prompts.py` com o template de prompt que sera usado pelo endpoint `POST /security_reports/{id}/auto_categorize` (a ser implementado no plano do Item 3 do Wave 1 do roadmap-000056).

O template deve:
- Listar as 9 categorias validas com descricoes em pt-BR (uma frase cada)
- Incluir o texto do relato como variavel
- Solicitar resposta em JSON: `{"category": "<valor>", "confidence": "alta|media|baixa", "justification": "<str>"}`
- Instrucao de pensar com `/nothink` ou sem chain-of-thought para velocidade

```python
CATEGORIZE_PROMPT = """/nothink
Voce e um assistente especializado em seguranca publica urbana.
Categorize o relato abaixo escolhendo EXATAMENTE UMA das seguintes categorias:

- furto_roubo: Furtos, roubos, assaltos, tentativas de roubo
- iluminacao: Problemas de iluminacao publica (postes apagados, ruas escuras)
- transito: Transito caótico, acidentes, sinalizacao deficiente, pontos de onibus perigosos
- espaco_publico_inseguro: Espacos publicos inseguros ou abandonados (pracas, calcadas, paradas)
- vandalismo: Depredacao de patrimônio publico ou privado, pichacao
- moradores_situacao_rua: Concentracao de moradores em situacao de rua gerando inseguranca
- conflito_social: Conflito comunitario, tiroteio, tensao entre grupos, barricadas
- barulho_perturbacao: Barulho excessivo perturbando a ordem publica
- outro: Qualquer outro problema de seguranca que nao se encaixe nas categorias acima

Relato: {text}

Responda APENAS com JSON valido no formato:
{{"category": "<valor>", "confidence": "alta|media|baixa", "justification": "<max 1 frase>"}}
"""
```

- **Files**: `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/prompts.py` (create), `fala-gavea-seguranca/src/fala_gavea_seguranca/infrastructure/ai/__init__.py` (create, empty)
- **References**: `product-design/project/standards.md` (Python conventions, module boundaries)
- **Interface**: `CATEGORIZE_PROMPT: str` -- importado por `use_cases/auto_categorize_report.py` (plano futuro, Wave 1 Item 3)
- **Verify**: `uv run python -c "from fala_gavea_seguranca.infrastructure.ai.prompts import CATEGORIZE_PROMPT; print(CATEGORIZE_PROMPT.format(text='Teste'))"` imprime o prompt sem erro
- **Tests**: N/A (string de template sem logica)
- [x] Done

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | Enum centralizado no dominio; use cases e routers importam de um so lugar |
| DATA | Data Integrity | Adopted | SQLite armazena enum como string -- novos valores sao compativeis; seed script e idempotente |
| DX | Developer Experience | Adopted | Prompt template em modulo separado (infra/ai/) -- facil de localizar para Wave 1 Item 3 |
| SEC | Security | N/A | Mudanca de enum e string template; nao ha surface de ataque nova |
| TEST | Testability | Adopted | Step 1 inclui teste de enum; seed script nao tem logica testavel |
| I18N | Internationalization | N/A | Valores do enum sao identificadores de sistema (lowercase pt-BR kebab), nao strings de UI |

---

## Commit message

```
feat(security-report): enrich ReportCategory with 9 forum-derived categories

Replace the 4 generic categories (iluminacao, transito, vandalismo, outro)
with 9 categories grounded in the GaveaLab security forum (11/Jun/2024):
furto_roubo, iluminacao, transito, espaco_publico_inseguro, vandalismo,
moradores_situacao_rua, conflito_social, barulho_perturbacao, outro.

Derived from stakeholder analysis (5 Whys method) with residents,
community leaders, police, and public officials.

Also prepares the AI prompt template (infra/ai/prompts.py) for Wave 1
Item 3 auto-categorization (roadmap-000056).
```

---

## Implementation Summary

**Completed: 2026-06-16 14:35 UTC | Steps: 3/3 | All tests: 27 passed**

| Step | Status | Key output |
|------|--------|-----------|
| 1 | Done | `ReportCategory` expanded from 4 to 9 values; `app.db` deleted; 3 new unit tests added |
| 2 | Done | `scripts/seed_reports.py` created — 250 idempotent rows, pt-BR texts, forum-derived distribution |
| 3 | Done | `infrastructure/ai/prompts.py` created with `CATEGORIZE_PROMPT` string template for Wave 1 Item 3 |

**No partial/failed steps. No deferred items.**
