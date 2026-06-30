# Plan 000076 | plan/fala-gavea | 2026-06-22 11:53 UTC | Reescrever PROMPT-gerar-seed com fontes Herbert embutidas | Review: light
plan_format_version: 1

## Brief

Baseado em `knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt` e
`knowledge/RELATOS_HERBERT.txt`, reescrever o prompt gerador de CSV de seed de
relatos do **fala-gavea**, usando o `PROMPT-gerar-seed.md` atual como baseline de
formato de arquivo. O novo prompt deve ser **auto-contido** (conteúdo Herbert
embutido) e **substituir** o baseline existente.

## Decisões confirmadas (AskUserQuestion)

- **Fonte Herbert → Embutir no prompt.** O material dos dois `.txt` é destilado e
  colado dentro do próprio prompt como banco de relatos-fonte + cenários de uso.
  Resultado: prompt funciona em qualquer LLM sem depender de acesso ao repo pai
  (`inf2921-grupo-c/knowledge/` não está dentro de `fala-gavea/`).
- **Destino → Substituir o baseline.** Reescrever
  `fala-gavea/seeds/relatos/PROMPT-gerar-seed.md` no lugar. Os sample CSVs hoje
  referenciados (`data/sample-gavealab.csv`, `data/sample-gavealab-diagnostico.csv`)
  não existem no repo (só `data/fake-sample-gavealab.csv`), então a substituição
  também corrige fontes quebradas.

## Contexto verificado

