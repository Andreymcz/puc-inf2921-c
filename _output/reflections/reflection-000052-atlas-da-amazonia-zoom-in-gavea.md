# Reflection 000052 | 2026-06-15 22:52 UTC | Atlas da Amazônia → zoom in para a Gávea

## Artifacts reflected on

Nenhum artefato ancorado — reflexão free-form sobre conversa de equipe (WhatsApp, 15/06/2026 19:43–20:02).

## Summary

A conversa aconteceu em dois momentos encadeados.

**Momento 1 — direção técnica (19:43–19:48):** Natali propôs não recomeçar, mas misturar o que já existe (clustering de relatos) com um mapa georreferenciado. Andrey formalizou dois casos de uso distintos: (1) o cidadão que reporta um problema de segurança com foto, localização e texto; (2) o delegado que explora um dashboard georreferenciado com filtros de linha do tempo e chat. A pergunta sobre custo computacional ("quantas florestas vamos queimar") foi retórica — sinalizando que a equipe já tinha consciência de escala antes de comprometer.

**Momento 2 — âncora acadêmica (19:51):** Andrey trouxe a informação de que Fabiene tem um documento atestando a relevância do projeto em um caso de uso real, que pode ser anexado à entrega da disciplina. A frase "e pronto, tiramos 10" sugere que a equipe vê a combinação (entrega técnica + validação de caso real) como suficiente para o critério acadêmico.

**Momento 3 — origem recuperada (19:58–20:02):** Andrey explicitou a linha genealógica do projeto: do atlas da Amazônia (primeira apresentação, escala global) para a Gávea (zoom in, escala local). A viabilidade técnica foi confirmada: Google Maps API + dados dos cidadãos = mapa customizável com baixo custo. Sheila validou a lógica, perguntando apenas pela API.

## Reflection

O que se destaca é que o projeto sempre teve uma ideia-força clara — um atlas georreferenciado de dados cidadãos — mas essa ideia ficou latente enquanto a equipe construía o pipeline de análise textual (clustering, UMAP, claims, cruxes). A conversa de hoje não é uma mudança de direção: é o retorno à ideia original com maturidade técnica acumulada.

O "zoom in" da Amazônia para a Gávea é uma decisão de escopo que transforma o projeto de conceito em PoC concreto: um bairro específico, uma vertical temática (segurança), dois personas bem definidos (cidadão e delegado), e uma API de mapa que a equipe já sabe que funciona com baixo custo.

O que ficou implícito na conversa:

1. **O clustering atual já é o motor do caso de uso 2.** O delegado que quer ver "quem está no escuro" precisa exatamente do que o pipeline de clustering já entrega — agrupamentos semânticos de relatos, filtráveis por tema e por localização. A integração com o mapa não é um novo projeto; é uma nova camada de visualização sobre o que existe.

2. **A pergunta sobre custo foi respondida antes de ser feita.** "Alguns poucos copos de água" (Andrey, 19:59) é uma referência ao argumento de que LLMs locais (Ollama) e APIs de mapa (Google Maps, gratuito até certo limite) tornam o custo operacional desprezível. A preocupação com "florestas queimadas" se dissolve quando o modelo roda local e o mapa vem de uma API com tier gratuito.

3. **Fabiene é um stakeholder real, não só uma avaliadora.** O documento que ela ofereceu não é apenas um bônus acadêmico — é evidência de que existe demanda institucional pelo produto. Isso muda o enquadramento da entrega: o projeto pode ser apresentado como uma ferramenta já validada por um caso de uso real, não só como um protótipo de curso.

4. **A equipe chegou à mesma arquitetura por caminhos diferentes.** Natali chegou pelo ângulo da simplificação ("não recomeçar"). Andrey chegou pelo ângulo da genealogia do projeto ("zoom in da Amazônia"). Sheila validou pelo ângulo técnico ("é uma API do Google?"). A convergência sem debate longo indica que a solução estava implícita no trabalho que a equipe já fez.

## Follow-ups

- Como os dados de localização do cidadão (GPS da foto/relato) se integram ao pipeline atual de clustering? O campo `territory` já existe nos Comments — é suficiente, ou precisa de coordenadas lat/long?
- O dashboard do delegado (caso de uso 2) precisa de autenticação separada, ou o modelo de "acesso local sem auth" do GaveaLab é aceitável para o PoC?
- O documento da Fabiene precisa ser adaptado ou pode ser anexado diretamente? Verificar formato exigido pela disciplina.
- O mapa georreferenciado substitui o UMAP scatter plot, complementa, ou os dois coexistem como visualizações diferentes para personas diferentes?
