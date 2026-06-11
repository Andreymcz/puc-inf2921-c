# Texto copiado de https://onedrive.live.com/:w:/g/personal/7ad9a5228970b927/IQCOXhAGEmIiS52Qf58HbMmVAcLn3-iABMf9cm6Fdpkp9yA?rtime=X9JDPzzH3kg&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3cvYy83YWQ5YTUyMjg5NzBiOTI3L0lRQ09YaEFHRW1JaVM1MlFmNThIYk1tVkFjTG4zLWlBQk1mOWNtNkZkcGtwOXlBP2U9aUVqR1Rl

Núcleo de Prática Jurídica – Departamento de Direito 

 

INF2921/CIS2114 - Projeto de sistemas de IA 

Plataforma Fala Gávea 

 

Professores: 

Renato Cerqueira  

 Gabriel Banaggia 

 

Alunos(a): 

Andrey Rodrigues 

Júlia Calixto 

Herbert de Carvalho 

Natalí Garcia 

Sheila Manhães 

 

 

 

 

 

 

Rio de Janeiro, 

Junho de 2026. 

Contextualização 

A Plataforma Fala Gávea é uma solução open source inspirada na ferramenta Talk to the City, desenvolvida para centralizar reivindicações, ideias e percepções de cidadãos dos territórios da Gávea, Parque da Cidade e Rocinha. A plataforma opera como uma camada de inteligência sobre dados brutos estruturados como csv permitindo que gestores públicos, pesquisadores e investidores sociais tomem decisões embasadas em fatos. 

A arquitetura central fundamenta-se em uma tríade sistêmica: (1) base de conhecimento alimentada por relatos cidadãos, (2) perguntas de usuários decisores, e (3) ferramentas de processamento com IA e validação humana. O objetivo é democratizar o acesso à informação territorial mantendo rigor ético, conformidade com a LGPD e alinhamento ao PL 2338 (Marco Regulatório da IA no Brasil). 

Caso de Uso 01: Consulta para tomada de decisão 

Como gestor público ou investidor, quero conhecer os problemas e necessidades de um território para tomar decisões embasadas nas demandas reais dos cidadãos. 

Ator Principal: Gestor Público / Investidor 

Objetivo 

Permitir que agentes decisores, gestores públicos, investidores, pesquisadores e líderes comunitários, acessem uma visão estruturada, segmentada das reivindicações e percepções dos cidadãos, viabilizando a formulação de políticas públicas e investimentos baseados em evidências. 

Atores 

Ator 

Tipo 

Interesse Principal 

Gestor Público 

Primário 

Formular e justificar políticas públicas com base em dados reais 

Investidor Social 

Primário 

Identificar prioridades e alocar recursos estrategicamente 

Pesquisador 

Primário 

Consolidar e analisar dados de campo e fontes externas 

Líder Comunitário 

Secundário 

Auditar se as demandas capturadas condizem com a realidade do território 

 

Pré-condições 

A plataforma deve conter uma base de dados com relatos e reivindicações de cidadãos já processados e categorizados. 

Deve existir ao menos um conjunto de dados territorializados disponível para consulta. 

Fluxo Principal 

Passo 

Ator 

Ação 

1 

Agente 

Acessa o dashboard da plataforma e seleciona o território de interesse (ex.: Rocinha, Gávea Asfalto, Parque da Cidade) 

2 

Sistema 

Exibe painel com clusters temáticos das reivindicações: segurança, mobilidade, saúde, educação, etc. 

3 

Agente 

Aplica filtros por tema ou nível de urgência. 

4 

Sistema 

Atualiza visualizações: gráficos de volume  

5 

Agente 

Seleciona um cluster para aprofundamento e acessa relatos representativos e opiniões divergentes  

6 

Sistema 

Apresenta lista priorizada de demandas, tendências temporais e comparativo entre subterritórios 

7 

Agente 

Exporta relatório estruturado para embasar proposta de política pública ou investimento 

 

 

Fluxos Alternativos 

Dados insuficientes para o território selecionado 

O sistema exibe alerta informando a baixa densidade de dados para o território. 

Sugere territórios vizinhos com dados disponíveis ou convida o agente a iniciar uma campanha de coleta. 

Validação por líder comunitário 

O líder acessa a plataforma com perfil diferenciado e pode sinalizar relatos como 'condizente com a realidade' ou 'requer revisão'. 