- **Endpoint alvo** `POST /admin/seed/relatos` em
  [fala-gavea/src/fala_gavea/presentation/api/routers/seed.py](fala-gavea/src/fala_gavea/presentation/api/routers/seed.py#L59-L68)
  lê exatamente estas colunas via `csv.DictReader`:
  `user_id` (ou alias `id_cidadao`), `texto_relato`, `latitude`, `longitude`,
  `data`, `topico`, `urgency`. Só `user_id`/`id_cidadao` é obrigatório; as demais
  têm fallback. → O cabeçalho de 7 colunas do baseline está **correto** e deve ser
  preservado literalmente.
- **Tópicos válidos** (de [SCHEMA.md](fala-gavea/seeds/relatos/SCHEMA.md#L17-L21)):
  `Iluminacao publica`, `Transito e mobilidade`, `Vandalismo`, `Espaco publico`,
  `Lixo e conservacao`, `Seguranca e circulacao`, `Conflito social`, `Outro`
  (sem acento — texto idêntico ao banco).
- **Bounding box Gávea**: lat -22.975 … -22.953 | lon -43.235 … -43.205.
- **Intervalo de datas**: 2025-06-18 … 2026-06-18.
- **Fontes Herbert** mapeiam quase 1:1 nos tópicos do SCHEMA:

  | Seção em RELATOS_HERBERT.txt | Tópico SCHEMA |
  |---|---|
  | 1. Iluminação pública, postes apagados | `Iluminacao publica` |
  | 2. Trânsito e mobilidade, sinalização, transporte | `Transito e mobilidade` |
  | 3. Conflito social, perturbação da ordem | `Conflito social` |
  | 4. Lixo e conservação, entulho, limpeza | `Lixo e conservacao` |
  | 5. Espaço público, calçadas, praças, parques | `Espaco publico` |
  | 6. Vandalismo, depredação de patrimônio | `Vandalismo` |
  | 7. Segurança e circulação, pontos de risco | `Seguranca e circulacao` |

  `CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt` traz 14 casos de uso de agentes
  públicos (iluminação, mobilidade, segurança viária, mulher/DH, saúde, assistência
  social, meio ambiente) — usados como **lentes de consequência** para enriquecer
  o `texto_relato` (ex.: relato de iluminação → evasão escolar EJA; lixo → leptospirose).

## Estratégia do novo prompt

Estrutura do `PROMPT-gerar-seed.md` reescrito (mantendo o estilo do baseline):

1. **Cabeçalho / preâmbulo** — explica que o CSV é importável por
   `POST /admin/seed/relatos`, card "Seed de Relatos"; `user_id` canônico, `id_cidadao`
   como alias.
2. **`## Banco de relatos-fonte (Herbert)`** — bloco embutido com o **texto integral
   e literal** de `RELATOS_HERBERT.txt`, copiado exatamente como foi escrito (mantém
   o agrupamento original pelos 7 tópicos). **Sem destilar, resumir ou parafrasear** —
   o texto inteiro entra como anexo de referência. Instrução ao modelo: gerar relatos
   *parecidos* com estes (mesmo tema/voz/tom), não cópias.
3. **`## Cenários de agentes públicos`** — bloco embutido com o **texto integral e
   literal** de `CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt` (os 14 casos de uso
   na íntegra). Instrução ao modelo: usar esses cenários para **enriquecer** os
   relatos gerados, conectando cada um à consequência concreta que o agente público
   correspondente buscaria enxergar (ex.: iluminação → evasão escolar EJA; lixo →
   leptospirose; conflito → saúde mental).
4. **`## Formato de saída (OBRIGATÓRIO)`** — idêntico ao baseline: só CSV, UTF-8,
   vírgula, aspas duplas em campos com vírgula/quebra; cabeçalho exato
   `user_id,texto_relato,latitude,longitude,data,topico,urgency`; 40 linhas (ajustável).
5. **`## Regras por coluna`** — preservadas do baseline (verificadas contra `seed.py`):
   user_id estável e recorrente (~10-15 cidadãos), texto em voz de cidadão com
   referências a ruas/pontos da Gávea, lat/lon no bounding box (6 casas), data ISO no
   intervalo, topico exato da lista, urgency `alta`/`media`/`baixa` com heurística de risco.
   **Voz em primeira pessoa**: muitos relatos-fonte do Herbert estão em terceira pessoa
   ("Moradores relatam…", "Idoso relata…"). O modelo deve **personificar o morador** e
   reescrever cada relato gerado em **primeira pessoa** ("Moro na…", "Tenho medo de…",
   "Meu filho perdeu aulas porque…"), como se o próprio cidadão estivesse enviando a demanda.
6. **`## Qualidade`** — variar tópicos/urgências/locais/autores; coerência texto↔tópico↔urgency;
   distribuir os relatos pelos 7 tópicos proporcionalmente ao banco-fonte; nenhuma coluna extra.
   **Espaçamento espacial**: espalhar lat/lon por todo o bounding box da Gávea (não
   concentrar num único ponto), variando bairros/ruas. **Espaçamento temporal**:
   distribuir as datas ao longo de todo o intervalo 2025-06-18 … 2026-06-18 (não
   agrupar tudo num único mês), permitindo que um mesmo `user_id` recorrente relate em
   datas diferentes.
   **Agrupamentos coerentes com os cenários** (sobreposto ao espalhamento global): o
   espaçamento não é puramente aleatório — alguns eventos devem **se agrupar** no tempo
   e no espaço de forma realista, ligados aos cenários dos agentes públicos. Ex.: vários
   relatos de **alagamento/drenagem** (cenário Rio-Águas) concentrados num mesmo período
   chuvoso e numa mesma região; surto de relatos de **conflito armado/tiroteio** numa
   mesma semana e logradouro; relatos de **iluminação apagada** que persistem por meses
   no mesmo trecho. Assim a base reproduz "ondas" temáticas que um pesquisador veria nos
   casos de uso, não ruído uniforme.
7. **Linha final** — `Gere agora o CSV.`

Pontos de Gávea para ancorar `texto_relato` (já citados no baseline + plausíveis):
Parque da Cidade, Praça Santos Dumont, Rua Marquês de São Vicente, Rua Artur Araripe,
PUC-Rio, Estrada da Gávea, Largo da Gávea, Rua Vice-Governador Rubens Berardo.

## Passos de implementação

1. Reescrever o arquivo
   [fala-gavea/seeds/relatos/PROMPT-gerar-seed.md](fala-gavea/seeds/relatos/PROMPT-gerar-seed.md)
   conforme a estrutura acima, com o banco-fonte Herbert embutido (seções 1-7) dentro
   do bloco ```` ```text ````.
2. Colar o **conteúdo integral e literal** de `RELATOS_HERBERT.txt` sob a seção
   `## Banco de relatos-fonte (Herbert)` — sem editar, resumir ou reordenar.
3. Colar o **conteúdo integral e literal** de
   `CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt` sob a seção
   `## Cenários de agentes públicos` — sem editar nem condensar.
4. Atualizar o preâmbulo fora do bloco ```` ```text ````: remover as referências aos
   sample CSVs inexistentes; explicar que as fontes agora estão embutidas (derivadas
   dos relatos coletados pelo Herbert).
5. Conferir que o cabeçalho e a lista de tópicos batem caractere-a-caractere com
   `seed.py` e `SCHEMA.md`.

## Critérios de aceitação

- [ ] `PROMPT-gerar-seed.md` é auto-contido: contém o banco de relatos-fonte e os
      cenários embutidos; não referencia nenhum arquivo externo como pré-requisito.
- [ ] Cabeçalho de saída exatamente `user_id,texto_relato,latitude,longitude,data,topico,urgency`.
- [ ] Lista de tópicos idêntica (sem acento) à de `seed.py`/`SCHEMA.md`.
- [ ] Bounding box, intervalo de datas e heurística de urgency preservados do baseline.
- [ ] O texto **integral e literal** dos dois `.txt` do Herbert está embutido, sem
      destilação, resumo ou paráfrase.
- [ ] O prompt instrui geração de relatos *parecidos* (não cópias) e exige
      espaçamento **espacial** (lat/lon por todo o bounding box) e **temporal**
      (datas por todo o intervalo).
- [ ] O prompt instrui reescrita em **primeira pessoa**, personificando o morador
      (mesmo quando o relato-fonte está em terceira pessoa).
- [ ] O prompt instrui **agrupamentos coerentes** de eventos no tempo/espaço ligados
      aos cenários dos agentes (ex.: alagamentos concentrados num período/região).
- [ ] Nenhuma referência remanescente a `data/sample-gavealab.csv` ou
      `data/sample-gavealab-diagnostico.csv`.

## Verificação

- Revisão visual do markdown reescrito (diff contra o baseline).
- (Opcional, manual) Rodar o prompt em um LLM, salvar o CSV gerado e testar
  `POST /admin/seed/relatos` com o painel admin do fala-gavea para confirmar
  `inserted > 0` e `errors == []`.
- Não há testes automatizados para arquivos de prompt; a verificação é por inspeção
  + import manual.

## Fora de escopo

- Gerar o CSV em si (o deliverable é o prompt, não os dados).
- Copiar os `.txt` do Herbert para dentro de `fala-gavea/` (descartado: optou-se por embutir).
- Alterar o endpoint de seed, o SCHEMA.md ou o `seed_relatos.py`.
- Adicionar a coluna `urgency` ao SCHEMA.md (discrepância pré-existente: SCHEMA lista
  6 colunas, endpoint aceita 7 — registrar como nota, não corrigir neste plano).

## Notas / riscos

- **Discrepância SCHEMA vs endpoint**: `SCHEMA.md` documenta 6 colunas (sem `urgency`),
  mas `seed.py` lê `urgency`. O baseline e este plano seguem o endpoint (7 colunas).
  Vale um plano separado para alinhar o SCHEMA.md.
- Tamanho do prompt cresce ao embutir os dois `.txt` na íntegra (~210 + ~125 linhas)
  — aceitável; cabe folgado em qualquer janela de contexto moderna. Como o texto-fonte
  é colado dentro do bloco ```` ```text ````, atenção para que o conteúdo Herbert não
  contenha crases triplas que quebrem a cerca (não contém).
```

## Review (light)

- Escopo de arquivo único, baixo risco, sem código executável → profundidade `light`.
- Conformidade com fontes verificada diretamente em `seed.py` e `SCHEMA.md`.
- Sem violação de constituição/standards (arquivo de documentação/prompt, não toca
  persistência nem LLM client).
