# Research 000010 | -O other | 2026-05-28 00:42 | Dados sobre cidadao alem do tttc: Agentes Publicos e Empreendedores

tags: civic-tech, citizen-data, public-management, impact-investment, lgpd, territorial-intelligence, fala-gavea

## User Brief

O que o Alem dos dados que o tttc usa, quais outras informacoes Agentes Publicos e Empreendedores privados querem saber sobre o cidadao?

## Agent Interpretation

Pesquisa sobre quais dimensoes de dados sobre o cidadao sao necessarias para dois perfis de usuarios do sistema fala.Gavea, **alem** do que o pipeline Talk to the City (T3C) ja coleta (texto/depoimentos, claims, citacoes, temas clusterizados):

1. **Agentes Publicos** -- gestores publicos, servidores, formuladores de politicas publicas que precisam de suporte a decisao territorial
2. **Empreendedores Privados** -- investidores de impacto, empresas, empreendedores locais que querem entender o territorio para fins de negocio ou investimento social

Contexto: plataforma fala.Gavea (nome de trabalho), extensao local do T3C, PUC-Rio 2026, contexto brasileiro (LGPD, comunidades favelas e Amazonia).

## Files Referenced

- `_output/advisory-logs/advisory-000003-use-cases-virtual-space-citizens-public-agents.md` -- casos de uso e datasets abertos brasileiros
- `_output/reflections/reflection-000009-fala-gavea-redesenho-t3c-produto.md` -- reflexao sobre produto fala.Gavea
- `product-design/project/product-design-as-intended.md` -- design intent e personas UC2a/UC2b

---

## Q&A Log

### Q1 -- Dados sobre cidadao que Agentes Publicos e Empreendedores querem alem do T3C

**Pergunta:**

Alem dos dados que o tttc usa (depoimentos textuais, claims, citacoes, temas), quais outras informacoes Agentes Publicos e Empreendedores privados querem saber sobre o cidadao, no contexto do fala.Gavea?

**Resposta:**

O pipeline T3C responde "o que os cidadaos dizem que querem", mas nao responde "onde alocar R$10M" nem "qual problema piorou nos ultimos tres anos". As lacunas se organizam em quatro camadas para Agentes Publicos e quatro para Empreendedores.

---

### Dados que Agentes Publicos precisam (alem do T3C)

#### Camada A -- Contexto demografico (quem mora onde)

| Dado | Fonte | Por que importa |
|------|-------|-----------------|
| Populacao por setor censitario | IBGE Censo 2022 | Pondera a severidade: problema em setor com 2.000 pessoas != setor com 80 |
| Piramide etaria e genero | IBGE Censo 2022 | Indica se a prioridade e escola, saude materna, idosos ou emprego jovem |
| Decil de renda por setor | IBGE rendimento + CadUnico density | Determina elegibilidade a subsidios e capacidade de copagamento |
| Autodeclaracao racial/indigena | IBGE Censo 2022 | Obrigatorio para FUNAI, INCRA, Bolsa Familia -- e dado sensivel LGPD |

#### Camada B -- Lacunas de servico publico (o que o governo ja oferece)

| Dado | Fonte | Por que importa |
|------|-------|-----------------|
| Cobertura de agua e saneamento | SNIS/SINISA | Permite cruzar claims de "sem agua" com cobertura medida -- distingue falha sistemica de percepção |
| Cobertura de UBS e distancia | DATASUS/CNES | Identifica territorio sem posto de saude a distancia caminhavel |
| Matricula escolar vs. populacao em idade escolar | INEP Censo Escolar | Detecta criancas fora da escola por territorio |
| Densidade do CadUnico por territorio | MDS (agregado) | Indica concentracao de vulnerabilidade ja registrada; revela populacoes "invisiveis" |
| Reclamacoes no Fala.BR por municipio e tema | Fala.BR API (CGU) | Sinal de demanda cidada ja formalizado; cruza com T3C para ver o que escala vs. o que fica na participacao |

#### Camada C -- Pontuacao de prioridade e urgencia

Gestores publicos nao querem dados brutos -- querem filas de acao priorizadas. Tres metricas derivadas sao necessarias:

1. **Indice de severidade**: frequencia de tema (T3C) + populacao afetada (IBGE) + gravidade da lacuna de servico (SNIS/DATASUS/INEP) = score composto por par territorio-problema
2. **Tendencia longitudinal**: o mesmo problema foi mencionado em multiplos ciclos de engajamento? O indicador SNIS/DATASUS confirma ou contradiz a percepcao?
3. **Delta orcamento-acao**: o que foi investido nesse territorio nos ultimos N anos (SIAFI/orcamento aberto) vs. o que cidadaos reportam como nao resolvido? Esse "ponto cego" e o sinal mais claro para um gestor.

