# Check 000090 | CHORE-X | 2026-07-06 20:16 | Validation Report (quality gate plan-000088)

source: plan-000088 -- quality gate step 1 (/check validate all)

> Warning: No stack framework variables found in conventions.md. Running all check scripts. Add BACKEND_FRAMEWORK and FRONTEND_FRAMEWORK to conventions.md to enable stack filtering.

## Scope

`all` -- executed via `run_all_checks.py` (20 discovered scripts; registry `check_plugin_registry.json` absent, no stack filter). Includes test suites (test-runner, scope all). `check_spec_conformance.py` SKIPPED -- script not present in this harness installation.

## Summary

| Check | Status | Errors | Warnings |
|-------|--------|--------|----------|
| check_api_contract_sync | PASS | 0 | 0 |
| check_design_output | PASS | 0 | 0 |
| check_harness_drift | PASS | 0 | 0 |
| check_human_markers_only | PASS | 0 | 0 |
| check_route_coverage | PASS | 0 | 0 |
| check_skill_spec | PASS | 0 | 0 |
| check_unused_files | PASS | 0 | 0 |
| check_version_changelog_sync | PASS | 0 | 0 |
| check_conventions | FAIL (pre-existing) | 18 | 18 |
| check_skill_system | FAIL (pre-existing) | 24 | 1 |
| check_telemetry | FAIL (pre-existing) | 54 records | - |
| check_vuln_patterns | FAIL (pre-existing) | 4 HIGH | 0 |
| check_worktree_health | FAIL (pre-existing) | 1 | 0 |
| check_backend_test_coverage | INFO (tooling error: uv venv has no pip) | 1 | - |
| check_api_auth_decorators | SKIPPED (Flask layout absent) | - | - |
| check_frontend_test_coverage | SKIPPED (no frontend) | - | - |
| check_i18n_keys | SKIPPED (no i18n framework) | - | - |
| check_migration_chain | SKIPPED (no Alembic) | - | - |
| check_po_parity | SKIPPED (no .po catalogs) | - | - |
| check_validation_constants_sync | SKIPPED (layout absent) | - | - |
| tests: kb-qa (`uv run pytest`) | PASS | 0 (8 passed) | 0 |
| tests: gavealab-poc (`test_workspace.py`) | PASS | 0 (4 passed) | env: `uv sync` broken under Python 3.14 (llvmlite); ran via ephemeral env |

**Overall: 8/13 scored checks passed; all 5 failures are pre-existing conditions untouched by plan-000088. Tests 12/12 passed.**

## Failure details (all pre-existing, none in plan-000088 scope)

- **check_conventions**: 18 errors are `${VAR}` referenced only by harness *template* files (`BACKEND_*`, `FRONTEND_*`, `MIGRATIONS_DIR`, `MODELS_DIR`, `E2E_TEST_CMD`, `SESSION_NOTES_FILE`) -- known legacy-project condition. 18 warnings: defined-but-unused variables.
- **check_skill_system**: 22 errors from SKILL.md `references` resolving `project/*.md` while files live under `product-design/project/` (checker path-resolution mismatch; `product-design-as-coded.md` genuinely absent); 1 invalid category `scaffolding` in python-scaffold; 1 warning `conversation_trace.py` imports missing `check_secrets` (confirmed at runtime this session).
- **check_telemetry**: 54/63 records missing `decision_points` keys (`prompt`, `chosen_option`, `rationale_presented`) + unknown `session_id` -- schema drift.
- **check_vuln_patterns**: 4 HIGH in sibling/copied dirs -- `python-scaffold/scripts/scaffold.py:43` (ssti, here and in fala-gavea copy), `fala-gavea-seguranca/static/app.js:176,204` (innerHTML XSS). Not part of this plan's diff.
- **check_worktree_health**: 1 orphaned worktree artifact of the nested parent `doutourado` repo.
- **check_backend_test_coverage** (INFO): script tries `python -m pip` inside a uv-managed venv without pip.

## Assessment for plan-000088

None of the failures touch plan-000088 files (`_output/communication/2026-07-06/`, `_output/tmp/taxonomia-support-counts.md`, `_output/generated-scripts/mine_harness_flows.py`) nor production code. Classification for the quality gate: **no critical findings attributable to the plan; all failures deferred as pre-existing** (candidates for future harness-maintenance plans).
