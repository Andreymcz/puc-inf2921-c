# Plan 000092 | FEATURE-O | 2026-07-06 20:25 | python-scaffold v2 P1: templates/, spec TOML, multi-entidade 1-N, golden tests | Review: standard
plan_format_version: 1

source: research-000089 -- fundacao da v2 do python-scaffold (recs HIGH 3, 4, 5 e MEDIUM 6)

## Brief (verbatim)

> source: research-000089 -- python-scaffold v2 P1 (fundacao): refatorar scaffold.py em templates/ + renderer stdlib logic-free; spec loader TOML (tomllib, spec_version=1, validacao estrita de identificadores como vetor de injecao, rejeicao de versoes/relacoes desconhecidas); suporte multi-entidade com relacionamentos 1-N/N-1; caminho --spec nao-interativo (wizard fica para P4); recusa de diretorio destino nao-vazio; fast path --entity retrocompativel via spec default sintetizada; golden tests em 2 tiers (comparacao byte-a-byte de arvores golden por commit + uv sync/pytest/ruff/pyright do projeto gerado em CI lenta; sem timestamps no output, newline="\n")

## Context

A skill `/python-scaffold` v1.0.0 e um script stdlib unico (`scripts/scaffold.py`, 1.022 linhas) com ~30 templates inline `string.Template` (linhas 65-984) atras de `render()` (linha 42). Gera 1 entidade de shape fixo (nome configuravel via `--entity`), 4 use cases CRUD, ~19 testes. O fala-gavea nasceu desse scaffold (plan-000072) e evoluiu a mao o que a v2 quer generalizar.

Este plan e o P1 de 4 (research-000089 rec 5): fundacao determinista sobre a qual auth JWT (P2), BDD (P3) e wizard + sementes SEJA (P4) serao construidos. Decisao de arquitetura registrada em D-006 (product-design-as-intended.md): wizard -> spec TOML -> gerador deterministico; `scaffold.py` permanece estritamente nao-interativo (nunca pergunta, nunca le env, nunca acessa rede).

Restricoes herdadas da pesquisa:
- Spec em TOML (`tomllib` e stdlib desde 3.11; stdlib nao tem parser YAML) com `spec_version = 1` obrigatorio; versoes desconhecidas rejeitadas.
- Identificadores da spec sao interpolados em codigo-fonte gerado -> validacao estrita e P0 de seguranca (rec 3).
- Relacionamentos v1: apenas many-to-one (N-1) declarado no lado N; one-to-many e o reverso implicito. N-N e auto-referencia rejeitados com mensagem explicita (rec 9).
- Templates 100% logic-free: todo controle de fluxo (loops por entidade, slots condicionais) vive em Python; nenhum mini-syntax `{% if %}` (guardrail ARCH da pesquisa).
- One-shot: recusar diretorio destino nao-vazio; sem `--force`.
- Determinismo de output: sem timestamps; `newline="\n"` em todo write (golden tests byte-a-byte no Windows).

## Steps

### Step 1: Extrair templates inline para `templates/` (logic-free)

Criar `.claude/skills/python-scaffold/templates/` e mover cada constante `string.Template` de `scaffold.py` para um arquivo proprio, preservando o conteudo e a sintaxe `${placeholder}`:

```
templates/
  project/        pyproject.toml.tmpl, README.md.tmpl, gitignore.tmpl, env.example.tmpl, config.py.tmpl
  domain/         exceptions.py.tmpl, entity.py.tmpl, repository.py.tmpl
  application/    create.py.tmpl, get.py.tmpl, list.py.tmpl, delete.py.tmpl
  infrastructure/ session.py.tmpl, models_header.py.tmpl, model_class.py.tmpl, sqlalchemy_repository.py.tmpl
  presentation/   schemas.py.tmpl, dependencies.py.tmpl, router.py.tmpl, main.py.tmpl
  tests/          conftest.py.tmpl, fake_repository.py.tmpl, test_unit.py.tmpl, test_integration.py.tmpl
```