#### Camada D -- Analitica espacial

| Dado | Fonte | Complexidade |
|------|-------|-------------|
| Poligonos de favelas e comunidades | IBGE malha de setores + PCRJ/GIS municipal | Baixa |
| Isocronas de transporte | GTFS municipal + OSM | Media |
| Zonas de risco ambiental (enchentes, deslizamentos) | TerraBrasilis, CEMADEN | Baixa (WFS/WMS abertos) |
| Status de regularizacao fundiaria | INCRA + cartorio municipal | Alta -- fragmentado, pouco digitalizado |

---

### Dados que Empreendedores Privados precisam (alem do T3C)

**Nota de persona:** "Empreendedores privados" abrange tres sub-perfis com apetites de dados diferentes: (a) investidores de impacto social (ESG, CDFI), (b) investidores de mercado local (varejo, fintech, logistica), (c) empresas que oferecem servicos para populacoes vulneraveis. Esses sub-perfis nao sao eticamente equivalentes -- o design deve trata-los com acessos diferenciados (ver secao LGPD/CARE abaixo).

#### Camada E -- Capacidade economica e tamanho de mercado

| Dado | Fonte | Por que importa |
|------|-------|-----------------|
| Estimativas de economia informal | datazoom.Amazonia, PNAD Continua | TAM para fintech, microcredito, varejo em territorios sem economia formal visivel |
| Renda domiciliar per capita | IBGE PNAD Continua + CadUnico como piso | Viabilidade de produto: o morador consegue pagar R$30/mes? |
| Fluxos de transferencia Pix por CEP | BCB (estatisticas abertas por CEP) | Indica atividade economica e fluxo de caixa em territorios sem banco formal |
| Densidade de empresas por setor (CNAE) | Receita Federal CNPJ aberto por CEP | Mapeia ecossistema de negocios existente; identifica setores nao atendidos |
| Densidade de MEI | Receita Federal MEI aberto | Proxy para taxa de formalizacao e atividade empreendedora local |

#### Camada F -- Capital humano e forca de trabalho

| Dado | Fonte | Por que importa |
|------|-------|-----------------|
| Taxa de emprego formal por territorio | RAIS/CAGED por municipio | Investidores em educacao e requalificacao precisam da linha de base |
| Escolaridade por coorte etaria | IBGE Censo 2022, INEP | Informa analise de lacuna de skills para programas de forca de trabalho |
| Padroes de deslocamento (origem-destino) | IBGE OD surveys, GTFS + APIs de mobilidade | Logistica, last-mile delivery, investimentos em transporte dependem de mobilidade |

#### Camada G -- Necessidades de mercado nao atendidas (dado mais valioso e mais perigoso)

O sinal mais util comercialmente -- quais produtos e servicos os cidadaos dizem que faltam -- esta diretamente nos depoimentos T3C se corretamente tagueados. O risco e que esse sinal, exposto sem restricao para atores comerciais, transforma dados de participacao civica em inteligencia de mercado as custas da agencia da comunidade.

Categorias de necessidades nao atendidas extraiveis do T3C:
- Acesso a servicos de saude (farmacia proxima, esperas para especialista)
- Acesso a alimentos (ausencia de supermercados, monopolios locais com precos abusivos)
- Acesso a servicos financeiros (sem agencia bancaria, juros altos em emprestimos)
- Conectividade (falhas de cobertura movel, sem banda larga)
- Servicos habitacionais (encanamento, eletrica, coleta de lixo)

#### Camada H -- Metricas ESG e medicao de impacto

| Metrica | Fonte | Notas |
|---------|-------|-------|
| Alinhamento aos ODS | Metadados ODS da ONU; indicadores IBGE ODS | Mapeia claims para metas ODS especificas para relatorio ESG |
| IVS (Indice de Vulnerabilidade Social) | IPEA IVS (aberto) | Indice composto pre-existente; deve ser importado, nao recomputado |
| Exposicao a risco ambiental | CEMADEN + TerraBrasilis | Pilar "E" do ESG; investidores precisam de exposicao a risco para evitar ativos encalhados |
| Fluxos historicos de investimento | SIAFI, portal de transparencia BNDES | Mede efeito de crowding-in/crowding-out do investimento publico |

---

### Tiers de risco LGPD para os dados adicionais

**Tier 1 -- Dados sensiveis (Art. 5, IX LGPD): maxima protecao**

