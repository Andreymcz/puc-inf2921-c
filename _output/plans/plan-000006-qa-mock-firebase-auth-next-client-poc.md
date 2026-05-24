# QA Log -- plan-000006 -- Mock Firebase Auth no next-client para PoC citizen user
# 2026-05-24 21:43 UTC

## Brief

from research 5

## Q&A Log

**Q1:** from research 5
*(Baseado em research-000005: Mock Firebase Auth no next-client para PoC citizen user)*

**A1:** Plano 000006 gerado com 4 steps:
1. Criar patches TypeScript (`auth.ts`, `getIdToken.ts`) em `tttc-poc/patches/next-client/src/lib/firebase/`
2. Reescrever `Dockerfile.nextclient-poc` com build context `tttc-poc/` e COPY dos patches
3. Atualizar `docker-compose.yml` com context `.` para o servico next-client
4. Rebuild e smoke test (avatar "Citizen" na navbar, formulario habilitado)

**Root cause identificado:** `Dockerfile.nextclient-poc` usava build context `./tttc-light-js-ollama`,
excluindo `patches/`. A correcao segue o padrao do `Dockerfile.express-poc`.

**Q2:** Deseja commitar o plano agora?

**A2:** Sim, commitar.