Sinalizações ficam visíveis para gestores como camada de auditoria territorial. 

Requisitos Não-Funcionais e Éticos 

Todos os relatos exibidos devem estar anonimizados em conformidade com a LGPD. 

Mecanismos de coleta com risco classificado como alto pelo Marco Regulatório exigem documentação adicional de justificativa e transparência. 

Visões estatísticas não devem invisibilizar nuances: dados devem ser obrigatoriamente segmentáveis por subterritório (asfalto vs. favela) para evitar médias enganosas. 

Caso de Uso 02 - Coleta, Síntese e Gestão da Base de Conhecimento 

Como GaveaLab, quero uma ferramenta que colete e sintetize pesquisas com cidadãos, democratize o acesso à informação e consolide perfis e necessidades do território. 

Ator Principal: GaveaLab 

Objetivo 

Fornece ao GaveaLab uma plataforma que processe dados brutos de arquivos csv e gere sínteses inteligentes com supervisão humana. O sistema deve clusterizar tópicos automaticamente via IA, extrair opiniões divergentes, suportar edição e revisão manual dos resultados e consolidar um perfil territorial vivo e auditável. 

 

Atores 

Ator 

Tipo 

Responsabilidade 

GaveaLab  

Primário 

Curadoria dos dados estruturados, revisar clusters e validar sínteses 

Sistema de IA (LLM local/API) 

Sistema 

Clusterizar reivindicações, extrair claims, criar tópicos e classificar claims por tópicos fornecidos 

Revisor Humano 

Secundário 

Auditar categorias geradas pela IA, editar ou rejeitar sugestões 

Cidadão  

Externo 

Fornecer relatos via áudio, texto ou formulário estruturado 

 

Pré-condições 

Ao menos uma fonte de dados deve estar coletada (o CSV com claims do GaveaLab). 

O modelo de IA deve estar configurado, local (Ollama/LLaMA) ou via API (Claude, GPT), com chave de acesso válida quando aplicável. 

Fluxo Principal — Ingestão e Processamento 

Passo 

Ator 

Ação 

1 

Operador 

Faz upload de CSV com reivindicações  

2 

Sistema 

Normaliza os dados: extrai campo de texto, associa metadados (origem, data, território) 

3 

Sistema (IA) 

Executa pipeline de clusterização: extrai claims individuais dos relatos brutos 

4 

Sistema (IA) 

Agrupa claims em tópicos e subtópicos; gera títulos de categoria automaticamente 

5 

Sistema (IA) 

Identifica opiniões divergentes dentro do mesmo cluster  para debate 

6 

Revisor humano 

Acessa interface de revisão, valida ou edita títulos de categoria, move claims entre clusters 

7 

Sistema 

Consolida versão aprovada e atualiza o dashboard para consulta pelos agentes do Caso de Uso 1 

 

Fluxo Alternativo  

 Coleta por Áudio 

Operador grava áudio de fórum físico ou entrevista e faz upload para a plataforma. 

Sistema transcreve o áudio para texto (ferramenta local ou API de speech-to-text). 

Texto gerado entra no pipeline de processamento do Passo 2 do fluxo principal. 

Arquivo de áudio original é descartado após transcrição para garantir anonimato. 

Tecnologias empregadas 

Componente 

Descrição 

Tecnologia Candidata 

Motor de Processamento 

Clusteriza, extrai claims, identifica opiniões conflitantes 

LLM local (Ollama) + prompts configuráveis 

Interface de Consulta 

Site com filtros, áreas para análise específica e interativo 

Streamlit  customizado 

 

Requisitos Funcionais do Sistema 

Prompts de clusterização devem ser configuráveis pelo operador para guiar a IA com categorias a priori. 

Interface de revisão deve permitir edição de títulos de clusters, realocação de claims e adição de notas. 

Pipeline deve ser reprodutível e registrar versão do modelo utilizado para auditabilidade. 

Requisitos Éticos  

Dados de cidadãos de áreas vulneráveis devem ser anonimizados antes do armazenamento permanente. 

Sistema deve estar em conformidade com a LGPD (Lei 13.709/2018) e monitorar impactos do PL 2338. 

Validação humana é obrigatória antes da publicação de qualquer síntese ou relatório gerado por IA. 

 