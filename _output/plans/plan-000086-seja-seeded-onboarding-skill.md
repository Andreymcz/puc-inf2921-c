# Plan 000086 | plan/harness-seja | 2026-07-02 03:06 UTC | Skill /seja-seeded-onboarding (seed + onboard + roteiro de jornadas) | Review: standard
plan_format_version: 1
source: communicate research session (2026-07-01) — pesquisa de artefatos para /seja-seeded-onboarding

## Brief

Criar uma nova skill `seja` empacotável **`/seja-seeded-onboarding`** — artefato acoplado a um
repositório *harness-seja* que acompanha `seja-clean-python` e `seja-kb-qa`. **Escopo completo**:
thin-wrapper (padrão de `/onboard` e `/python-scaffold`) que orquestra 3 fases sobre um repo
seja-seeded já instalado:

1. **SEED** — roda o pipeline showcase idempotente/API-only que popula o app com dados curados
   de demonstração (modelo: fala-gavea `scripts/seed_all.py --profile showcase` / `make seed`,
   plan-000183).
2. **ONBOARD** — gera plano de onboarding personalizado role×level via o agente
   `onboarding-generator`, agora ancorado em dados reais em vez de app vazio (resolve a fricção
   JM-E-001 / JM-TB-001).
3. **GUIDED JOURNEYS** — emite um roteiro guiado de jornadas (padrão research-000085) usando as
   âncoras de jornada e payloads de verificação de `fala-gavea/seeds/relatos/SCHEMA.md`.

Herdar convenções seja: sibling `SKILL-quickguide.md` obrigatório, `compatibility: "Designed for
Claude Code with the SEJA harness"`, reserva de ID via `reserve_id.py`, saída por pasta-data, seed
API-only e idempotente.

## Agent Interpretation

A skill nova é um **orquestrador fino** no padrão consolidado do harness (thin-wrapper → generator
agent — ver `.claude/rules/harness-structure.md`). O ponto não-óbvio: **o pipeline de seed e os
dados de jornada vivem no repo-alvo** (gerado por `seja-clean-python`), não na skill. fala-gavea já
os tem (`scripts/seed_all.py`, `make seed`, `seeds/relatos/SCHEMA.md`). Portanto a skill precisa de
um **contrato de descoberta** — um manifesto por-repo que declara: (a) como semear (comando +
URL default + profile), e (b) as jornadas a roteirizar (âncoras + passos + payloads de verificação).

Escopo deste plano = **autoria do artefato de harness** (skill wrapper + quickguide + generator
agent + contrato de manifesto + docs + registro no inventário), com **fala-gavea como
implementação de referência/validação** (instanciar o manifesto a partir do material já existente
em `SCHEMA.md`). Não altera código de produção de nenhum app.

### Arquitetura da orquestração

```
/seja-seeded-onboarding <role> <level> [name] [--url] [--profile] [--skip-seed]
                        [--journeys-only] [--format]
  │
  ├─ C1 pre-skill
  ├─ Descoberta: localizar o manifesto seeds/journeys.yaml no repo-alvo
  │              (contrato). Se ausente → erro acionável apontando o schema.
  ├─ Fase SEED (salvo --skip-seed / --journeys-only):
  │     invoca o comando de seed declarado (ex.: `make seed URL=<url> PROFILE=showcase`)
  │     idempotente/API-only; se a app não responder em <url> → aviso + oferta de --skip-seed.
  ├─ Fase ONBOARD (salvo --journeys-only):
  │     reserva ID, lança `onboarding-generator` (existente) → plano role×level
  │     ancorado nos dados semeados.
  ├─ Fase JOURNEYS:
  │     lança `seeded-onboarding-generator` (novo) → roteiro guiado de jornadas
  │     a partir das âncoras + payloads de verificação do manifesto.
  ├─ Escreve saídas na pasta-data; monta index se >1 artefato.
  └─ C6 post-skill
```

## Constraints & Conventions

- **Padrão thin-wrapper + generator agent** (`.claude/rules/harness-structure.md`): o SKILL.md
  parseia args, roda pre/post-skill, reserva IDs e apresenta resultados; a geração fica no agente.
