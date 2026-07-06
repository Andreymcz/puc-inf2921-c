# Research 000089 | FEATURE-X | 2026-07-06 20:02 | Upgrade python-scaffold: BDD, CRUD com relacionamentos, JWT e sementes SEJA
tags: python-scaffold, bdd, jwt-auth, code-generation, security

## User brief (verbatim)

> upgrade clean python scafold, that was implemented no começo do fala-gavea. quero uma skill que faça um scaffold de um projeto clean python orientado a praticas ageis como bdd templates crud de entidade e seus relacionamentos, autenticacao com jwt, além de incluir as boas praticas e constituicao no design seja

## Agent interpretation

Evoluir a skill `/python-scaffold` (v1.0.0 -- script stdlib de 1.022 linhas com templates inline, que gerou o bootstrap do `fala-gavea/` no plan-000072) para uma v2 que gere projetos clean-architecture Python orientados a práticas ágeis:

1. **Múltiplas entidades CRUD com relacionamentos** (hoje: 1 entidade de shape fixo, só o nome é configurável);
2. **Templates BDD** (Gherkin + steps executáveis) -- inexistente hoje em todo o workspace;
3. **Autenticação JWT** com roles -- generalizando o que o fala-gavea construiu à mão depois do scaffold (PyJWT, User entity, register/login, `get_current_user`/`require_role`);
4. **Boas práticas e constituição SEJA** semeadas no projeto gerado (artefatos `product-design/` pré-preenchidos a partir da spec, prontos para `/seja-setup` + `/design`).

A pesquisa avaliou o desenho da v2: formato de entrada (wizard vs spec), framework BDD, escopo de auth, arquitetura de templates e faseamento.

## Files

- `.claude/skills/python-scaffold/SKILL.md` -- skill atual (thin wrapper, v1.0.0)
- `.claude/skills/python-scaffold/scripts/scaffold.py` -- gerador stdlib de 1.022 linhas (render via `string.Template`, linha 42; templates inline linhas 65-984)
- `.claude/skills/python-scaffold/SKILL-quickguide.md` -- contrato atual (1 entidade, 4 use cases CRUD, ~19 testes)
- `_output/plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md` -- registro do bootstrap do fala-gavea via scaffold
- `fala-gavea/src/fala_gavea/infrastructure/auth/jwt_service.py` -- implementação JWT de referência
- `fala-gavea/src/fala_gavea/infrastructure/auth/password_service.py` -- usa bcrypt direto (passlib é peso morto no pyproject)
- `fala-gavea/src/fala_gavea/config.py` -- linha 4: fallback inseguro `"change-me"` que NÃO deve ser generalizado
- `fala-gavea/pyproject.toml` -- linhas 10-11: `pyjwt>=2.8`, `passlib[bcrypt]>=1.7` (vestigial)

## Contexto levantado

- O scaffold atual gera: FastAPI + SQLAlchemy + SQLite + Pydantic v2 + pytest, camadas domain/application/infrastructure/presentation, 4 use cases CRUD, ~12 testes unitários (FakeRepository) + 7 de integração (TestClient). Sem auth, sem BDD, sem relacionamentos.
- O fala-gavea, nascido desse scaffold, cresceu à mão exatamente o que o brief pede de volta na skill: JWT Bearer com roles citizen/agent/admin, entidade User, múltiplas entidades relacionadas (Report -> ReportType FK, Report -> User author FK, Comment, Vote, Forwarding, SavedFilter), use cases em subpacotes por entidade.
- Nenhum projeto do workspace usa BDD hoje (nenhum `.feature`, nenhum pytest-bdd/behave).
- Constituição do projeto: Q1 exige que todos os testes rodem via pytest; Q3 exige type annotations; S1 proíbe segredos em código.

## Q&A log

