# QA Log — plan-000068 | Chat NL intent-to-filter | 2026-06-16 21:38 UTC

## Brief

source: research-000066 — implementar busca inteligente com chat NL: action envelope no endpoint de chat existente, ParseFilterIntent use case com validação server-side, chip de confirmação no frontend vanilla JS + Leaflet

## Q&A

**Q:** busca inteligente com IA. quero usar um chat inteligente para definir minhas intenções e como quero filtrar/visualizar os dados. O chat deve converter as intenções do usuario em chamadas de api + mudança do estado do front end para a visualização da intenção do usuário.

**A:** Plano 000068 criado para implementar `POST /intents/parse` — endpoint independente que extrai filtros de linguagem natural com Ollama (qwen3:8b), valida server-side contra enums de categoria/status e ISO dates, e retorna `{message, action|null}`. Frontend ganha painel de intent chat inline em `index.html` com chip de confirmação antes de aplicar filtros ao mapa Leaflet. 8 steps, 9 testes CI-safe, 3 emendas do review (Field max_length, A11Y, guard since>until).