- **Sibling `SKILL-quickguide.md` obrigatório**, com blockquote pointer no topo do SKILL.md
  (`harness-governance.md § Sibling SKILL-quickguide.md pattern`).
- **`compatibility: "Designed for Claude Code with the SEJA harness"`** no frontmatter (igual
  a `python-scaffold`/`onboard`/`seja-setup`).
- **Reserva de ID** via `python .claude/skills/scripts/reserve_id.py --type seeded-onboarding
  --title '<slug>'`. `reserve_id.py` aceita `--type` arbitrário (sem validação — verificado), então
  o tipo novo `seeded-onboarding` não exige registro adicional.
- **Seed API-only e idempotente**: a skill **não** acessa DB/Chroma diretamente — apenas invoca o
  comando de seed declarado no manifesto (que por convenção é API-only). Re-execução é segura.
- **Sem caminhos hardcoded / sem URL hardcoded**: `--url` (default `http://localhost:8000`) e o
  comando de seed vêm do manifesto.
- **Generator recebe a constituição do projeto** no prompt (trust boundary — regra de generator
  agents em `harness-structure.md`).
- **Saída UTF-8 sem BOM, ASCII plano** (sem em-dash/curly quotes) nos arquivos gerados; conversão
  HTML opcional via `md_to_html.py` (padrão de `onboarding-generator`).
- **Portabilidade**: skill auto-contida em `.claude/skills/seja-seeded-onboarding/`, copiável para
  qualquer repo SEJA (igual à nota de portabilidade do `python-scaffold`).

## Files

### Created
- `.claude/skills/seja-seeded-onboarding/SKILL.md` — thin-wrapper (parse args, descoberta do
  manifesto, orquestra SEED→ONBOARD→JOURNEYS, pre/post-skill).
- `.claude/skills/seja-seeded-onboarding/SKILL-quickguide.md` — sibling designer-friendly
  (o-que-faz, exemplos, quando usar / não usar, portabilidade).
- `.claude/agents/seeded-onboarding-generator.md` — generator do roteiro guiado de jornadas
  (consome o manifesto: para cada jornada, produz passos + touchpoint + payload de verificação;
  monta o "seeded onboarding packet" ligando estado-do-seed + plano de onboarding + roteiro).
- `.claude/references/general/seeded-onboarding/journey-manifest.md` — **contrato**: schema do
  `seeds/journeys.yaml` (campos `seed`, `app`, `journeys[]` com `persona`/`steps`/`verify`),
  exemplo mínimo, e regras de descoberta/erro.
- `fala-gavea/seeds/journeys.yaml` — **manifesto de referência** instanciado a partir de
  `fala-gavea/seeds/relatos/SCHEMA.md` (§ Âncoras de jornada + Payloads de verificação): jornada
  do agente (worklist ≥10) e do cidadão (8 não-resolvidos + 2 resolvidos), comando `make seed`.

### Modified
- `.claude/rules/harness-structure.md` — incrementar contagem de skills user-facing e de subagent
  prompts (generator); registrar o novo grupo de referências `general/seeded-onboarding/`.
- `.claude/skills/skills-manifest.json` — registrar a skill `seja-seeded-onboarding`.

## Steps

### Step 1: Definir o contrato do manifesto de jornadas
Criar `.claude/references/general/seeded-onboarding/journey-manifest.md` especificando o schema de
`seeds/journeys.yaml` que um repo seja-seeded provê. Campos mínimos:
- `seed:` — `command_template` (uma string de comando única com placeholders `{url}` e `{profile}`,
  ex.: `make seed URL={url} PROFILE={profile}` para repos estilo variável-de-Makefile, ou
  `uv run python scripts/seed_all.py --url {url} --profile {profile}` para repos estilo flag),
  `default_url`, `profiles` (ex.: `showcase`, `full`), `idempotent: true`. A skill substitui
  `{url}`/`{profile}` e roda o resultado **verbatim** — **não** anexa flags fixas `--url`/`--profile`,
  porque os repos-alvo divergem na convenção de argumento (o `make seed` do fala-gavea usa
  `URL=`/`PROFILE=` (variáveis de Make), não flags GNU — verificado em `fala-gavea/CLAUDE.md §
  Build & Run` e plan-000183 Step 7).
