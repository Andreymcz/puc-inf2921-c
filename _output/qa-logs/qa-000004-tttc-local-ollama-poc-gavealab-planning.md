# QA 000004 | 2026-05-24 01:56 UTC | Talk to the City PoC local — planejamento e dados GaveaLab

**Brief**: Sessão de planejamento da PoC TRL 3 do Talk to the City rodando localmente com Ollama, incluindo pesquisa do fork, advisory de deployment, plano de execução, ideia de plugin multi-formato e criação do CSV de dados de teste baseado no relatório real do GaveaLab.

---

## Q1
Abri o Talk to the City (https://talktothe.city/) e achei bem interessante. Quero extrair toda e qualquer informação necessária para rodar o software localmente, sem depender de serviços externos. Se for muito difícil, quero saber se existe a possibilidade de extender o software. Além da interface atual, podemos criar novas ferramentas para os stakeholders do GaveaLab. Repositório: https://github.com/aIObjectives/tttc-light-js

## A1
Gerado advisory-000004: pesquisa do repositório tttc-light-js, identificação das 5 dependências de nuvem (Firebase, GCS, Pub/Sub, Redis, OpenAI), descoberta do fork `tttc-light-js-ollama` com Ollama integrado, e do precedente de Taiwan MODA. Recomendações priorizadas por risco: começar com Ollama, depois MinIO, BullMQ, e por último Keycloak.

---

## Q2
O tttc-light-js suporta deployment 100% local — há precedente real (Taiwan MODA em produção). Quero saber mais sobre este Taiwan MODA.

## A2
Pesquisa aprofundada: Taiwan MODA usou T3C na AI Alignment Assembly (2023) com 400+ participantes e 2.000+ opiniões. Os consensos influenciaram política pública real (open-source AI, sensibilidade cultural, papel pioneiro do setor público). Correção ao advisory anterior: o precedente confirma auto-hospedagem da infraestrutura, não eliminação completa de APIs externas (ainda usaram GPT-4). Conexão com vTaiwan (desde 2014, Polis + T3C).

---

## Q3
O projeto será um TRL 3, que acredito que não precisa ser um MVP, pode chegar a uma prova de conceito.

## A3
Reescopo para TRL 3: sem auth (Firebase/Keycloak desnecessários), sem persistência real (filesystem local), sem fila de jobs (execução síncrona). Apenas 3 serviços Docker: Ollama + Express + Next.js. Fluxo: CSV → pipeline worker (Ollama local) → clusters → visualização no browser.

---

## Q4
Me parece um plano interessante.

## A4
Gerado plan-000001 com 5 steps: (1) clonar fork tttc-light-js-ollama, (2) criar .env.poc desativando cloud, (3) docker-compose.yml com 3 serviços, (4) CSV de teste + adaptador multi-formato, (5) executar end-to-end e validar visualização no browser.

---

## Q5
[/pending] — listagem de ações pendentes.

## A5
5 ações pendentes (todas atrasadas): periodic-curation, spec-drift-check, e 3 create-decision-entry de advisory-000002 (atlas georreferenciado). Sessão interrompida antes de endereçar — usuário redirecionou para nova ideia.

---

## Q6
Ideia para perguntar para o stakeholder: LLM especializada em transformar dados de pesquisas armazenados em formatos diversos para o formato de entrada do fork. Pode ser um plugin que permite o stakeholder enviar dados de diversos formatos (fontes) e ser um software que permite maior integração de dados de diversas fontes com diversas tecnologias.

## A6
Análise da ideia: arquitetura em 3 camadas (parser → extrator LLM → normalizador), tabela de formatos prováveis do GaveaLab com dificuldade, comparação de esforço por TRL. Para TRL 3: script CLI `adapt_to_tttc.py` usando Ollama local. 6 perguntas formuladas para o stakeholder sobre fontes de dados atuais e dificuldades.

---

## Q7
Atualize o Step 4 do plano E crie um advisory separado para explorar melhor esta ideia.

## A7
Step 4 do plan-000001 expandido com parte 4b (script `adapt_to_tttc.py`). Criado advisory-000005 com arquitetura completa, tabela de fontes, comparação por TRL, 6 perguntas para o stakeholder GaveaLab, e sinergia identificada com kb-qa (mesmo adaptador alimenta T3C e ChromaDB). Commitados juntos.

---

## Q8
Como você sabe quais são os 4 temas do GaveaLab?

## A8
Honestidade: não sei — "≥4 temas" era requisito técnico do T3C (clustering precisa de diversidade), não conhecimento real do GaveaLab. O CSV seria fictício baseado em contexto geral. Proposta: alinhar com stakeholder antes de criar, ou usar dados que eles indicarem.

---

## Q9
O stakeholder tem respostas, mas ainda não temos acesso a elas. Vamos criar um CSV fictício com info do relatório final do GaveaLab sobre o estudo. Tem informações sobre metodologia do estudo também. Está na base de conhecimento.

## A9
Consultada a base de conhecimento (kb-qa) com 3 queries ao relatório do GaveaLab (diagnóstico jun-nov 2023). Identificados 6 temas reais do relatório: Segurança (maior reivindicação, percepções opostas asfalto vs favela), Governança/descaso do governo, Infraestrutura/esgoto, Saúde, Habitação (87% satisfação no asfalto vs 29% nas favelas), Meio ambiente. Criado `tttc-poc/data/sample-gavealab.csv` com 30 respostas fictícias fundamentadas nos dados reais, com coluna `territory` (asfalto/favela) replicando a segmentação do estudo. Commitado.

---

## Q10
Pronto, agora quero verificar o que já temos de planejamento para ingerir estas perguntas no fork do tttc-com-ollama. Este é o objetivo corrente.

## A10
Estado do plan-000001 revisado. Resumo: CSV ✅ feito. Steps 1–3 (clonar fork, .env.poc, docker-compose) pendentes. Step 4 metade feito (CSV ok, script adapt_to_tttc.py não). Step 5 (execução end-to-end) pendente. Gap crítico: Step 2 exige inspecionar o código do fork para saber nomes exatos das variáveis de ambiente — sem isso o .env.poc é especulativo. Próxima ação natural: executar Step 1 (clonar fork e inspecionar estrutura).

---

## Decisões registradas nesta sessão

| Decisão | Advisory/Plano |
|---------|---------------|
| Usar fork tttc-light-js-ollama como base (não modificar repo principal) | advisory-000004 |
| Escopo TRL 3: sem auth, sem persistência, sem fila — só 3 serviços Docker | plan-000001 |
| CSV de teste baseado nos 6 temas reais do diagnóstico GaveaLab 2023 | tttc-poc/data/sample-gavealab.csv |
| Plugin multi-formato: script CLI primeiro, plugin Express depois (TRL 4+) | advisory-000005 |
| Próximo passo: clonar fork e inspecionar variáveis de ambiente para desbloquear Step 2 | plan-000001 |