**Q1 (brief inicial):** upgrade do clean python scaffold implementado no começo do fala-gavea -- skill que faça scaffold de projeto clean python orientado a práticas ágeis: templates BDD, CRUD de entidade e seus relacionamentos, autenticação JWT, incluindo boas práticas e constituição no design SEJA.

**Clarificações (AskUserQuestion):**

- **Q2:** Como declarar múltiplas entidades e relacionamentos? **A2 (usuário):** Wizard interativo (AskUserQuestion).
- **Q3:** Qual abordagem BDD? **A3 (usuário):** pytest-bdd.
- **Q4:** Escopo da autenticação JWT? **A4 (usuário):** Auth opt-in via flag/spec.
- **Q5:** O que significa incluir a constituição SEJA? **A5 (usuário):** Semear `product-design/` no projeto gerado (constitution.md, conventions.md, standards.md pré-preenchidos a partir da spec).

**A1 (resposta consolidada):** ver "Recomendações" abaixo. Síntese: a v2 deve adotar o pipeline wizard -> spec TOML -> gerador determinístico. O wizard (camada SKILL.md) entrevista o usuário e materializa um `scaffold-spec.toml` salvo no projeto gerado; o `scaffold.py` permanece estritamente não-interativo e consome só a spec -- isso preserva a constraint SEJA de não-determinismo, dá trilha de auditoria e permite re-runs reproduzíveis (`--spec` como bypass documentado do wizard). TOML em vez de YAML porque a stdlib do Python não tem parser YAML (`tomllib` é stdlib desde 3.11) e o objetivo de portabilidade zero-dependência deve ser mantido. O trabalho deve ser fatiado em 3-4 plans (fundação multi-entidade -> auth -> BDD -> wizard + sementes SEJA), com golden tests em dois níveis validando o gerador.

## Análise de expert (research-reviewer, depth: deep)

Perspectivas avaliadas: ARCH, SEC, TEST, DX, UX, COMPAT. Achados principais:

| Perspectiva | Veredito | Achado central |
|---|---|---|
| ARCH | Adotar com condições | Pipeline wizard->spec->renderer é o shape certo; spec em TOML (stdlib `tomllib`), não YAML; `string.Template` não tem loops/condicionais -- toda composição fica em Python, templates 100% logic-free |
| SEC | Adotar com condições bloqueantes | Não generalizar o fallback `"change-me"` do fala-gavea (fail-fast se `JWT_SECRET_KEY` ausente); abandonar passlib (não mantido desde ~2020, incompatível com bcrypt>=4.1 e com Python 3.13 -- usa módulo `crypt` removido); validar todo identificador da spec (regex estrita + blacklist de keywords) pois valores da spec viram código-fonte |
| TEST | Adotar com condições | pytest-bdd 8.1.0 maduro, parser gherkin-official, pt-BR nativo via `# language: pt`; gerar BDD como exemplar (1 feature por entidade: happy path + 1 erro), não exaustivo -- cobertura duplicada = manutenção dupla; golden tests em 2 tiers para o próprio gerador |
| DX | Adotar | Refatorar para diretório `templates/` é quase mecânico (constantes `string.Template` já isoladas); manter fast path `--entity Post` funcionando (spec default sintetizada); mensagens de erro da spec nomeando chave e limitação |
| UX | Modificar proposta | Wizard puro para N entidades x campos x relações = 40+ rodadas -> fadiga; mitigar com notação compacta de campos por entidade (`title:str(120), author->User, status:enum(open,closed)`) + preview obrigatório da spec com confirmação antes de escrever + bypass `--spec` de primeira classe |
| COMPAT | Adotar com condições | `spec_version = 1` desde o dia um, rejeitar versões desconhecidas; re-scaffold é one-shot em diretório vazio (recusar diretório não-vazio, sem `--force`) -- merge idempotente em projeto evoluído é outro produto; manter compatibilidade da CLI atual |