| Tipo de dado | Categoria LGPD | Risco |
|-------------|---------------|-------|
| Autodeclaracao racial (via linkage censitario) | Origem racial ou etnica | Targeting discriminatorio se linkado a enderecos individuais |
| Claims sobre saude nos depoimentos | Saude | Perfilamento medico em escala |
| Claims sobre pratica religiosa/cultural | Convicções religiosas | Relevante em comunidades amazonicas |
| Opiniao politica expressa em depoimentos | Opinoes politicas | Categoria sensivel direta -- critico para depoimentos sobre servicos politicos |

**Tier 2 -- Dados pessoais com base legal necessaria (Art. 7)**

| Tipo | Base legal aplicavel | Condicoes |
|------|---------------------|-----------|
| Depoimento geocodificado (nivel de endereco) | Art. 7, VI (legitimo interesse) ou Art. 7, III (politicas publicas) | Requer ROPA; limitado a competencia do orgao |
| Linkage com CadUnico por territorio | Art. 7, III (politicas publicas) | Apenas agregado/anonimizado; linkage individual requer consentimento especifico |
| Indicadores DATASUS por setor censitario | Art. 7, III | Disponivel como dado aberto agregado -- sem linkage individual |

**Tier 3 -- Dados territoriais (nao individuais): menor exposicao LGPD**

Agregados IBGE, SNIS, TerraBrasilis e dados de pessoas juridicas (CNPJ) -- desde que setores com menos de 30 domicilios sejam suprimidos para evitar reidentificacao.

**Implicacoes criticas de design:**
- Manter ROPA (Art. 37 LGPD) para cada dataset ingerido alem do nucleo T3C
- Consentimento especifico e limitado por finalidade (Art. 8) -- formulario nao pode usar "melhoria civica generica" se dados serao compartilhados com investidores
- Minimizacao de dados (Art. 6, III): cada persona recebe apenas o necessario para sua finalidade declarada
- Para comunidades indigenas: CPLI (Consulta Previa, Livre e Informada -- Decreto 5.051/2004) obrigatorio antes de qualquer coleta

---

### Matriz de disponibilidade e complexidade tecnica

| Dado | Fonte | Disponibilidade | Complexidade de integracao |
|------|-------|----------------|---------------------------|
| Agregados demograficos por setor | IBGE Censo 2022 SIDRA | Aberto, gratuito | Baixa |
| Indicadores SNIS | SNIS / Base dos Dados | Aberto, gratuito | Baixa |
| IVS (IPEA) | IPEA IVS portal | Aberto, gratuito | Baixa |
| Fala.BR por municipio/tema | Fala.BR API (CGU) | Aberto, gratuito | Baixa (REST API documentada) |
| CNES (postos de saude) | DATASUS FTP | Aberto, legado | Media (formato DBF, geocodificacao) |
| INEP Censo Escolar | INEP portal aberto | Aberto, gratuito | Baixa |
| CEMADEN risco ambiental | CEMADEN WFS/WMS | Aberto, gratuito | Media |
| TerraBrasilis | INPE API | Aberto, gratuito | Baixa |
| CNPJ/MEI (negocios locais) | Receita Federal bulk | Aberto, gratuito (100GB+) | Media (filtragem necessaria) |
| RAIS/CAGED (emprego) | MTE (agregado) | Aberto (nivel municipio) | Media |
| CadUnico microdata individual | MDS (restrito) | Restrito -- requer convenio | Alta (obrigacao institucional) |
| Regularizacao fundiaria | INCRA + cartorios | Parcialmente aberto | Alta (fragmentado) |
| Dados OD mobilidade fina | IBGE (irregular) / APIs comerciais | Irregular | Alta |

**Dados que SO a coleta primaria cobre (nao existem em datasets abertos):**
1. Resolucao sub-setor censitario (rua, quadra) -- dados abertos param no setor (~300 domicilios)
2. Tracking longitudinal de participacao -- T3C e projetado para eventos pontuais
3. Gap percepcao vs. realidade -- cruzamento de problema relatado com indicador medido requer modulo dedicado
4. CadUnico individual -- requer convenio formal (pre-requisito de governanca, nao tecnico)

---

### Riscos CARE: vigilancia e commodificacao

**Risco 1 -- Targeting predatorio (viola Beneficio Coletivo):**
Mapa de vulnerabilidade + necessidades expressas pode ser usado para microcredito predatorio, redlining de seguradoras, ou aceleracao de gentrificacao quando investidores veem "demanda insatisfeita + baixa formalizacao + infraestrutura melhorando".

