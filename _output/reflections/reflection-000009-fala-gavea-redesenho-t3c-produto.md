# Reflection 000009 | 2026-05-26 23:21 UTC | fala.Gavea — redesenho T3C e ideias de produto

## Artifacts reflected on

- [advisory-000002 — Atlas georreferenciado Amazônia + IA](../advisory-logs/advisory-000002-atlas-georreferenciado-amazonia-ia.md) (2026-04-24)
- [advisory-000003 — Casos de uso: cidadão / gestor / GaveaLab](../advisory-logs/advisory-000003-use-cases-virtual-space-citizens-public-agents.md) (2026-05-22)
- [advisory-000004 — Talk to the City: deployment local](../advisory-logs/advisory-000004-talk-to-the-city-local-deployment-extension.md) (2026-05-23)
- [advisory-000005 — Plugin de ingestão multi-formato](../advisory-logs/advisory-000005-multi-format-data-ingestion-plugin-tttc.md) (2026-05-24)
- [plan-000001 — PoC TRL 3: T3C local com Ollama](../plans/plan-000001-trl3-poc-tttc-local-ollama.md) (2026-05-24)
- [qa-000004 — Planejamento da PoC / dados GaveaLab](../qa-logs/qa-000004-tttc-local-ollama-poc-gavealab-planning.md) (2026-05-24)

**Escopo declarado pelo usuário:** redesenho simplificado do Talk to the City, com processamento por LLM local, em TRL 3, sem autenticação por enquanto. Foco em ingerir estudos, criar ferramentas de análise e integrar dados entre eles. O caso de uso do GaveaLab é o principal — é nele que se cria todo o arcabouço do projeto, permitindo um sistema que armazene dados de pesquisas e que pesquisadores façam análises aprofundadas com ferramentas de IA.

## Summary

O arco dos seis artefatos descreve uma convergência: partiu de um atlas georreferenciado amplo (advisory-000002) e foi estreitando até um PoC concreto de síntese de pesquisas cívicas locais.

- **advisory-000002** explorou estender o kb-qa para um atlas geoespacial e diagnosticou que o kb-qa cobre só 20-30% do necessário. Convergiu para arquitetura em camadas (RAG textual + DuckDB spatial orquestrados por agente). Na Q2 o usuário redirecionou o escopo: controle de acesso pertence à camada HTTP (API REST), não a metadados (`sensitivity_level` vira metadado de curadoria); e preferência por um serviço autocontido (executável que sobe MCP+REST) com LLM local plugável via litellm. Princípios CARE/OCAP como restrição de soberania de dados.
- **advisory-000003** completou e refinou os três casos de uso: UC1 (cidadão) ganhou cláusula motivacional; UC2 foi dividido em gestor público (UC2a) e investidor (UC2b); UC3 (GaveaLab) foi decomposto em coleta (UC3a), síntese (UC3b) e consolidação de perfis (UC3c). Apontou o pipeline Talk to the City como arquitetura de referência para UC3b, mapeou 12 datasets abertos brasileiros, e levantou riscos de LGPD, astroturfing e captura da camada de síntese.
- **advisory-000004** mapeou o tttc-light-js (monorepo pnpm, 3 apps, 5 dependências de nuvem com substitutos locais), o fork `tttc-light-js-ollama`, e o ponto de extensão `kb_qa_enrich`.
- **advisory-000005** propôs o adaptador LLM multi-formato em 3 camadas (parser → extrator LLM → normalizador) e a sinergia de alimentar tanto o T3C quanto o ChromaDB do kb-qa com o mesmo adaptador.
- **plan-000001** (PoC TRL 3) está com steps 1-3 feitos, step 4 pela metade (CSV dos 6 temas reais do GaveaLab pronto; script `adapt_to_tttc.py` não), step 5 pendente.
- **qa-000004** costurou tudo: pesquisa do fork → escopo TRL 3 → plano → ideia do plugin → CSV baseado nos 6 temas reais do diagnóstico GaveaLab 2023 (Segurança, Governança, Infraestrutura/esgoto, Saúde, Habitação, Meio ambiente — segmentado em asfalto vs favela).

## Reflection

> ideias:
> fala.BR - plataforma existente. pesquisar
>
>
> Ideias de nome para o projeto:
>
> fala.Gavea
> produto que a gente coloque gravando a conversa e envia para o sistema
> ele extrai cidadaos unicos com id do audio
> as transcricoes alimentam uma plataforma para analise. id, claim (formato talk to the city)
> pergunta: como garantir lgpd ? : se inscrever no curso puc
> seria bem interessante um cidadão que participa de um forum com o fala.Gavea pudesse ter poder sobre o que está no site. casa forum gera um id, que o cidadao detém o direito de enviar ou nao para o forum virtual. caso envie o cidadao pode fazer o que bem entender com esse id e colocar a informacao que lhe for conveniente.
>
> skills para o seja
> seja-agil - minha filosofia de dev. pesquisar praticas atuais amplificadas com uso de llms. [produtizacao]
>
> ferramenta digital para amplificar, escutar , realidade

## Follow-ups

Perguntas em aberto que emergiram da reflexão (registradas como observações, não como recomendações):

- **fala.BR** — plataforma federal de ouvidoria já citada no advisory-000003 (Fala.BR / CGU, 6M+ manifestações, API REST). Qual a relação entre o nome de produto "fala.Gavea" e a plataforma existente fala.BR? O que de fala.BR é referência e o que é distinção?
- **Captura de áudio → ID de cidadão → claim** — o fluxo proposto (gravador → extração de cidadãos únicos por ID de áudio → transcrição → formato `id, claim` do T3C) introduz uma etapa de ASR + diarização/identificação de locutor que ainda não aparece em nenhum artefato. advisory-000005 listou áudio como formato de "alta dificuldade" (ASR + segmentação) reservado para TRL 4+. Como esse fluxo se encaixa no escopo TRL 3 atual?
- **LGPD via inscrição no curso PUC** — a ideia de garantir base legal LGPD através da inscrição no curso PUC é uma resposta direta à lacuna de "base legal/consentimento" levantada em advisory-000003 (R3). Qual o escopo dessa base legal e como ela se relaciona com o consentimento granular e revogável que a LGPD exige?
- **Soberania do cidadão sobre o próprio ID** — a ideia de o cidadão deter o direito sobre o ID gerado em cada fórum (decidir enviar ou não ao fórum virtual, e controlar a informação associada) é um modelo de governança de dados centrado no titular. Como ele se relaciona com os princípios CARE/OCAP de advisory-000002 e com o "ledger de identidade pseudônima purgável" de advisory-000003?
- **seja-agil / skills para o SEJA** — ideia de produtizar uma filosofia de desenvolvimento ("seja-agil") como skills do harness SEJA, pesquisando práticas atuais amplificadas por LLMs. É um eixo distinto do sistema fala.Gavea — vale rastrear separadamente?