Trade-offs resolvidos: determinismo SEC vs SEJA (fail-fast + instrução de geração de segredo no README, sem segredo aleatório no output); riqueza do wizard vs determinismo (fronteira na spec: preview/confirm torna a spec, não a conversa, o contrato); amplitude BDD vs manutenção de templates (exemplares); conveniência de re-run vs perda de dados (one-shot com recusa).

Fontes: pytest-bdd 8.1.0 docs/changelog (parser gherkin-official, localização pt); FastAPI discussion #11773 e tutorial OAuth2-JWT (migração passlib -> pwdlib); pwdlib (François Voron); fastapi-users password-hash config.

## Recomendações

1. **[HIGH] Segurança do template de auth antes de generalizar**: sem fallback `"change-me"` -- `config.py` gerado falha na inicialização se `JWT_SECRET_KEY` não estiver setada; `.env.example` com chave vazia + instrução no README (`python -c "import secrets; print(secrets.token_hex(32))"`); expiry default 60 min (não 24h); `algorithms=["HS256"]` explícito no decode.
2. **[HIGH] bcrypt direto atrás de `PasswordService`, sem passlib** no `pyproject.toml` gerado -- passlib é incompatível com bcrypt>=4.1 e com Python 3.13; o próprio `password_service.py` do fala-gavea já valida o padrão.
3. **[HIGH] Validar todo identificador da spec no load** (regex `^[A-Za-z][A-Za-z0-9_]*$`, blacklist de keywords Python, colisões com nomes reservados como `User` quando `auth = "jwt"`) -- valores da spec são interpolados em código-fonte (vetor de injeção).
4. **[HIGH] Spec em TOML (`tomllib`, stdlib), não YAML**, com `spec_version = 1` e rejeição dura de versões desconhecidas -- mantém a portabilidade zero-dependência do gerador.
5. **[HIGH] Fatiar em 3-4 plans incrementais**: (P1) refactor templates/ + spec loader + multi-entidade 1-N + golden tests; (P2) auth JWT opt-in (com review SEC próprio); (P3) exemplares BDD; (P4) wizard + sementes product-design/. O caminho `--spec` mínimo já sai no P1; o wizard chega no P4 sem bloquear nada.
6. **[MEDIUM] Golden tests em 2 tiers para o gerador**: (tier 1, todo commit) scaffold de 2-3 specs golden versionadas com comparação byte-a-byte da árvore gerada (sem timestamps no output; `newline="\n"` no write para determinismo no Windows); (tier 2, CI lenta) `uv sync && pytest && ruff && pyright` dentro do projeto gerado -- única prova de que o output honra Q1-Q3 da constituição.
7. **[MEDIUM] BDD opt-in como exemplar**: `bdd = true` na spec gera 1 `.feature` pt-BR por entidade (`# language: pt`; happy path + 1 cenário de erro 422/404) com step definitions compartilhadas em `tests/bdd/` -- pytest-bdd 8.1.0 roda dentro do pytest existente (constituição Q1). BDD exaustivo por use case foi considerado e rejeitado (cobertura duplicada, ~3x superfície de template).
8. **[MEDIUM] Wizard com notação compacta + preview/confirm obrigatório + bypass `--spec`**: AskUserQuestion só para escolhas enumeráveis (auth on/off, roles, BDD, tipo de relação); campos por entidade em uma rodada de texto livre com confirmação da interpretação; `scaffold.py` permanece estritamente não-interativo.
9. **[LOW] Relacionamentos v1 limitados a 1-N/N-1**, com mensagem explícita de rejeição para N-N e auto-referência (deferir para `spec_version = 2`).
10. **[LOW] Sementes de design marcadas como rascunho gerado por máquina** pendente de revisão humana (SEJA classifica constitution/design-intent como Human-maintained), cada semente anotada com o template canônico do harness de que deriva (proteção contra drift).

## Decisões de desenho registráveis

- Pipeline wizard -> spec TOML versionada -> gerador determinístico (candidata a D-NNN).
