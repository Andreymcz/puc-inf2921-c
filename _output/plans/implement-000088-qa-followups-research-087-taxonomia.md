# QA Log | implement plan-000088 | 2026-07-07 12:10 UTC | Follow-ups research-000087: taxonomia de arquetipos + figura de timeline

source: plan-000088 -- lifecycle QA companion do /implement (auto mode)

## Brief

implement plan 88 -- executar os dois follow-ups da research-000087: (1) secao de taxonomia dos 5 arquetipos de fluxo com contagens de suporte verificadas; (2) figura de timeline com faixas paralelas (repo pai x fala-gavea) evidenciando a concorrencia F3||F4.

## Execution log (auto mode, 4 iteracoes de 20)

- **Step 1 (subagente, SUCCESS, commit `9d56f0f`)**: script `mine_harness_flows.py` rodou as-is; adicionado apenas um bloco aditivo de P(next|current) com n por linha. Numeros congelados em `_output/tmp/taxonomia-support-counts.md` (corpus congelado 96/120, cutoff <= 30/jun).
- **Steps 2 e 3 (subagentes paralelos, SUCCESS, commits `a9b593a` / `6bef5a4` pelo orquestrador)**: criados `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` e `_output/communication/2026-07-06/timeline-faixas-paralelas.md`. Subagentes paralelos nao commitam nem escrevem o progress file (evita corrida de index git / append) -- padrao anotado no progress file.
- **Step 4 (subagente, SUCCESS, commit `f8728aa`)**: passe LGPD aprovado com 0 correcoes; nota de passe no rodape dos dois entregaveis.
- **Quality gate (check-000090 validate, check-000091 review)**: testes 12/12 PASS; review light sem findings criticos (3 advisories LOW); falhas do standards-checker todas pre-existentes e fora do escopo. Generator-critic: 0/2 iteracoes.

## Q&A

**Q1 (agente -> usuario, 2026-07-06):** Step 5 (condicional): integrar a secao de taxonomia e a figura de timeline no relatorio (relatorio/relatorio-inf2921-grupo-c.md/.tex) agora? Opcoes: manter standalone (recomendado, decisao registrada no plano) / integrar agora / integrar so no .md.

**A1 (usuario):** Manter standalone. Step 5 permanece nao executado (condicional); integracao pode virar plano seguinte junto com Rec 2 e Rec 5 da pesquisa.

## Achados notaveis

- Divergencia material de suporte: arquetipo "ondas de roadmap" no fala-gavea tem 15 planos com `source: roadmap` (8 com Wave explicito), nao os 12 publicados na research-000087; o texto usa os verificados e marca 12 como nao reproduzido (revisor re-verificou por grep independente).
- O briefs-index do repo pai e vivo: a propria entrada da research-000087 desloca F4 de 16 para 17 invocacoes; reproducao exige cutoff <= 30/jun (documentado no support-counts e no progress file).
- Ambiente: `python` fora do PATH no Git Bash; usar `uv run python`. `check_spec_conformance.py` nao existe nesta instalacao do harness (SKIPPED no gate).
