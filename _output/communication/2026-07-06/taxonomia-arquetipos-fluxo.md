# Taxonomia de arquétipos de fluxo de uso do harness SEJA

- **Data:** 2026-07-06
- source: research-000087 -- Rec 1 taxonomia de arquétipos
- source: plan-000088 Step 2
- **Escopo:** seção autossuficiente destinada a integração posterior no texto do doutorado / relatório do curso (área: engenharia de software / mineração de repositórios de software, MSR).

---

## 1. Pergunta de pesquisa e resposta em síntese

A pergunta que motiva esta seção é: **que fluxos de trabalho recorrentes emergem do uso prolongado de um harness de desenvolvimento assistido por agentes, além do fluxo canônico `research -> plan -> implement`?** O fluxo canônico -- pesquisar o contexto, planejar a mudança, executar o plano -- é a espinha dorsal esperada por construção do próprio harness, e de fato domina os dados: a transição `plan -> implement` é a mais frequente em todos os cortes analisados (50% a 71% das saídas de `plan`, conforme a fase). A contribuição desta seção, porém, está no que aparece **além** dele. A mineração do histórico completo de invocações de skills em dois repositórios do mesmo desenvolvedor (research-000087) revela que o fluxo canônico se especializa e se recombina em **cinco arquétipos recorrentes**: o *fluxo de bootstrap*, a *execução por ondas de roadmap*, o *loop de grooming*, o *micro-loop de feature* e o *fluxo de relato*. Cada arquétipo corresponde a um regime de trabalho distinto do desenvolvedor, e a distribuição dos arquétipos difere sistematicamente entre o perfil de uso exploratório (prototipação e acúmulo de conhecimento de domínio) e o perfil focado (implementação de um produto bem definido).

## 2. Regra de identificação operacional

Para que a taxonomia seja reproduzível, adotamos a seguinte regra de identificação, herdada da metodologia da pesquisa de origem (research-000087) e reverificada de forma independente contra os índices de invocações (`taxonomia-support-counts.md`, plan-000088 Step 1):

1. **Evento**: cada linha do índice de briefs de um repositório é um evento `(timestamp, skill, brief, status)`. Os eventos são reordenados explicitamente por timestamp; empates (invocações em lote) preservam a ordem do arquivo como critério de desempate.
2. **Sessão**: eventos consecutivos separados por **até 3 horas** pertencem à mesma sessão. A análise de sensibilidade da pesquisa de origem (cortes de 1h, 2h, 3h e 6h) indica que os arquetipos são estáveis nos quatro cortes; apenas a granularidade das sessões muda.
3. **Assinatura de sessão**: a sequência de skills da sessão com **repetições consecutivas colapsadas** (por exemplo, `plan, implement, implement, implement` colapsa para `plan -> implement^n`).
4. **Ocorrência de arquétipo**: uma **subsequência** da assinatura de sessão que casa com a assinatura do arquétipo. As contagens de suporte são indicadas caso a caso, na forma em que puderam ser verificadas (contagem de sessões, contagem de artefatos com encadeamento `source:` explícito, ou probabilidade condicional de transição `P(próxima|atual)` com o `n` da linha).

Os corpora analisados são: **96 invocações** no repositório exploratório (puc-inf2921-c, 24/abr a 30/jun de 2026) e **120 invocações** no repositório focado (fala-gavea, 17/jun a 1/jul de 2026), ambos verificados. Os números referem-se ao corpus congelado na janela da pesquisa; o índice vivo do repositório exploratório já contém uma invocação a mais (a própria research-000087, de 06/jul). A análise segmenta o histórico em quatro fases ancoradas em eventos: **F1 exploração** (24/abr a 10/jun, repo exploratório), **F2 transição** (10 a 17/jun, protótipos do produto ainda no repo exploratório), **F3 execução focada** (17/jun a 1/jul, repositório dedicado do produto) e **F4 relato** (19 a 30/jun, cauda de comunicação no repo exploratório, **concorrente** com F3 -- fluxos paralelos por repositório, não uma linha do tempo global).

## 3. Os cinco arquétipos

A tabela abaixo resume a taxonomia; as subseções seguintes descrevem cada arquétipo com sua assinatura, o comportamento do desenvolvedor que ele representa, o suporte quantitativo verificado e um exemplo âncora concreto (artefatos referenciados por ID).

| # | Arquétipo | Assinatura | Fase dominante | Suporte verificado |
|---|---|---|---|---|
| 1 | Fluxo de bootstrap | `advise/research -> plan -> implement^n` | F1 | 3 sessões de F1 iniciam com advise; `implement -> implement` 75% (6/8) em F1 |
| 2 | Execução por ondas de roadmap | `plan --roadmap -> (plan[item de onda] -> implement)^n` | F2/F3 | 15 planos do fala-gavea + 4 do repo exploratório com `source:` apontando para roadmap; `plan -> plan` 40% (8/20) em F2 |
| 3 | Loop de grooming | `reflect -> (research|plan) -> plan -> implement` | F3 | 11 reflections em F3; 8 seguidas de research (4) ou plan (4) na mesma sessão |
| 4 | Micro-loop de feature | `(research -> plan -> implement)^n` | F3 | P(plan|research) = 70% (16/23) em F3 |
| 5 | Fluxo de relato | `research -> communicate` | F4 (e cauda de F3) | `communicate -> research` 100% (2/2) em F3; F4 dominada por research 31% e communicate 25% |