- `app:` — `readiness_check` (ex.: `GET /health` ou rota de login) para o guard de "app no ar".
- `journeys:` — lista; cada item: `id`, `persona`, `goal`, `login` (conta semeada), `steps[]`
  (`action`, `touchpoint`), `verify[]` (`request`: método+rota+body; `expect`: descrição do
  resultado esperado — ex.: "≥10 relatos de iluminação não resolvidos").
Incluir um exemplo mínimo e as **regras de descoberta**: procurar `seeds/journeys.yaml` na raiz do
repo-alvo **ou no caminho passado por `--repo <dir>` / `--manifest <path>`**; se ausente → erro
acionável citando este arquivo de schema.
- **Files**: `.claude/references/general/seeded-onboarding/journey-manifest.md` (create)
- **References**: `fala-gavea/seeds/relatos/SCHEMA.md` (§ Âncoras de jornada, § Payloads de
  verificação); `plan-000183` (interface `seed_all.py`/`make seed`).
- **Verify**: o arquivo descreve schema + exemplo + regras de erro; o schema mostra **dois**
  exemplos de `command_template` (variável-de-Make e flag-style); um humano consegue escrever um
  `journeys.yaml` só com ele.

### Step 2: Instanciar o manifesto de referência do fala-gavea
Criar `fala-gavea/seeds/journeys.yaml` conforme o schema do Step 1, transcrevendo o material já
existente em `SCHEMA.md`:
- `seed.command_template: make seed URL={url} PROFILE={profile}`, `default_url:
  http://localhost:8000`, `profiles: [showcase, full]`, `idempotent: true`.
- `app.readiness_check`: login `citizen01@gavea.br` (ou rota equivalente).
- Jornada **agente**: `login: agente@gavea.br`; `verify` = `POST /reports/query` com
  `{report_type_ids:[<Iluminacao publica>], statuses:[pendente,em_analise], since:2026-05-29}`,
  `expect: ">=10 relatos de iluminacao nao resolvidos"`.
- Jornada **cidadão**: `login: citizen01@gavea.br`; `verify` = `GET /reports/{id}/forwardings`
  (forwarding A `solucao_em_andamento`, B `finalizado`); `expect: "meus relatos = 8 nao resolvidos + 2 resolvidos"`.
Não alterar código do fala-gavea — apenas adicionar o YAML declarativo.
- **Files**: `fala-gavea/seeds/journeys.yaml` (create)
- **References**: `fala-gavea/seeds/relatos/SCHEMA.md`; `fala-gavea/CLAUDE.md § Build & Run`.
- **Depends on**: Step 1
- **Verify**: YAML válido; `verify` payloads batem com os documentados em `SCHEMA.md`.

### Step 3: Escrever o generator agent `seeded-onboarding-generator`
Criar `.claude/agents/seeded-onboarding-generator.md` (frontmatter: `name`, `description`,
`designer_description`, `tools: Read, Bash, Glob, Grep, Write`). Entrada: `manifest_path`,
`seed_status` (executado/skip + resumo), `onboarding_output_path` (do onboarding-generator, se
houver), `output_path`, `output_id`, `format`, `project_context` (inclui constituição). Processo:
1. Ler o manifesto e a constituição do projeto.
2. Para cada jornada: renderizar seção com passos numerados (action + touchpoint), a conta de
   login, e um bloco **"Como verificar"** com o payload `verify` e o `expect`.
3. Montar o **Seeded Onboarding Packet**: cabeçalho, resumo do estado do seed, link para o plano de
   onboarding role×level (se gerado), e os roteiros de jornada.
4. Escrever `.md`; se `format` inclui html, rodar `md_to_html.py` (mesmo padrão do
   `onboarding-generator`, incl. `--style` se `communication-style.md` existir).