*Resposta de design:* A visao do Investidor nunca expoe densidade espacial de necessidades especificas em resolucao sub-setor. Investidores ESG precisam de IVS por territorio, nao mapas de calor de "moradores demandam X" por quadra.

**Risco 2 -- Cascata de reidentificacao (viola Autoridade de Controle):**
Combinacao de (a) conteudo do depoimento geocodificado + (b) dados demograficos do setor + (c) densidade do CadUnico pode reidentificar individuos em comunidades pequenas. Em uma favela com 400 domicilios, um depoimento que menciona "sou mulher negra, mais de 60 anos, com diabetes, moro aqui desde 1980" + dados IBGE de raça/idade identifica a pessoa.

*Resposta de design:* Limiar minimo de agregacao de 30 domicilios para qualquer saida. Para contexto amazonico, elevar para 50.

**Risco 3 -- Extracao sem retorno (viola Responsabilidade):**
Se a plataforma gera relatorios ricos para investidores e gestores enquanto as comunidades que geraram os dados nao recebem beneficio visivel, replica a dinamica extrativista criticada como "colonialismo de dados" na literatura de civic tech.

*Resposta de design:* Mecanismo de retorno comunitario obrigatorio: qualquer relatorio de inteligencia territorial gerado a partir dos depoimentos de uma comunidade deve incluir uma versao em linguagem acessivel (nivel de leitura do 6o ano, portugues) entregue a representantes comunitarios ANTES da versao para stakeholders externos.

**Risco 4 -- Comunidades indigenas amazonicas (viola Etica):**
CPLI (Decreto 5.051/2004) e obrigatorio antes de qualquer coleta em territorios com povos indigenas. Nao e apenas etico -- e legal.

**Risco 5 -- Vigilancia governamental (viola Etica):**
Se gestores publicos tem acesso a tracking de depoimento individual (quem disse o que, de qual endereco, em qual data), cria capacidade de vigilancia sobre participacao civica. Desincentiva expressao especialmente em temas politicos.

*Resposta de design:* Outputs para Gestor Publico devem ser APENAS agregados tematicos -- nunca rastreavel ao individuo. Limite tecnico, nao apenas de politica.

---

## Arquitetura de Enriquecimento Proposta

```
Pipeline T3C (existente)
  Depoimento -> claims -> temas clusterizados -> citacoes
        |
        v
Camada de Enriquecimento Territorial (proposta)
  |-- GeoCodificador: normalizacao endereco/territorio -> ID setor censitario
  |-- EnriquecedorEstatico: join setor -> indicadores IBGE/SNIS/INEP/IVS
  |-- EnriquecedorDinamico: API Fala.BR, alertas TerraBrasilis
  |-- PontuadorPrioridade: indice composto (freq. tema + pop. + lacuna servico)
        |
        v
Camada de Saida Filtrada por Persona (novo contexto limitado)
  |-- VisaoComunidade/Publica: depoimentos anonimizados + temas
  |-- VisaoGestorPublico: Camadas A+B+C+D (sem renda/identidade individual)
  |-- VisaoInvestidor: Camadas E+F+H (sem linkage a depoimento individual, agregado)
```

**Restricao arquitetural critica:** A saida do GeoCodificador (ID do setor censitario por depoimento) deve ser armazenada como atributo derivado SEPARADO -- nunca fundido de volta ao texto do depoimento. Isso mantem isolamento de linhagem de dados entre o depoimento pessoal e o enriquecimento estatistico.

---

## Resumo de Recomendacoes

### ALTA Prioridade

**R1 -- Definir tiers de acesso diferenciado como fronteira arquitetural de primeira classe**

Implementar tres roles de saida (Comunidade/Publico, Gestor Publico, Investidor de Impacto) com limites de escopo de dados tecnicamente forcados, nao apenas filtros de display. Uma camada de saida unica que tenta servir todos os perfis e a raiz tanto da nao-conformidade com LGPD quanto das violacoes dos principios CARE.

**R2 -- Estabelecer ROPA e documentacao de base legal para cada tipo de dado adicional antes de construir o pipeline de enriquecimento**

LGPD Art. 37 exige isso independentemente de o dado ser aberto ou restrito. Para o caso de uso de gestor publico, Art. 7, III (execucao de politicas publicas) e a base mais forte -- mas requer que a instituicao implementadora seja ou tenha parceria formal com um orgao publico.

**R3 -- Para qualquer implantacao em territorios indigenas, implementar protocolo CPLI antes de qualquer coleta**

Decreto 5.051/2004 no Brasil. Nao e opcao etica -- e obrigacao legal.

