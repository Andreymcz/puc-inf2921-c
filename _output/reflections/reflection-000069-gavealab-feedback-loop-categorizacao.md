# Reflection 000069 | 2026-06-17 11:20 UTC | GaveaLab — feedback loop ausente na categorização por IA

## Artifacts reflected on

- [plan-000060](_output/plans/plan-000060-tags-livres-security-report.md) — Tags livres em SecurityReport (Wave 1 Item 2)
- [plan-000061](_output/plans/plan-000061-ai-auto-categorizacao-curadoria-delegado.md) — AI auto-categorização + curadoria pelo delegado (Wave 1 Item 3)
- [plan-000062](_output/plans/plan-000062-backend-filtro-temporal-until.md) — Backend filtro temporal `until` (Wave 1 Item 4)
- [plan-000063](_output/plans/plan-000063-frontend-painel-filtros-completo.md) — Frontend painel de filtros completo (Wave 2 Item 5)
- [plan-000068](_output/plans/plan-000068-chat-nl-intent-to-filter.md) — Chat NL intent-to-filter — busca inteligente com IA

## Summary

Os cinco planos constroem em sequência a capacidade analítica do fala-gavea-segurança: tags livres (Wave 1) → filtro temporal → categorização por IA com curadoria humana → painel de filtros completo no frontend → chat em linguagem natural convertendo intenções em filtros.

O fluxo de curadoria (plan-000061) é não-destrutivo por design: `POST /{id}/auto_categorize` salva `ai_suggested_category` sem tocar em `category`; `PATCH /{id}/category` permite ao delegado confirmar ou corrigir, zerando a sugestão. O dado de curadoria humana existe no banco — a correção é persistida — mas nenhum dos cinco planos prevê capturar esse par (sugestão IA → decisão humana) como sinal de treino ou avaliação.

O chat NL (plan-000068) introduz um segundo ponto de curadoria implícito: o usuário aplica ou descarta o filtro sugerido pela IA, mas esse evento também não é registrado como feedback.

## Reflection

Não existe feedback loop na auto categorização pela IA. O humano pode curar, mas o feedback do humano não é usado para retroalimentar a IA.

## Follow-ups

- O par `(ai_suggested_category, category_confirmada_pelo_delegado)` já está disponível no banco — falta apenas registrá-lo como dataset de treino/avaliação. Qual seria o formato ideal para exportar esses pares?
- O evento de "aplicar filtro sugerido pelo chat NL" versus "descartar" também é sinal de qualidade do modelo — vale instrumentar?
- Qual limiar de pares curados justificaria um fine-tuning local versus ajuste de prompt (few-shot com exemplos curados)?
- O projeto Canal Digital Comunitário mencionado na sessão tem requisito explícito de feedback loop humano → modelo. O GaveaLab poderia ser o banco de dados de treino para esse sistema?
