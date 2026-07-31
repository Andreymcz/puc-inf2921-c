# QA Log — communication-000094 | 2026-07-31 UTC

**Brief:** comunicar para Fabiene um pitch com o resultado do projeto Fala-Gávea. Formato de vídeo, 1min–1min30, seguindo a estrutura de 7 passos enviada por ela.

---

## Q&A / decisões da sessão

**Q: Qual segmento de audiência usar?**
A: `CLT` (clients). A orientação da Fabiene descreve um pitch para comissionadores/patrocinadores — o mesmo público de `fala-gavea/docs/communication-000126-clients.md`, que serviu de base factual. Assumido sem perguntar (sessão não-interativa); se a intenção for pitch técnico para avaliadores (`EVL`), o roteiro precisa trocar diferencial e impacto por qualidade de arquitetura e cobertura de testes.

**Q: De onde vêm os fatos do roteiro?**
A: `fala-gavea/README.md`, `fala-gavea/CLAUDE.md`, `fala-gavea/product-design/project/product-design-as-coded.md` e o comunicado de clientes 000126. Fluxos citados (registro com mapa, painel do agente com 5 visões, busca semântica, chat NL, encaminhamento com ciclo de vida, deploy em container) estão todos marcados como entregues.

**Q: Que números podem ser citados?**
A: Apenas os verificáveis. `data/seed_relatos_fala_gavea_5k.csv` tem 5.000 linhas — mas é **dataset sintético**, então o roteiro diz "na nossa demonstração". Não foi inventado nenhum dado estatístico sobre segurança urbana na Gávea; a abertura usa uma cena, não uma estatística. A seção "Nota de honestidade sobre os números" documenta cada afirmação e sua base.

**Q: Foi criado índice da pasta de data?**
A: Não — a pasta `2026-07-31/` contém um único artefato, e a regra do skill dispensa o índice nesse caso.

---

---

## Revisão 2 — reescrita a partir dos slides finais

**Q: Por que o primeiro roteiro foi descartado?**
A: Ele vendia o artefato ("mapa + busca semântica + chat"), não a tese. Os slides finais da apresentação trazem o argumento real, que é muito mais forte: **silêncio racional** (o cidadão cala por cálculo de risco, não por apatia) espelhado com a **cegueira do gestor** (dado demais, território de menos). O produto existe para reconstruir confiança, e o roteiro passou a ser construído sobre isso.

**Q: O que mudou de concreto?**
- Abertura trocada: de "um poste apagado" para o silêncio como estratégia de sobrevivência.
- Problema virou espelhado (cidadão + gestor), que é o que distingue o projeto de um canal de denúncia comum.
- Solução ancorada na **votação em pins** — "medo individual vira sinal coletivo" — mecanismo ausente do roteiro anterior.
- Diferencial reformulado pelo que se escolheu **não** fazer: anonimato, coordenada arredondada a 3 casas, IA local, humano no loop. Ética como decisão de projeto, não como disclaimer.
- Impacto: de "reduzir tempo de acionamento" (meta sem baseline) para **confiança + replicabilidade** — que é o que interessa a quem financia.
- Removida a citação aos "cinco mil relatos": era dataset sintético e enfraquecia o pitch.
- Equipe corrigida para incluir Sheila Manhães; adicionados os profs. Renato Cerqueira e Gabriel Banaggia e a URL de produção.
- Adicionadas duas seções novas: "Por que o roteiro está construído assim" (defesa de cada escolha) e cortes ordenados para a versão de 1:00.

**Q: O roteiro cabe em 1:30?**
A: 244 palavras. A ~165 palavras/min fecha em ~1:29 — apertado. A seção "Versão 1:00" lista 4 cortes em ordem de prioridade, com a contagem de palavras de cada um, e nomeia as 4 frases que não podem sair.

---

## Pontos em aberto para a equipe

1. Cronometrar o fluxo de registro antes de gravar (roteiro afirma "menos de dois minutos").
2. Confirmar que a URL do deploy está viva no dia da gravação.
3. Se surgir um dado público de iluminação/segurança do Rio, ele melhora a abertura (passo 1).