Regras: UTF-8 sem BOM, ASCII plano, caminhos concretos.
- **Files**: `.claude/agents/seeded-onboarding-generator.md` (create)
- **References**: `.claude/agents/onboarding-generator.md` (padrão de estrutura/escrita);
  `.claude/skills/scripts/md_to_html.py`; roteiro research-000085 (formato de "roteiro guiado").
- **Depends on**: Step 1
- **Verify**: prompt do agente é autossuficiente — descreve entrada, processo, formato de saída e
  regras; espelha o rigor do `onboarding-generator.md`.

### Step 4: Escrever o SKILL.md thin-wrapper
Criar `.claude/skills/seja-seeded-onboarding/SKILL.md` com blockquote pointer para o quickguide no
topo. Frontmatter: `name: seja-seeded-onboarding`, `description`, `argument-hint`,
`compatibility: "Designed for Claude Code with the SEJA harness"`, `metadata` (version, category
`utility`, context_budget). O `SKILL-quickguide.md` **não** entra em `metadata.references` (contrato
de runtime do sibling — `harness-governance.md § Sibling SKILL-quickguide.md pattern`). Corpo:
- **Arguments**: `<role-family>` `<expertise-level>` (aliases igual a `/onboard`), `[name]`,
  `--repo <dir>` / `--manifest <path>` (aponta a descoberta para um repo seja-seeded aninhado),
  `--url`, `--profile showcase|full`, `--skip-seed`, `--journeys-only`, `--format md|html|both`.
- **Instructions**:
  1. Run /pre-skill "seja-seeded-onboarding" $ARGUMENTS (C1).
  2. Resolver role/level (mapeamento de aliases idêntico ao `/onboard`).
  3. **Descoberta**: localizar `seeds/journeys.yaml`. Ordem: (a) caminho explícito via `--manifest
     <path>` / repo-root via `--repo <dir>`, senão (b) `seeds/journeys.yaml` na raiz do repo-alvo
     (CWD ou `--add-dir`). Nota: quando o repo seja-seeded é aninhado (ex.: `fala-gavea/` neste
     monorepo), usar `--repo fala-gavea` ou `--manifest fala-gavea/seeds/journeys.yaml`. Ausente →
     erro acionável citando `general/seeded-onboarding/journey-manifest.md`.
  4. **Fase SEED** (salvo `--skip-seed`/`--journeys-only`): substituir `{url}`/`{profile}` no
     `seed.command_template` do manifesto e executar o resultado **verbatim** (sem anexar flags
     fixas). Antes, rodar o `app.readiness_check`; se falhar → avisar que a app precisa estar no ar
     + Ollama e oferecer `--skip-seed`. Capturar o resumo do estado do seed.
  5. **Fase ONBOARD** (salvo `--journeys-only`): resolver role/level (alias map idêntico ao
     `/onboard`), reservar ID (`--type onboarding`), e lançar `onboarding-generator` (Agent tool,
     `general-purpose`) passando o **contrato completo** do agente (ver `.claude/agents/
     onboarding-generator.md § Input` e `/onboard` step 4): `role_tags`, `level`, `role_file_paths`
     (`.claude/references/general/onboarding/<role>.md`), `level_file_path` (`.claude/references/
     general/onboarding/<level>.md`), `project_context` (product-design-as-coded + conventions),
     `output_path`, `output_id`, `format`, e `name`/`area` se fornecidos. **Nota:** uma invocação
     reserva **dois** IDs — `onboarding` (plano role×level) e `seeded-onboarding` (roteiro de
     jornadas); o Seeded Onboarding Packet liga os dois.
  6. **Fase JOURNEYS**: reservar ID (`--type seeded-onboarding`) e lançar
     `seeded-onboarding-generator` com manifesto + seed_status + caminho do onboarding.
  7. Escrever na pasta-data `${ONBOARDING_PLANS_DIR}/<YYYY-MM-DD>`; se >1 artefato, montar index.
  8. Run /post-skill <id> (C6).