### 3.1 Fluxo de bootstrap

**Assinatura:** `advise/research -> plan -> implement^n`.

**Descrição.** É o regime de abertura de um espaço de problema ainda mal definido. O desenvolvedor começa a sessão com uma skill consultiva (`advise` ou `research`) para delimitar o que se sabe e o que falta saber, converte o resultado em um único plano longo e então executa esse plano em uma cadeia de invocações sucessivas de `implement`, frequentemente distribuídas por dias -- e até por máquinas -- diferentes. O que distingue o bootstrap do fluxo canônico não é a presença dos três estágios, mas a **assimetria** entre eles: um único ato de planejamento sustenta muitas execuções encadeadas, porque no início do projeto o custo de re-planejar é alto e o plano funciona como memória externa entre sessões.

**Suporte verificado.** Em F1, 3 sessões iniciam com `advise` (entry-point de sessão), e a transição `implement -> implement` atinge 75% (6/8, n=8) -- a maior autotransição de `implement` de todas as fases, caindo para 29% em F2 e 15% em F3, o que confirma que a execução passo-a-passo de um plano longo é característica da fase de bootstrap e não do regime focado.

**Exemplo âncora.** O plano 000001 (protótipo tttc-poc, a adaptação local do Talk to the City), executado por steps em dias e máquinas diferentes -- a materialização direta do `implement^n` da assinatura.

### 3.2 Execução por ondas de roadmap

**Assinatura:** `plan --roadmap -> (plan[item de onda] -> implement)^n`.

**Descrição.** Quando o escopo do trabalho é grande demais para um único plano, o desenvolvedor invoca o modo roadmap: um artefato de decomposição que organiza o trabalho em ondas (*waves*) de itens. Cada item da onda vira, em seguida, um plano próprio que referencia o roadmap de origem via header `source:`, e cada plano é executado pelo seu `implement`. O arquétipo aparece nos dados como rajadas de `plan -> plan` (enfileiramento de planos consumindo itens da mesma onda) seguidas de pares `plan -> implement`, e como uma cadeia documental verificável nos headers dos arquivos de plano.

**Suporte verificado.** A contagem verificada por inspeção direta dos headers é: **15 planos do fala-gavea** com `source:` apontando para um roadmap -- destes, 8 com item de onda explícito na linha ("Wave N", roadmaps 000071, 00001 e 000088) e 7 com `source: roadmap-000151` (roadmap organizado em 3 ondas, cuja linha `source` nos planos 000152-000158 não repete o texto "Wave") -- **mais 4 planos no repositório exploratório** (roadmap-000026 W0-1, roadmap-000028 W0-1 e W1-1, roadmap-000071 Wave 0). O relatório de pesquisa original cita 12 planos no fala-gavea; esse valor **não foi reproduzido** por nenhum critério de contagem testado (o critério estrito por "Wave" explícito dá 8; o critério amplo por `source: roadmap-NNN` dá 15) e deve ser lido como número da pesquisa original, não verificado. A direção do achado -- suporte de dois dígitos ao encadeamento roadmap -> plano no perfil focado -- permanece válida sob qualquer dos critérios. O arquétipo também explica o pico de `plan -> plan` em F2: 40% (8/20, n=20), contra 14% em F1 e 17% em F3.

**Exemplo âncora.** O roadmap-000151 do fala-gavea, cujas 3 ondas foram consumidas pelos planos 000152 a 000158; no repositório exploratório, o roadmap-000071 (Wave 0), que atravessa a fase de transição.

### 3.3 Loop de grooming

**Assinatura:** `reflect -> (research|plan) -> plan -> implement`.

**Descrição.** É o mecanismo de re-orientação periódica do perfil focado. O desenvolvedor invoca `reflect` ancorado em artefatos existentes (planos concluídos, roadmap vigente, estado do produto), usa a reflexão para inventariar lacunas entre o que foi construído e o que foi prometido, e o resultado alimenta imediatamente o próximo ciclo de trabalho -- ou via uma `research` que aprofunda a lacuna encontrada, ou diretamente via um novo `plan`. O nome "grooming" é deliberado: o padrão é análogo ao refinamento de backlog de metodologias ágeis, mas aqui mediado por uma skill de reflexão que produz um artefato persistente.

**Suporte verificado.** Em F3 existem **11 reflections** (arquivos em `fala-gavea/_output/reflections/`), e a linha de transições de saída de `reflect` em F3 tem n=11, das quais **8 são seguidas por research (4) ou plan (4) na mesma sessão** -- ou seja, em quase três quartos dos casos a reflexão não encerra a sessão, e sim bifurca para o próximo ciclo (reflect -> plan 36%, reflect -> research 36%).