### MEDIA Prioridade

**R4 -- Construir o modulo EnriquecedorEstatico comecando pelos quatro datasets abertos de menor atrito**

IBGE Censo 2022 (demograficos + renda), SNIS (saneamento), IVS IPEA, Fala.BR. Esses quatro cobrem 80% do valor de suporte a decisao para gestores publicos com 20% da complexidade de integracao. Estabelece a arquitetura do pipeline antes de adicionar fontes mais dificeis.

**R5 -- Projetar o Modulo de Engajamento Longitudinal como extensao planejada v0.2**

T3C e um pipeline sem estado -- cada evento de engajamento e independente. Adicionar tracking longitudinal requer estado de sessao, re-consentimento do participante e motor de comparacao. Tratar como extensao com contexto limitado proprio; projetar o schema v1 para suportar isso (timestamp, session ID em cada chunk/depoimento) mesmo sem o motor de comparacao construido.

**R6 -- Implementar limiar minimo de agregacao de 30 domicilios na camada de query**

Previne reidentificacao em comunidades pequenas independentemente do que o display mostra. Para contexto amazonico: 50 domicilios.

**R7 -- Projetar artefato de retorno comunitario junto a todo relatorio de inteligencia territorial**

Para cada saida gerada para gestor ou investidor, o sistema auto-gera resumo em linguagem acessivel (6o ano, portugues) entregue a representantes comunitarios antes da versao para stakeholder. Implementa CARE Beneficio Coletivo.

### BAIXA Prioridade

**R8 -- Adiar integracao individual do CadUnico ate convenio formal com MDS**

Dados agregados do CadUnico sao suficientes para perfilamento territorial. Linkage individual adiciona valor marginal vs. custo legal e de governanca.

**R9 -- Separar produto de dados para investidor em contrato de servico distinto**

Requer que investidores declarem tese de investimento, aceitem clausulas de beneficio comunitario e se comprometam com relatorio anual de impacto como condicao de acesso ao tier de investidor.

---

## Lacunas que apenas coleta primaria preenche

| Lacuna | Por que nao ha dado aberto |
|--------|---------------------------|
| Resolucao sub-setor censitario (rua, quadra, comunidade) | Dados abertos param no setor (~300 domicilios); assentamentos informais e comunidades ribeirinhas sao invisiveis |
| Necessidades expressas vs. derivadas | Datasets medem condicoes observadas; ordenamento de prioridades pelo proprio cidadao so vem de surveys ou processos participativos |
| Dados de comunidades indigenas e tradicionais | FUNAI TI existe mas dados socioeconômicos individuais sao fragmentarios |
| Dimensoes qualitativas/culturais | Sem variaveis para pertencimento territorial, patrimonio cultural, governanca comunitaria |
| Necessidades em tempo real de eventos agudos | Maioria dos datasets e anual ou decenal; enchentes, incendios e choques economicos sao invisiveis ate o proximo ciclo |
| Qualidade do servico vs. disponibilidade | CNES informa que posto existe; nao captura tempo de espera, estoque de medicamentos, presenca do medico |
| Economia informal | RAIS/CAGED cobrem so emprego formal; 60-80% da atividade economica em municipios amazonicos e invisivel |

---

## Referencias

| Fonte | Relevancia |
|-------|-----------|
| LGPD -- Lei 13.709/2018 | Base legal para todos os dados de cidadao no Brasil |
| ANPD Resolucao CD/ANPD no. 6/2023 | Criterios de anonimizacao para validacao de outputs T3C |
| Decreto 5.051/2004 (Convencao 169 OIT) | CPLI para povos indigenas e tradicionais |
| IBGE Censo 2022 | Principal fonte sociodemografica |
| Base dos Dados (basedosdados.org) | Ponto de entrada pratico para datasets brasileiros harmonizados |
| DATASUS / CNES / SINAN | Dados de saude por municipio |
| INEP Censo Escolar | Dados educacionais por escola e municipio |
| SNIS/SINISA | Saneamento basico por municipio |
| Fala.BR (CGU) | 6M+ manifestacoes cidadas com API REST aberta |
| datazoom.Amazonia (PUC-Rio) | Datasets integrados para municipios da Amazonia Legal |
| TerraBrasilis / INPE | Desmatamento e alertas ambientais |
| IVS / IPEA | Indice de Vulnerabilidade Social (aberto, shapefile) |
| CARE Principles (Data Science Journal, 2020) | Governanca de dados indigenas -- extensivel a comunidades vulneraveis |
| advisory-000003 (este projeto) | Mapeamento original de datasets e casos de uso |