- **Portabilidade / Rationale** curtos (padrão `python-scaffold`).
Aplicar C4 (rationale nas AskUserQuestion de role/level e no guard de app-no-ar).
- **Files**: `.claude/skills/seja-seeded-onboarding/SKILL.md` (create)
- **References**: `.claude/skills/onboard/SKILL.md` (orquestração/args/ID/pasta-data);
  `.claude/skills/python-scaffold/SKILL.md` (forma enxuta/portabilidade); `general/constraints.md`
  (C4 rationale).
- **Depends on**: Step 1, Step 3
- **Verify**: SKILL.md tem o blockquote pointer; frontmatter válido (quickguide fora de
  `references`); as 3 fases e os guards estão descritos; args espelham `/onboard` onde aplicável; a
  lista de inputs passada ao `onboarding-generator` espelha `.claude/agents/onboarding-generator.md
  § Input`.

### Step 5: Escrever o SKILL-quickguide.md sibling
Criar `.claude/skills/seja-seeded-onboarding/SKILL-quickguide.md` no estilo designer-friendly
(igual a `onboard`/`python-scaffold`): **o que faz** (planta dados de demo + gera onboarding +
roteiro guiado de jornadas), tabela de roles/levels, **exemplos** (`/seja-seeded-onboarding builder
L1 --url http://localhost:8000`; `... --journeys-only`; `... --skip-seed`), **quando usar / não
usar** (não é para stakeholder update → `/communicate`; não substitui `/onboard` puro em repo sem
seed), nota de **portabilidade** e ponteiro para o contrato do manifesto.
- **Files**: `.claude/skills/seja-seeded-onboarding/SKILL-quickguide.md` (create)
- **References**: `.claude/skills/onboard/SKILL-quickguide.md`,
  `.claude/skills/python-scaffold/SKILL-quickguide.md` (forma/tom).
- **Depends on**: Step 4
- **Verify**: cobre o-que-faz, exemplos, quando-usar/não-usar, portabilidade, referências.

### Step 6: Registrar no inventário do harness
Atualizar `.claude/rules/harness-structure.md`: incrementar a contagem de skills user-facing e a
descrição da lista de skills (adicionar `/seja-seeded-onboarding` como orquestrador seed+onboard+
roteiro); incrementar a contagem de subagent prompts / generator agents (adicionar
`seeded-onboarding-generator`); registrar o grupo de referências `general/seeded-onboarding/`.
Registrar a skill em `.claude/skills/skills-manifest.json`: **incrementar `"count"` (15 → 16)**,
atualizar `"generated"`, e acrescentar a entrada `seja-seeded-onboarding` (mesma forma das
existentes: `name`, `description`, `argument_hint`, `category: utility`, `version`).
- **Files**: `.claude/rules/harness-structure.md` (modify), `.claude/skills/skills-manifest.json` (modify)
- **References**: entradas existentes de `onboard`/`python-scaffold` no manifesto e no inventário.
- **Depends on**: Step 4, Step 3
- **Verify**: contagens e listas consistentes; `skills-manifest.json` continua JSON válido
  (parse OK); `"count"` == número de entradas em `skills[]` (16); a nova entrada aparece.

### Step 7: Validação end-to-end (seco) + docs
Validar a coerência do artefato sem exigir app/Ollama no ar:
- Conferir que o `seeds/journeys.yaml` do fala-gavea parseia e que seus `verify` payloads batem com
  `SCHEMA.md`.
- Dry-check da skill: percorrer as instruções contra o manifesto de referência e confirmar que cada
  fase tem entrada resolvível (descoberta → seed.command_template → onboarding-generator → journeys);
  confirmar que a substituição de `{url}`/`{profile}` no `command_template` do fala-gavea produz um
  comando bem-formado (`make seed URL=http://localhost:8000 PROFILE=showcase`).
- Rodar os linters de convenção do harness disponíveis (ex.: `python
  .claude/skills/scripts/run_all_checks.py` ou o checker de docs/skills, se presentes) e o
  `check_secrets.py` sobre os arquivos novos.
