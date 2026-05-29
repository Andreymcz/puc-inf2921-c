# communication-000011 | CLT | 2026-05-28 | fala.Gavea: Visao, Casos de Uso e Inteligencia Territorial

Este documento sintetiza os avancos recentes do projeto fala.Gavea para o GaveaLab e coordenadores do curso INF2921/CIS2114 na PUC-Rio. Ele consolida tres artefatos produzidos entre maio e junho de 2026 -- a validacao dos casos de uso, as reflexoes sobre o conceito de produto e a pesquisa sobre inteligencia territorial alem do pipeline T3C -- em um unico panorama orientado a decisoes. O objetivo e deixar claro o que foi decidido, o que esta sendo construido, qual e o estado atual do PoC e quais sao os proximos passos concretos. A conformidade com a LGPD e a soberania de dados do cidadao sao tratadas como restricoes de primeira classe, nao como consideracoes futuras.

---

## 1. Visao e Proposta de Valor

O fala.Gavea e uma plataforma local de participacao civica territorial. Seu objetivo central e transformar depoimentos de cidadaos em evidencia acionavel para pesquisa, gestao publica e investimento social -- sem que nenhum documento ou depoimento saia da maquina onde o sistema roda.

Tres principios orientam toda a arquitetura:

**Privacidade em primeiro lugar.** Todos os embeddings, armazenamento e recuperacao de dados rodam localmente. O pipeline de LLM usa modelos locais (via Ollama), eliminando a dependencia de servicos de nuvem para o nucleo de analise. Isso nao e uma opcao tecnica -- e um compromisso com a soberania de dados dos cidadaos que contribuem seus depoimentos.

**O dado do cidadao vira evidencia, nao ruido.** O pipeline Talk to the City (T3C) transforma depoimentos textuais em arvores de temas com citacoes rastreadas. Cada claim sintetizado pode ser verificado na fonte original. Isso da legitimidade metodologica aos resultados -- requisito fundamental para publicacao academica e para uso em politicas publicas.

**GaveaLab e o caso de uso central.** O GaveaLab cria o arcabouco do projeto: sem a infraestrutura de coleta com consentimento LGPD-granular (UC3a), de sintese por IA (UC3b) e de consolidacao de perfis territoriais ao longo do tempo (UC3c), os outros casos de uso -- o cidadao contribuindo (UC1), o gestor publico priorizando (UC2a) e o investidor identificando lacunas (UC2b) -- nao tem base para operar. O GaveaLab nao e apenas usuario do sistema: e seu co-construtor institucional.

**Relacao com o fala.BR.** O nome fala.Gavea dialoga intencionalmente com o fala.BR -- plataforma federal de ouvidoria do CGU, com mais de 6 milhoes de manifestacoes e API REST aberta. O fala.BR e federal e generalista; o fala.Gavea e local, territorial e de pesquisa academica. Os dados do fala.BR sao uma das fontes de enriquecimento territorial planejadas para a plataforma, nao um concorrente.

---

## 2. Casos de Uso Validados

Os tres casos de uso originais foram refinados, o UC1 recebeu sua clausula motivacional completa, o UC2 foi dividido em dois perfis distintos com necessidades de dados irreconciliaveis, e o UC3 foi decomposto em tres sub-fluxos com riscos de privacidade e UX proprios.

| ID | Ator | Proposito |
|----|------|-----------|
| UC1 | Cidadao | Espaco virtual para discutir problemas e ideias sobre seu territorio -- o conhecimento local do cidadao e ouvido, sintetizado com outras vozes e se torna evidencia acionavel que influencia decisoes de gestores e pesquisadores |
| UC2a | Gestor Publico | Ver problemas territoriais clusterizados por tema, localizacao e urgencia para alocar recursos e desenhar intervencoes com base em evidencia cidada |
| UC2b | Investidor Social | Ver o perfil consolidado de necessidades de um territorio com dados de tendencia para identificar lacunas onde investimento cria beneficio mensuravel para a comunidade |
| UC3a | GaveaLab | Coletar depoimentos de cidadaos com consentimento LGPD-granular e base legal de pesquisa academica |
| UC3b | GaveaLab | Sintese de temas por IA (embed -> cluster -> rotular -> citar) -- a arquitetura T3C e diretamente utilizavel aqui |
| UC3c | GaveaLab | Consolidar e atualizar perfis de necessidades territoriais ao longo do tempo para rastrear mudancas, publicar achados e medir o impacto de intervencoes |

**Por que separar UC2a e UC2b importa.** Gestores publicos precisam de filas de prioridade por setor censitario, lacunas de servico medidas e correlacao com orcamento investido. Investidores de impacto precisam de capacidade economica local, capital humano, alinhamento com ODS e metricas ESG. Servir os dois com a mesma saida produz um sistema que nao serve bem a nenhum -- e cria riscos diferentes de LGPD e CARE para cada perfil. A separacao tecnica das camadas de saida e uma decisao arquitetural, nao apenas de interface.

