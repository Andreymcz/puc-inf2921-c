# Plan 000020 | CHORE-O | 2026-06-09 23:30 | generate sample-gavealab.csv with 500 and 1000 entries | Review: light
plan_format_version: 1

## Brief

**User brief:** generate data/sample-gavealab.csv with 500 and 1000 entries

**Agent interpretation:** Extend the existing `data/sample-gavealab.csv` (30 rows of pt-BR citizen relatos from Gávea) to produce two versioned sample datasets: `data/sample-gavealab-500.csv` (500 rows) and `data/sample-gavealab-1000.csv` (1000 rows). Both files must have the same schema as the existing file (`id,comment,territory`) and contain realistic, varied pt-BR civic feedback content suitable for exercising the GaveaLab analysis pipeline (auto-topics, claims, cruxes, UMAP visualization). The existing 30-row file is kept as-is.

**Rationale for two files:** Different test scenarios call for different dataset sizes — 500 rows tests pipeline throughput at moderate scale; 1000 rows exercises embedding and UMAP performance under higher load.

## Files

- `data/sample-gavealab.csv` — existing seed file (30 rows, read for style reference)
- `data/sample-gavealab-500.csv` — new output (500 rows)
- `data/sample-gavealab-1000.csv` — new output (1000 rows)
- `_output/generated-scripts/generate_sample_csv.py` — generation script (to be committed alongside the data files for reproducibility)

## Complexity Assessment

Low — pure data generation with no code changes to the main application. No tests to update. No schema changes.

## Steps

### Step 1 — Write the generation script

Create `_output/generated-scripts/generate_sample_csv.py`.

The script must:

1. Define a corpus of pt-BR civic feedback comment templates covering the topics found in the existing seed file:
   - **Segurança pública** (policiamento, violência, abordagem policial)
   - **Infraestrutura** (calçadas, iluminação, vielas, acesso de veículos de emergência)
   - **Saneamento** (esgoto, coleta de lixo, valões)
   - **Saúde** (posto de saúde, ambulância, atendimento)
   - **Educação** (escola pública, estrutura, professores)
   - **Espaços públicos** (Parque da Cidade, áreas verdes, manutenção)
   - **Comércio local** (fechamento de lojas, especulação imobiliária)
   - **Governança** (falta de resposta da prefeitura, promessas não cumpridas)
   - **Habitação** (moradia, reforma, dignidade)
   - **Transporte** (ônibus, acesso, mobilidade)

2. Define a list of `territory` values matching the existing data: `["asfalto", "favela", "comunidade", "alto da gávea"]`.

3. Use template variation: each template has placeholders filled from synonym lists, so generated rows differ textually even when derived from the same base comment. Minimum 60 unique base templates to keep variation realistic.

4. Generate rows by sampling templates with replacement (seeded with `random.seed(42)` for reproducibility), varying territory assignment, and assigning sequential integer IDs.

5. Write two output files:
   - `data/sample-gavealab-500.csv` — 500 rows
   - `data/sample-gavealab-1000.csv` — 1000 rows (first 500 rows identical to the 500-row file to allow diff testing)

6. Use `csv.writer` with `encoding='utf-8'` and `newline=''` for correct CSV output. Header: `id,comment,territory`.

7. Print a summary: files written and row counts.

**Constraints:**
- All comment text in pt-BR.
- No comment shorter than 10 characters (minimum enforced by GaveaLab's upload filter).
- No hardcoded absolute paths — compute output paths relative to the script's location (`Path(__file__).parent.parent.parent / "data"`).
- Script is self-contained (stdlib only: `csv`, `random`, `pathlib`).

### Step 2 — Run the script and verify outputs

Run:
```
python _output/generated-scripts/generate_sample_csv.py
```

Verify:
- `data/sample-gavealab-500.csv` exists and has exactly 501 lines (1 header + 500 data rows).
- `data/sample-gavealab-1000.csv` exists and has exactly 1001 lines.
- First 500 data rows of the 1000-row file match the 500-row file exactly.
- No row has a `comment` column shorter than 10 characters.
- Both files are UTF-8 encoded.

Verification commands:
```powershell
(Get-Content data\sample-gavealab-500.csv | Measure-Object -Line).Lines   # expect 501
(Get-Content data\sample-gavealab-1000.csv | Measure-Object -Line).Lines  # expect 1001
```

### Step 3 — Smoke-test with GaveaLab upload page (manual)

This step is a manual verification hint for the implementer — it does not block the plan's completion.

Load `data/sample-gavealab-500.csv` via the GaveaLab Streamlit upload page and confirm:
- Session creation succeeds.
- Comment count shown matches 500.
- No validation errors are raised by `workspace.create_session()`.

## Review

**Depth:** light (CHORE-O, single script + data files, no application code changed)

- No security surface changes.
- No new dependencies.
- Script uses seeded RNG — fully reproducible.
- Existing `data/sample-gavealab.csv` is unchanged.
- Generated files are data artifacts; they may be gitignored or committed depending on team preference (out of plan scope — team decides).
