# Communication 000094 | CLT | 2026-07-31 | Pitch — Fala, Gávea!

**Produto:** Fala, Gávea! — sistema de demandas cidadãs para segurança urbana
**Destinatária:** Fabiene (coordenação / avaliação de pitch)
**Formato:** roteiro de vídeo, 1min–1min30
**Equipe:** Andrey, Mauro, Julia, Herbert, Natali — INF2921/CIS2114 2026.1

> Estruturado nos 7 passos da orientação recebida. Duração-alvo: **1:25**. Narração: ~215 palavras (≈150 palavras/min).

---

## Roteiro de narração (com marcações de tempo e imagem)

### [0:00–0:09] 1. Frase de impacto

> "Um poste apagado na Gávea. Quem você avisa?
> A maioria das pessoas não sabe — e é por isso que o poste continua apagado."

**Imagem:** rua escura da Gávea à noite / poste apagado. Corte seco para o logo **Fala, Gávea!**

---

### [0:09–0:24] 2. O problema

> "Todo dia moradores enxergam problemas de segurança urbana: iluminação quebrada, lixo acumulado, pontos de risco.
> Mas o relato se perde — vira mensagem em grupo de WhatsApp, reclamação em rede social, ligação sem protocolo.
> E do outro lado, o agente público recebe informação dispersa, sem localização, sem prioridade, sem histórico. Ninguém consegue enxergar o padrão."

**Imagem:** montagem rápida — prints de grupos de mensagens, papéis, planilha bagunçada.

---

### [0:24–0:47] 3. A solução

> "Imagine se cada relato virasse um ponto no mapa — e cada ponto, uma ação rastreável.
> É isso que o **Fala, Gávea!** faz. O cidadão abre o sistema, marca no mapa onde viu o problema, escolhe o tipo e a urgência, descreve, e envia. Menos de dois minutos.
> O agente público recebe tudo num painel: mapa, filtros, agrupamento por tema, relatos parecidos — e um assistente de IA com quem ele conversa em português para entender o que está acontecendo no bairro.
> Quando decide agir, cria um encaminhamento para o órgão responsável e acompanha até a resolução."

**Imagem (screen recording, ritmo rápido):** formulário + mapa Leaflet → envio → painel do agente → busca semântica → chat NL → encaminhamento mudando de status.

---

### [0:47–1:00] 4. O diferencial

> "O diferencial não é o mapa — é a IA que trabalha *dentro* do fluxo do agente.
> A busca é semântica: procure por 'rua escura' e o sistema traz relatos de 'poste queimado' e 'iluminação apagada'.
> E ela roda **local**: o dado do cidadão não sai para nuvem nenhuma. Se a IA cair, o sistema continua funcionando — a tecnologia apoia a decisão humana, nunca a substitui."

**Imagem:** busca "rua escura" retornando resultados com palavras diferentes; selo/legenda **"IA local · dado do cidadão não sai daqui"**.

---

### [1:00–1:12] 5. O impacto

> "O que muda: o relato deixa de ser desabafo e vira demanda com dono, prazo e status.
> Na nossa demonstração, o sistema organiza cinco mil relatos e faz o agente sair da leitura um-a-um para a triagem por tema em segundos.
> A meta é simples: reduzir o tempo entre 'o cidadão viu' e 'o órgão foi acionado'."

**Imagem:** mapa com os clusters de relatos (Rocinha, PUC, Baixo Gávea, Parque da Cidade); contador de relatos; ciclo de status `aguardando → em andamento → finalizado`.

---

### [1:12–1:22] 6. Como fazer acontecer

> "O sistema já existe e está no ar: API, aplicação web, autenticação por papel e deploy em container.
> O próximo passo é um piloto real na Gávea, com uma associação de moradores e um órgão parceiro — e a migração do banco para escala municipal."

**Imagem:** URL do deploy na tela; três ícones — *Piloto* · *Parceria* · *Escala*.

---

### [1:22–1:30] 7. Convite

> "O Fala, Gávea! nasceu como projeto de curso, mas foi construído para funcionar de verdade.
> Nos ajude a levar isso para a rua: com um bairro parceiro, a gente transforma reclamação em resolução.
> **Fala, Gávea!** — a cidade escuta."

**Imagem:** equipe / logo / call-to-action com contato.

---

## Versão enxuta (60s)

Se precisar cortar para 1:00, remova estes trechos e mantenha o resto intacto:

- Passo 2: corte a frase "E do outro lado, o agente público..." (mostre em imagem)
- Passo 3: corte "agrupamento por tema, relatos parecidos"
- Passo 5: mantenha só a primeira e a última frase

---

## Checklist de gravação

| Item | Nota |
|---|---|
| Ritmo | ~150 palavras/min; pausa de 1s entre os blocos 2→3 e 4→5 |
| Áudio | narração gravada separada do screen recording; música baixa só nos passos 1 e 7 |
| Screen recording | rodar `make seed` (perfil showcase) antes, para o mapa aparecer povoado |
| Legendas | obrigatórias — a maior parte assiste sem som |
| Duração final | conferir ≤ 1:30 antes de exportar |

---

## Nota de honestidade sobre os números

Para não gerar problema em avaliação ou em conversa com parceiro real, use os números como estão abaixo:

| Afirmação no roteiro | Base real | Como falar |
|---|---|---|
| "cinco mil relatos" | `data/seed_relatos_fala_gavea_5k.csv` — dataset **sintético** de demonstração | Dizer "na nossa demonstração" (já está no roteiro). Não apresentar como volume real da Gávea. |
| "menos de dois minutos" | tempo do fluxo de registro medido pela equipe | Cronometrar uma vez antes de gravar para confirmar. |
| "está no ar" | deploy em container (Railway) | Confirmar que a URL está viva no dia da gravação. |
| "reduzir o tempo entre o cidadão viu e o órgão foi acionado" | meta declarada, **sem baseline medido** | Manter como meta ("A meta é simples..."), nunca como resultado obtido. |

Se a equipe conseguir um dado público de segurança urbana ou iluminação do Rio antes da gravação, ele substitui bem a abertura do passo 1 e dá mais credibilidade.

---

*Fala, Gávea! — INF2921/CIS2114 2026.1 | Equipe: Andrey, Mauro, Julia, Herbert, Natali*