**Por que decompor UC3.** Coleta (UC3a), sintese (UC3b) e consolidacao de perfis (UC3c) tem fluxos de UX, criterios de aceitacao e perfis de risco de privacidade separados. UC3a lida com consentimento e base legal; UC3b lida com qualidade metodologica da sintese; UC3c lida com tracking longitudinal e re-consentimento. Tratar os tres como um bloco unico cria o risco de o pesquisador chegar ao meio do fluxo e descobrir que as affordances necessarias estao ausentes.

---

## 3. Conceito fala.Gavea

O nome "fala.Gavea" emergiu da reflexao da equipe em maio de 2026 como sintese do posicionamento do produto: uma plataforma que escuta, amplifica e analisa a voz territorial de cidadaos, com raizes academicas na Gavea (PUC-Rio).

### O fluxo de captura por audio

O conceito de produto inclui uma camada de captura que vai alem de formularios textuais: o sistema recebe a gravacao de um forum presencial (ou sessao remota), extrai cidadaos unicos por ID de audio (diarizacao de locutor), transcreve cada fala e alimenta o pipeline T3C no formato `id, claim`. Isso resolve o problema pratico de que muitos cidadaos -- especialmente em comunidades de baixa renda, comunidades riberinhas e contextos amazonicos -- expressam suas necessidades muito mais naturalmente em voz do que em texto escrito.

Vale registrar que o fluxo de audio (ASR + diarizacao) e de alta complexidade tecnica e esta projetado para TRL 4+. O PoC atual (TRL 3) trabalha com dados textuais do GaveaLab.

### Soberania de dados centrada no titular

O principio de governanca mais inovador do fala.Gavea e a soberania do cidadao sobre o proprio ID. Cada forum gera um identificador que o cidadao detem. O cidadao decide se envia ou nao o seu depoimento para o forum virtual, e pode controlar o que esta associado ao seu ID. Isso implementa os principios CARE de Autoridade de Controle e Beneficio Coletivo: o dado nao e extraido da comunidade -- e oferecido pela comunidade, sob seus proprios termos.

Esse modelo se relaciona diretamente com o "ledger de identidade pseudonima purgavel" identificado em advisory-000003: o cidadao pode revogar o consentimento e ter seu ID removido do corpus sem destruir os agregados tematicos ja produzidos.

### Base legal LGPD via pesquisa academica

A garantia de conformidade com a LGPD para a coleta de depoimentos e viabilizada pela inscrição formal no curso de pesquisa da PUC-Rio, que estabelece a base legal de pesquisa academica (Art. 7, IV da LGPD). Isso responde diretamente a lacuna de "base legal e consentimento" identificada em advisory-000003 (recomendacao R3). O escopo da base legal cobre o corpus de pesquisa academica -- qualquer uso adicional dos dados (por gestores ou investidores) requer base legal propria e consentimento especifico por finalidade.

---

## 4. Inteligencia Territorial Alem do T3C

O pipeline T3C responde "o que os cidadaos dizem que precisam". Para que gestores publicos e empreendedores de impacto tomem decisoes, eles precisam de um contexto que o T3C sozinho nao fornece. A pesquisa 000010 mapeou oito camadas de dados adicionais e propos uma arquitetura de enriquecimento territorial.

### O que Gestores Publicos precisam (Camadas A-D)

**Camada A -- Contexto demografico:** Populacao por setor censitario (IBGE Censo 2022) para ponderar a severidade dos problemas relatados; piramide etaria para direcionar o tipo de intervencao; decil de renda para elegibilidade a subsidios; autodeclaracao racial para obrigacoes do FUNAI e INCRA.

**Camada B -- Lacunas de servico publico:** Cobertura de agua e saneamento (SNIS) para cruzar com claims de "sem agua" e distinguir falha sistemica de percepcao; cobertura de UBS e distancia (DATASUS/CNES); matricula escolar vs. populacao em idade escolar (INEP); reclamacoes no Fala.BR por municipio e tema.

**Camada C -- Pontuacao de prioridade:** Gestores nao querem dados brutos -- querem filas de acao priorizadas. O indice de severidade composto combina frequencia de tema (T3C) + populacao afetada (IBGE) + gravidade da lacuna de servico (SNIS/DATASUS/INEP). A tendencia longitudinal (o mesmo problema apareceu em multiplos ciclos?) e o delta orcamento-acao (o que foi investido vs. o que ainda aparece como nao resolvido) sao os sinais mais uteis para um gestor.

**Camada D -- Analitica espacial:** Poligonos de favelas e comunidades (IBGE + GIS municipal), isocronas de transporte (GTFS + OSM), zonas de risco ambiental (TerraBrasilis, CEMADEN).