Documentar a skill onde o repo lista skills (se aplicável). A execução real do seed (`make seed`
com API+Ollama) e a captura de prints das jornadas ficam como **verificação manual de follow-up**
(precisam de servidor local), consistente com plan-000183.
- **Files**: (nenhum de produção) — apenas validação; ajustes pontuais se um linter apontar.
- **References**: `.claude/skills/scripts/` (checkers), `plan-000183 § Implementation Summary`
  (precedente de "seed vivo é follow-up manual").
- **Depends on**: Step 2, Step 4, Step 5, Step 6
- **Verify**: linters de convenção passam sobre os arquivos novos; YAML válido; sem segredos.
- **Tests**: N/A — artefato de harness (SKILL/agent/ref/manifesto); coberto pelos checkers de
  convenção e pela verificação manual do seed vivo (follow-up).

## Suggestions — fora de escopo (para depois)

1. **`seja-clean-python` emite `seeds/journeys.yaml`** ao gerar um app, para que todo repo
   seja-seeded já nasça com o contrato — fecha o loop da família de artefatos.
2. **Modo `--all`/batch** (como `/onboard`) para gerar pacotes de múltiplos role×level de uma vez.
3. **Captura automática de prints** das jornadas (Playwright/headless) para materializar o roteiro
   guiado como galeria — evolução do research-000085.
4. **Guard de "seed já aplicado"**: detectar dados existentes e pular o seed sem `--skip-seed`.

## Review (standard)

- **Depth:** auto=standard (novo artefato de harness multi-arquivo, sensível à governança, com
  acoplamento cross-repo ao fala-gavea), floor=light, flag=none → **effective=standard**.
- **Fronteira de escopo:** o seed vive no repo-alvo; a skill só o invoca via contrato — evita
  duplicar o pipeline e mantém API-only/idempotência no lado do app. ✅
- **Reuso:** ONBOARD reaproveita o `onboarding-generator` existente em vez de reimplementar. ✅
- **Trust boundary:** generator recebe a constituição; seed é API-only (sem DB direto). ✅
- **Risco:** divergência entre `journeys.yaml` e o `SCHEMA.md`/estado real do app — mitigado pelo
  Step 7 (checagem dos payloads) e pela verificação manual do seed vivo.
- **Risco:** contagens/inventário do harness ficarem dessincronizados — Step 6 atualiza
  `harness-structure.md` + `skills-manifest.json` (incl. `count` 15→16) explicitamente.
- **Plan review (standard, plan-reviewer):** 6 perspectivas shortlisted (DX, ARCH, COMPAT, API,
  SEC, DATA); 3 Adopted, 3 deep-dived e resolvidas via emendas aditivas; sem conflitos, sem
  regressão de segurança/privacidade. Emendas aplicadas: (1) `seed.command_template` com
  placeholders `{url}`/`{profile}` — `make seed` usa `URL=`/`PROFILE=`, não flags; (2) Step 4
  enumera o contrato completo de input do `onboarding-generator` + nota de dois-IDs; (3) args
  `--repo`/`--manifest` para repo aninhado (fala-gavea); (4) Step 6 bump de `count` no
  `skills-manifest.json` + quickguide fora de `references`.

## Brief Traceability

- "thin-wrapper que orquestra 3 fases" → Steps 3–5 (wrapper + generator) + Arquitetura da orquestração.
- "SEED idempotente/API-only (make seed / seed_all.py)" → Step 4 Fase SEED + contrato Step 1.
- "ONBOARD role×level via onboarding-generator" → Step 4 Fase ONBOARD (reuso do agente existente).
- "GUIDED JOURNEYS (research-000085) via âncoras + payloads de SCHEMA.md" → Steps 2–3 + Fase JOURNEYS.
- "convenções seja (sibling quickguide, compatibility, reserve_id, pasta-data)" → Steps 4–6 + Constraints.
- "artefato acoplado a harness-seja junto de seja-clean-python/seja-kb-qa" → Step 6 (registro) +
  Suggestion 1 (emissão pelo seja-clean-python).