Fragmentos multi-entidade (ex.: `model_class.py.tmpl`, imports/registro de routers em `main.py.tmpl`) usam slots nomeados `${...}` preenchidos por concatenacao em Python -- nunca condicional/loop dentro do template. Adicionar em `scripts/renderer.py`: `load_template(rel: str) -> str` (resolve relativo a `templates/`, cache simples em dict) e mover `render()` e `write_file()` para la, com `write_file` passando `newline="\n"` explicito.

Convencao de escape (review A5): `render()` mantem `Template.substitute` estrito (falha alto em placeholder desconhecido ou padrao `$` invalido -- inclusive `$1`, que levanta ValueError em tempo de render); `$` literal no output (exemplos shell, Makefile) escreve-se `$$`. Convencao documentada no docstring de `renderer.py`.

- **Files**: `.claude/skills/python-scaffold/templates/**` (create, ~22 arquivos); `.claude/skills/python-scaffold/scripts/renderer.py` (create); `.claude/skills/python-scaffold/scripts/scaffold.py` (modify -- remove constantes inline, importa renderer)
- **References**: `scaffold.py` linhas 42-50 (render/write_file atuais), 65-984 (constantes)
- **Interface**: `load_template(rel: str) -> str`; `render(template: str, ctx: dict[str, str]) -> str`; `write_file(base: Path, rel: str, content: str) -> None`
- **Verify**: `uv run python .claude/skills/python-scaffold/scripts/scaffold.py --name tmp-smoke --output <tmpdir> --entity Post` gera a mesma arvore de arquivos que a v1 (mesmo conjunto de paths; conteudo equivalente)
- **Tests**: cobertos pelo Step 6 (golden tier 1)
- **Docs**: N/A (Step 8 consolida)
- [ ] Done

### Step 2: Spec loader TOML com validacao estrita (`spec.py`)

Criar `scripts/spec.py` (stdlib only: `tomllib`, `dataclasses`, `keyword`, `re`):