### O que Empreendedores Privados precisam (Camadas E-H)

**Camada E -- Capacidade economica:** Estimativas de economia informal (datazoom.Amazonia, PNAD Continua), fluxos de transferencia Pix por CEP (BCB), densidade de MEI (Receita Federal) -- proxy para taxa de formalizacao e atividade empreendedora local.

**Camada F -- Capital humano:** Taxa de emprego formal por territorio (RAIS/CAGED), escolaridade por coorte etaria (IBGE Censo + INEP), padroes de deslocamento para logistica e investimentos em transporte.

**Camada G -- Necessidades de mercado nao atendidas:** Este e o sinal mais valioso comercialmente -- e tambem o mais arriscado. As categorias extraiveis do corpus T3C com tagueamento correto incluem acesso a saude, acesso a alimentos, acesso a servicos financeiros, conectividade e servicos habitacionais. O design determina que esse sinal nunca seja exposto sem restricao para atores comerciais em resolucao sub-setor (ver secao LGPD abaixo).

**Camada H -- Metricas ESG e medicao de impacto:** Alinhamento aos ODS (metadados ONU + indicadores IBGE ODS), IVS (Indice de Vulnerabilidade Social do IPEA, pre-calculado e aberto), exposicao a risco ambiental (CEMADEN + TerraBrasilis), fluxos historicos de investimento (SIAFI, portal BNDES).

### Arquitetura de Enriquecimento Territorial

O enriquecimento e organizado em tres camadas sobre o pipeline T3C existente:

```
Pipeline T3C (existente)
  Depoimento -> claims -> temas clusterizados -> citacoes
        |
        v
Camada de Enriquecimento Territorial (proposta)
  GeoCodificador: normalizacao endereco/territorio -> ID setor censitario
  EnriquecedorEstatico: join setor -> indicadores IBGE/SNIS/INEP/IVS
  EnriquecedorDinamico: API Fala.BR, alertas TerraBrasilis
  PontuadorPrioridade: indice composto (freq. tema + pop. + lacuna servico)
        |
        v
Saida Filtrada por Persona
  VisaoComunidade/Publica: depoimentos anonimizados + temas
  VisaoGestorPublico: Camadas A+B+C+D (sem renda/identidade individual)
  VisaoInvestidor: Camadas E+F+H (sem linkage a depoimento individual, agregado)
```

**Restricao critica:** A saida do GeoCodificador (ID do setor censitario por depoimento) deve ser armazenada como atributo derivado separado -- nunca fundida de volta ao texto do depoimento. Isso mantem o isolamento de linhagem de dados entre o depoimento pessoal e o enriquecimento estatistico. Outputs para o Gestor Publico sao APENAS agregados tematicos -- nunca rastreaveis ao individuo. Esse e um limite tecnico, nao apenas uma politica de acesso.

---

## 5. Compliance LGPD e Governanca de Dados

### Tiers de risco

Os dados que o fala.Gavea coleta e processa se distribuem em tres tiers de risco LGPD com tratamentos distintos:

**Tier 1 -- Dados sensiveis (Art. 5, IX LGPD -- maxima protecao):** Autodeclaracao racial via linkage censitario; claims sobre saude nos depoimentos; claims sobre pratica religiosa ou cultural; opiniao politica expressa. Esses dados exigem base legal especifica (Art. 11), consentimento explicito e separado, e controles tecnicos que impedem exposicao a qualquer camada de saida externa.

**Tier 2 -- Dados pessoais com base legal necessaria (Art. 7):** Depoimento geocodificado em nivel de endereco (base legal: Art. 7, VI -- legitimo interesse, ou Art. 7, III -- politicas publicas); linkage com CadUnico por territorio (apenas agregado/anonimizado; linkage individual requer consentimento especifico); indicadores DATASUS por setor censitario (disponiveis como dado aberto agregado).

**Tier 3 -- Dados territoriais nao individuais (menor exposicao):** Agregados IBGE, SNIS, TerraBrasilis e dados de pessoas juridicas (CNPJ) -- desde que setores com menos de 30 domicilios sejam suprimidos para evitar reidentificacao. Para contexto amazonico, o limiar sobe para 50 domicilios.

### Tres obrigacoes criticas de design

1. **ROPA por dataset (Art. 37 LGPD):** O Registro de Operacoes de Tratamento de Dados Pessoais deve ser mantido para cada fonte de dados ingerida alem do nucleo T3C -- independentemente de o dado ser aberto ou restrito.

2. **Consentimento especifico por finalidade (Art. 8):** O formulario de consentimento nao pode usar "melhoria civica generica". Se dados serao compartilhados com gestores, isso e uma finalidade declarada separada. Se dados serao usados para perfis de investimento, e outra finalidade declarada separada.