**Exemplo âncora.** A reflection-000086 (inventário em tabela do estado CRUD do produto contra o roadmap vigente) e a reflection-000163, ambas seguidas de novos ciclos de planejamento na mesma janela de trabalho.

### 3.4 Micro-loop de feature

**Assinatura:** `(research -> plan -> implement)^n`, repetido dentro da mesma sessão.

**Descrição.** É a unidade de trabalho do perfil focado -- o fluxo canônico comprimido e iterado. Em vez de uma pesquisa ampla que abre espaço de problema (como no bootstrap), a `research` aqui é *just-in-time*: uma consulta curta e dirigida, imediatamente acoplada ao plano que a consome, seguida da implementação, e então o trio recomeça para a próxima feature dentro da mesma sessão. O que era, no perfil exploratório, um arco de dias (uma pesquisa -> um plano longo -> muitas execuções) torna-se, no perfil focado, um ciclo de minutos a horas repetido 2 a 4 vezes por sessão.

**Suporte verificado.** Em F3, P(plan|research) = **70%** (16/23, n=23) -- contra 33% em F2 -- indicando o acoplamento imediato pesquisa-plano. As assinaturas de sessão de F3 exibem o trio repetido de forma literal na saída do script de mineração (ex.: `implement > research > plan > implement > research > plan > implement > ...`).

**Exemplo âncora.** As assinaturas de sessão de F3 com 2 a 4 repetições do trio, exemplificadas na pesquisa de origem pelas sessões de 21/jun e 26/jun no fala-gavea (research-000087); a repetição do trio foi reverificada nas assinaturas emitidas pelo script de mineração.

### 3.5 Fluxo de relato

**Assinatura:** `research -> communicate` (com o retorno `communicate -> research`).

**Descrição.** É o harness usado não como motor de construção, mas como **arquivo consultável**: o desenvolvedor pesquisa o próprio histórico de artefatos (planos, reflections, briefs) para produzir material voltado a audiências externas -- relatórios, seções de texto acadêmico, material de apresentação. O padrão aparece como pares alternados de `research` e `communicate` em sessões curtas e esparsas, com pouca ou nenhuma invocação de `implement`. É o arquétipo que caracteriza a fase F4, que ocorre nas mesmas semanas de F3 mas no repositório exploratório, com cadência e composição opostas (2.3 invocações/sessão em F4 contra 6.7 em F3).

**Suporte verificado.** A transição `communicate -> research` é 100% (2/2, n=2) em F3 -- n pequeno, leitura descritiva apenas -- e a composição de F4 é dominada pelo par: research 31%, communicate 25% (plan 19%), invertendo a hierarquia de skills de todas as fases de construção.

**Exemplo âncora.** A própria cadeia que produz esta seção é uma instância contemporânea do arquétipo: a research-000087 (mineração do histórico) alimenta, via plan-000088, este artefato de comunicação -- o harness consultando seu próprio arquivo para relatar-se.

## 4. Fechamento: o papel duplo de /reflect

A taxonomia acima é estrutural: descreve formas de sequência. O achado qualitativo que a conecta de volta à pergunta comparativa dos dois perfis é que **a mesma skill pode ocupar funções distintas em arquétipos distintos**, e o caso mais nítido é `/reflect`. No perfil exploratório, `reflect` opera como **captura livre de ideação e pivô**: registra decisões estratégicas tomadas fora do harness, no momento em que redirecionam o projeto (ex.: reflection-000052, que registra um pivô de escopo do produto). No perfil focado, a mesma skill opera como **checkpoint periódico ancorado em artefatos**: inventaria lacunas contra o roadmap e alimenta o loop de grooming (arquétipo 3), como em reflection-000086. Mesma skill, mesma interface, funções opostas -- válvula de mudança de direção em um regime, instrumento de manutenção de direção no outro.

Esse achado sugere que a diferença entre os perfis exploratório e focado não está no *vocabulário* de skills disponível, e sim na *gramática* com que o desenvolvedor as combina: os arquétipos 1 e 5 pertencem ao regime exploratório e de relato, os arquétipos 2, 3 e 4 ao regime focado, e a fronteira entre eles é atravessada exatamente pelas skills de função dupla. Em resposta direta à pergunta de pesquisa: além do canônico `research -> plan -> implement`, emergem cinco arquétipos recorrentes -- e é a distribuição desses arquétipos, mais do que qualquer skill individual, que caracteriza o perfil de uso do harness.

---

*Números de suporte conforme `_output/tmp/taxonomia-support-counts.md` (plan-000088 Step 1, corpus congelado 24/abr a 30/jun); fonte primária: research-000087. Valores atribuídos apenas à pesquisa original estão marcados como não reproduzidos no texto.*

> Passe de privacidade (LGPD, Rec 3 research-000087, plan-000088 Step 4, 2026-07-06): aprovado -- exemplos referenciam artefatos por ID; nenhum nome de colega, citação verbatim de brief/reflection/WhatsApp ou conteúdo de relato cidadão presente.