- Dataclasses frozen: `Spec(spec_version, project, entities)`, `EntitySpec(name, fields, relations)`, `FieldSpec(name, type, enum_values)`, `RelationSpec(name, target, kind)`.
- `load_spec(path: Path) -> Spec` parseia TOML e valida; toda falha levanta `SpecError` com mensagem nomeando a chave (`entities[2].relations[0].kind: "many-to-many" nao suportado em spec_version 1; suportado: many-to-one`).
- Validacoes (ordem): `spec_version == 1` (rejeicao dura de ausente/desconhecida); `project` em kebab-case (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`); nomes de entidade PascalCase `^[A-Z][A-Za-z0-9]*$`; nomes de campo/relacao snake_case `^[a-z][a-z0-9_]*$`; rejeitar keywords e soft keywords Python (`keyword.kwlist + keyword.softkwlist`) em qualquer identificador; tipos de campo permitidos: `str | text | int | float | bool | datetime | enum` (enum exige `values = [...]`, cada valor snake_case); relacoes: `kind = "many-to-one"` apenas, `target` deve ser entidade declarada na spec, auto-referencia (`target == entity.name`) rejeitada com mensagem propria; nome reservado: entidade `User` rejeitada com mensagem "reservado para auth (P2)" (evita colisao futura, decisao explicita da pesquisa).
- Validacoes de colisao (review A1 -- fecham o guard de injecao contra sobrescrita silenciosa):
  - Campos/relacoes `id` e `created_at` rejeitados (colunas injetadas pelo gerador), mensagem nomeando o identificador reservado.
  - Duplicatas por entidade verificadas sobre o conjunto de atributos EFETIVO: campos declarados UNIAO {`<relacao>_id`} UNIAO {`id`, `created_at`} -- pega campo escalar `report_type_id` coexistindo com relacao `report_type`.
  - Unicidade entre entidades sobre o conjunto de nomes DERIVADOS, nao so o PascalCase: `camel_to_snake(name)` e o plural/nome de tabela (`HTTPServer` vs `HttpServer` -> ambos `http_server`; snake de `Reports` == plural de `Report`). Mensagem nomeia as duas entidades em colisao.
- Formato TOML (documentado em docstring + Step 8):

```toml
spec_version = 1
project = "fala-gavea"

[[entities]]
name = "ReportType"
[[entities.fields]]
name = "name"
type = "str"

[[entities]]
name = "Report"
[[entities.fields]]
name = "text"
type = "text"
[[entities.fields]]
name = "urgency"
type = "enum"
values = ["low", "medium", "high"]
[[entities.relations]]
name = "report_type"
target = "ReportType"
kind = "many-to-one"
```

- **Files**: `.claude/skills/python-scaffold/scripts/spec.py` (create)
- **References**: research-000089 recs 3, 4, 9; D-006
- **Interface**: `load_spec(path: Path) -> Spec`; `dump_spec(spec: Spec) -> str` (serializador TOML minimo hand-rolled -- `tomllib` nao escreve; NAO adicionar `tomli-w`); `class SpecError(ValueError)`; `default_spec(project: str, entity: str) -> Spec` (fast path do Step 4)
- **Verify**: REPL: `load_spec` aceita a spec exemplo acima; rejeita `spec_version = 2`, campo `class`, campo `id`, relacao `many-to-many`, entidade `User`, auto-referencia, `HTTPServer`+`HttpServer`
- **Tests**: `tests/test_spec.py` -- casos de aceite + todos os caminhos de rejeicao listados, incluindo 1 caso por regra de colisao do review A1 (1 assert de mensagem por regra) + round-trip `load_spec(dump_spec(s)) == s` (review A6)
- **Docs**: N/A (Step 8)
- [ ] Done

### Step 3: Geracao multi-entidade dirigida pela spec

Reescrever o miolo de `scaffold.py` para iterar `spec.entities`:

- **Por entidade**: `domain/entities/<snake>.py` (dataclass com campos tipados da spec; enums viram `class <Name><Field>(str, Enum)` no mesmo modulo; relacoes N-1 viram campo `<rel>_id: str`), `domain/repositories/<snake>_repository.py`, 4 use cases em `application/use_cases/<snake>/` (subpacote por entidade, padrao fala-gavea), `infrastructure/repositories/sqlalchemy_<snake>_repository.py`, `presentation/schemas/<snake>_schemas.py` (Create/Response com os campos da spec; FKs como `<rel>_id: str`), `presentation/api/routers/<plural>.py`.
- **Compartilhados**: `domain/exceptions.py` (DomainError + `<Entity>NotFoundError` por entidade + InvalidInputError), `infrastructure/database/models.py` (um `<Entity>Model` por entidade; N-1 vira `Column(String, ForeignKey("<target_table>.id"), nullable=False, index=True)`; enum vira `Column(SAEnum(...))`), `main.py` (registra todos os routers), `dependencies.py` (um provider de repo por entidade), `conftest.py`.
- Mapa de tipos spec->Python->SQLAlchemy->Pydantic centralizado em `TYPE_MAP` no `scaffold.py` (nao nos templates).
- Ordem de geracao/registro: ordem de declaracao na spec (determinismo); validacao de FK em POST (target inexistente -> 404 do target) fica FORA do P1 -- rota create aceita o id e confia no NOT NULL/FK do SQLite (documentar no README gerado como limitacao conhecida).
- Testes gerados por entidade: mesmos ~12 unit + 7 integration da v1, parametrizados pelos campos da spec (payload de exemplo deterministico derivado do tipo: `"exemplo"`, `1`, `1.5`, `true`, primeiro valor do enum; FK preenchida criando o target antes no teste de integracao).

- **Files**: `.claude/skills/python-scaffold/scripts/scaffold.py` (modify -- núcleo multi-entidade); `.claude/skills/python-scaffold/templates/**` (modify -- placeholders por-entidade onde necessario)
- **References**: Step 1 (templates), Step 2 (Spec); `fala-gavea/src/fala_gavea/` como padrao de referencia (use cases em subpacote, FK em models)
- **Interface**: `scaffold(spec: Spec, output: Path) -> Path` (substitui a assinatura atual baseada em argparse; `main()` faz o parsing)
- **Verify**: scaffold da spec exemplo do Step 2 -> `uv sync && uv run pytest -v` no projeto gerado passa 100%; `uv run ruff check src/` e `uv run pyright src/` limpos
- **Tests**: cobertos por Steps 6-7
- **Docs**: N/A (Step 8)
- [ ] Done

### Step 4: CLI -- `--spec`, fast path retrocompativel e recusa de destino nao-vazio

- `parse_args`: novo `--spec <path>` (mutuamente exclusivo com `--entity`); `--name` continua obrigatorio sem `--spec` (com `--spec`, `project` vem da spec e `--name` e rejeitado se divergir).
- Fast path: `--entity Post` (ou default) chama `default_spec(name, entity)` reproduzindo o shape v1 (text, territory_level enum, territory_name, author_id, ai_labels/label_feedback/likes_count NAO entram -- ver nota) e segue o mesmo caminho de geracao. Nota: o shape v1 tem campos especificos de CitizenPost (ai_labels, likes_count); a default_spec v2 gera um shape generico `text: text` + `author_id: str` apenas, e o SKILL.md documenta a mudanca (v1 -> v2 nao e byte-compativel; e uma major da skill).
- One-shot: se `<output>/<project>/` existe e nao esta vazio, abortar com exit 2 e mensagem `target directory not empty: <path> (one-shot scaffold; choose a new directory)`. Sem `--force`.
- Apos gerar, escrever a spec efetiva (inclusive a sintetizada pelo fast path) em `<project>/scaffold-spec.toml` -- trilha de auditoria e input de re-run (D-006). Emissao deterministica (review A6): com `--spec`, copiar os bytes do arquivo de entrada verbatim; no fast path, serializar via `dump_spec()` (Step 2). Determinismo importa: o arquivo fica dentro da arvore comparada pelos golden tests.

- **Files**: `.claude/skills/python-scaffold/scripts/scaffold.py` (modify -- parse_args/main)
- **References**: D-006 (one-shot, spec como contrato)
- **Interface**: CLI: `scaffold.py (--spec PATH | --name NAME [--entity ENTITY]) [--output DIR]`
- **Verify**: (a) `--spec` da spec exemplo gera projeto; (b) fast path `--name x --entity Post` gera projeto generico; (c) segunda execucao no mesmo destino aborta com exit 2; (d) `scaffold-spec.toml` presente e re-parseavel por `load_spec`
- **Tests**: `tests/test_cli.py` -- os 4 casos do Verify via subprocess/`tmp_path`
- **Docs**: N/A (Step 8)
- [ ] Done

### Step 5: Determinismo de output

Auditar templates e geracao: nenhum timestamp/versao dinamica no output; iteracao sempre em ordem de declaracao da spec; `write_file` com `encoding="utf-8"`, `newline="\n"`; nomes de arquivo e conteudo identicos entre execucoes e plataformas (Windows/Linux); scan de `templates/**` por `$` literal nao-escapado (deve ser `$$` -- review A5).

- **Files**: `.claude/skills/python-scaffold/scripts/renderer.py` (verify/modify); `.claude/skills/python-scaffold/templates/**` (verify)
- **References**: research-000089 rec 6 (pre-requisitos dos golden tests)
- **Interface**: N/A
- **Verify**: duas execucoes consecutivas do mesmo comando em diretorios distintos -> `diff -r` vazio
- **Tests**: assert de igualdade de arvores no `tests/test_golden.py` (Step 6) cobre isso permanentemente
- **Docs**: N/A
- [ ] Done

### Step 6: Golden tests tier 1 (byte-a-byte, todo commit)

Criar `.claude/skills/python-scaffold/tests/`:

- `specs/minimal.toml` (1 entidade, sem relacoes) e `specs/multi.toml` (3 entidades, 2 relacoes N-1, 1 enum -- a spec exemplo do Step 2).
- `golden/minimal/**` e `golden/multi/**`: arvores geradas uma vez no implement e commitadas (`.gitattributes` local com `* -text` para blindar contra autocrlf).
- `test_golden.py`: para cada spec, scaffolda em `tmp_path` e compara arvore golden (conjunto de paths identico + `filecmp`/bytes identicos por arquivo; diff de paths divergentes na mensagem de falha).
- `test_spec.py` e `test_cli.py` (Steps 2 e 4) vivem no mesmo pacote de testes.
- `pytest.ini` DENTRO de `.claude/skills/python-scaffold/tests/` com `markers = slow` e `addopts = -m "not slow"` (review A2): o `pyproject.toml` da raiz define `testpaths = ["tests"]` sem markers, e sem um config file local que venca a resolucao de rootdir nao existe "addopts local"; registrar o marker so no conftest nao cobre o addopts. `-m slow` na CLI sobrescreve o addopts (ultimo `-m` vence).
- `regen_golden.py` (review A2): re-scaffolda `specs/*.toml` para dentro de `golden/`; regra documentada: arvores regeneradas sao revisadas via `git diff` antes do commit. E o caminho de manutencao para toda mudanca de template (inclusive P2-P4).
- Runner: `uv run pytest .claude/skills/python-scaffold/tests -v` a partir da raiz do repo (documentar no SKILL.md; nao integra o pytest do produto).

- **Files**: `.claude/skills/python-scaffold/tests/` (create -- specs/, golden/, test_golden.py, test_spec.py, test_cli.py, conftest.py, pytest.ini, regen_golden.py, .gitattributes)
- **References**: research-000089 rec 6
- **Interface**: N/A
- **Verify**: `uv run pytest .claude/skills/python-scaffold/tests -v` passa; alterar 1 byte num template quebra `test_golden.py`
- **Tests**: este step E os testes
- **Docs**: N/A (Step 8)
- [ ] Done

### Step 7: Golden tier 2 (validacao lenta do projeto gerado)

`tests/test_generated_project.py` marcado `@pytest.mark.slow` (marker registrado no `pytest.ini` do Step 6): scaffolda `specs/multi.toml` em `tmp_path` e roda `uv sync --extra dev`, `uv run pytest -v`, `uv run ruff check src/`, `uv run pyright src/` via subprocess, falhando com o stdout/stderr da etapa que quebrar. Excluido do run default pelo `addopts = -m "not slow"` do `pytest.ini`; invocado explicitamente com `-m slow` (unica prova de que o output honra a constituicao Q1-Q3 do projeto gerado).

Higiene de ambiente dos subprocessos (review A3): rodar com `cwd=<projeto gerado>` e env copiado SEM `VIRTUAL_ENV` e `UV_PROJECT_ENVIRONMENT`, para que `uv sync`/`uv run` dentro do `tmp_path` nunca resolvam contra o `.venv` do repo (no Windows, `uv run pytest` exporta `VIRTUAL_ENV` para filhos; o uv atual apenas avisa, mas o warning polui o output de falha e o comportamento e sensivel a versao).

- **Files**: `.claude/skills/python-scaffold/tests/test_generated_project.py` (create); `.claude/skills/python-scaffold/tests/conftest.py` (modify -- marker)
- **References**: research-000089 rec 6 tier 2
- **Interface**: N/A
- **Verify**: `uv run pytest .claude/skills/python-scaffold/tests -m slow -v` passa de ponta a ponta (requer rede para uv sync na primeira execucao)
- **Tests**: este step E o teste
- **Docs**: N/A (Step 8)
- [ ] Done

### Step 8: Atualizar SKILL.md e SKILL-quickguide.md

- `SKILL.md`: versao 2.0.0 (review A4 -- o proprio Step 4 declara a mudanca do fast path uma major; era 1.0.0) + `metadata.last-updated` + `argument-hint` incluindo `--spec`; argumentos `--spec` (novo, recomendado) e `--entity` (fast path, shape generico v2); instrucao para o agente montar a spec TOML a partir do pedido do usuario quando nao houver arquivo (precursor manual do wizard P4); passo de verificacao pos-geracao (`uv run pytest` no projeto gerado); nota one-shot.
- `SKILL-quickguide.md`: nova arvore gerada (multi-entidade), schema TOML completo com exemplo de relacao e enum, secao "Limitacoes v1 da spec" (N-1 apenas; sem N-N/auto-referencia; `User` reservado para P2-auth; validacao de FK em runtime fica no SQLite), roadmap P2-P4 em uma linha, instrucao dos golden tests.

- **Files**: `.claude/skills/python-scaffold/SKILL.md` (modify); `.claude/skills/python-scaffold/SKILL-quickguide.md` (modify)
- **References**: Steps 2, 4; research-000089 recs 5, 9
- **Interface**: N/A
- **Verify**: leitura -- args e exemplos consistentes com o comportamento implementado
- **Tests**: N/A
- **Docs**: SKILL.md + SKILL-quickguide.md sao a documentacao da skill (este step)
- [ ] Done

## Test plan

1. `uv run pytest .claude/skills/python-scaffold/tests -v` -- spec loader (aceite + todas as rejeicoes), CLI (4 casos), golden byte-a-byte (minimal + multi).
2. `uv run pytest .claude/skills/python-scaffold/tests -m slow -v` -- projeto gerado da spec multi passa `uv sync`, `pytest`, `ruff`, `pyright`.
3. Manual: `/python-scaffold demo-blog --entity Post` (fast path) -> `cd demo-blog && uv sync && uv run pytest -v` 100%; segunda invocacao no mesmo destino aborta.

## Review log

plan-reviewer (depth: standard, 6 perspectivas: SEC/ARCH/TEST/PERF/DX/COMPAT; DB/API/OPS/DATA/I18N/UX N/A). Todas convergiram para Adopted apos 6 amendments aplicados aos steps:

- A1 (SEC): validacao sobre conjunto de atributos efetivo (`id`/`created_at` reservados; relacao+`_id` vs campo escalar; unicidade cross-entidade de nomes derivados snake/plural) -- Step 2.
- A2 (TEST/DX): `pytest.ini` local para rootdir/markers/addopts (o `pyproject.toml` da raiz venceria sem ele) + `regen_golden.py` como caminho de manutencao -- Step 6.
- A3 (TEST): subprocessos tier-2 com env sem `VIRTUAL_ENV`/`UV_PROJECT_ENVIRONMENT` -- Step 7.
- A4 (COMPAT): versao da skill 2.0.0, nao 1.1.0 -- Step 8.
- A5 (COMPAT): convencao `$$` para `$` literal + substitute estrito documentado no renderer + scan no audit -- Steps 1 e 5.
- A6 (COMPAT): emissao deterministica de `scaffold-spec.toml` (copia verbatim para `--spec`; `dump_spec()` hand-rolled para fast path; round-trip test) -- Steps 2 e 4.

## Out of scope (P2-P4, research-000089 rec 5)

- P2: auth JWT opt-in (`auth = "jwt"` na spec; User entity, register/login, JWTService com fail-fast de secret, bcrypt direto sem passlib, expiry 60min, `algorithms=["HS256"]`).
- P3: BDD exemplar (`bdd = true`; 1 `.feature` pt-BR por entidade via pytest-bdd 8.x).
- P4: wizard AskUserQuestion na camada SKILL.md + sementes `product-design/` no projeto gerado.
- N-N, auto-referencia, validacao de FK na rota create, export/merge idempotente.