3. **Minimizacao de dados por persona (Art. 6, III):** Cada perfil de usuario recebe apenas o conjunto de dados necessario para sua finalidade declarada. A implementacao tecnica da Saida Filtrada por Persona nao e opcional -- e a mecanica que torna o consentimento especifico operacionalizavel.

### Mecanismo de retorno comunitario (CARE -- Beneficio Coletivo)

Qualquer relatorio de inteligencia territorial gerado a partir dos depoimentos de uma comunidade deve incluir uma versao em linguagem acessivel (nivel de leitura do 6o ano, portugues) entregue a representantes comunitarios ANTES da versao para stakeholders externos. Isso nao e um requisito etico opcional -- e a mecanica que distingue pesquisa academica responsavel de extrativismo de dados.

O sistema deve auto-gerar esse artefato de retorno junto a qualquer relatorio para gestor ou investidor.

### Comunidades indigenas -- obrigacao legal

Para qualquer implantacao em territorios com povos indigenas ou comunidades tradicionais, o protocolo de Consulta Previa, Livre e Informada (CPLI -- Decreto 5.051/2004, Convencao 169 da OIT) e obrigatorio antes de qualquer coleta. Isso nao e uma consideracao etica -- e uma obrigacao legal no Brasil.

---

## 6. Status do PoC e Proximos Passos

### Estado atual (TRL 3 -- Prova de Conceito)

O PoC em execucao valida o pipeline T3C local com dados reais do GaveaLab, sem autenticacao, rodando inteiramente na maquina local com Ollama como provedor de LLM.

| Step | Status | Descricao |
|------|--------|-----------|
| Step 1 | Concluido | Fork do T3C local com Ollama configurado e rodando |
| Step 2 | Concluido | Dados reais do GaveaLab carregados (6 temas: Seguranca, Governanca, Infraestrutura/esgoto, Saude, Habitacao, Meio ambiente -- segmentados em asfalto vs. favela) |
| Step 3 | Concluido | Pipeline T3C rodando sobre os dados do GaveaLab localmente |
| Step 4 | Em andamento | CSV dos 6 temas pronto; script `adapt_to_tttc.py` para adaptar o formato pendente |
| Step 5 | Pendente | Validacao e visualizacao dos resultados do pipeline |

O step 4 e o gargalo atual. O CSV com os dados reais dos 6 temas do diagnostico GaveaLab 2023 esta pronto; o que falta e o script de adaptacao de formato (`adapt_to_tttc.py`) que normaliza os dados para o schema de entrada do T3C.

Paralelamente, o plan-000006 esta definindo o modulo de autenticacao simulada (Firebase mock) para o fluxo do cidadao no PoC -- necessario para demonstrar a soberania de ID do cidadao em condicoes controladas.

### Roadmap imediato

**Prioridade alta -- concluir TRL 3:**
- Finalizar `adapt_to_tttc.py` e completar o step 4
- Executar o step 5 (validacao e visualizacao dos resultados)
- Demonstrar o fluxo completo: dados GaveaLab -> T3C local -> relatorio com citacoes rastreadas

**Prioridade alta -- base legal e governanca:**
- Definir ROPA inicial para os datasets do nucleo T3C + enriquecimento basico
- Definir protocolo CPLI para eventual implantacao em territorios indigenas (se aplicavel ao escopo do GaveaLab)

**Prioridade media -- EnriquecedorEstatico:**
- Construir o modulo de enriquecimento comecando pelos quatro datasets de menor atrito: IBGE Censo 2022, SNIS, IVS/IPEA, Fala.BR
- Esses quatro cobrem 80% do valor de suporte a decisao para gestores publicos com 20% da complexidade de integracao

**Prioridade media -- longitudinal e acesso diferenciado:**
- Projetar o Modulo de Engajamento Longitudinal como extensao planejada v0.2 (T3C e um pipeline sem estado -- tracking longitudinal requer extensao dedicada)
- Definir tecnicamente os tiers de acesso diferenciado (Comunidade vs. Gestor vs. Investidor) como fronteira arquitetural de primeira classe

---

## Artefatos de Referencia

- advisory-000003 -- Casos de uso: espaco virtual para cidadaos e agentes publicos (2026-05-22)
  `_output/advisory-logs/advisory-000003-use-cases-virtual-space-citizens-public-agents.md`

- reflection-000009 -- fala.Gavea: redesenho T3C e ideias de produto (2026-05-26)
  `_output/reflections/reflection-000009-fala-gavea-redesenho-t3c-produto.md`

- research-000010 -- Dados sobre cidadao alem do T3C: Agentes Publicos e Empreendedores (2026-05-28)
  `_output/research-logs/research-000010-dados-cidadao-alem-tttc-agentes-publicos-empreendedores.md`
