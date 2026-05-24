# Progress -- Plan 000006

Append-only cross-iteration learnings. Each subagent reads this file at the start and appends findings at the end.

## Codebase Patterns
<!-- Subagents consolidate reusable patterns here -->

## Iteration Log

### Step 1 — 2026-05-24

**Status:** SUCCESS

**What was done:**
- Created directory `tttc-poc/patches/next-client/src/lib/firebase/`
- Created `auth.ts`: stubs `onAuthStateChanged`, `signInWithGoogle`, and `signOut`. Auto-logs in a fixed `CITIZEN_USER` object (`uid: "citizen"`, `email: "citizen@poc.local"`) via `setTimeout` callback pattern to match the async contract of the real Firebase Auth module.
- Created `getIdToken.ts`: stubs `fetchToken` to return `["data", "poc-citizen-token"]` unconditionally, matching the `AsyncData<string | null>` return type expected by callers.

**Discoveries:**
- The `patches/` directory already existed with `express-server` patches (`Firebase.ts`, `storage.ts`, `types/context.ts`), confirming the patching pattern is established in this project.
- The `next-client` subdirectory under `patches/` did not exist yet — created it alongside the full `src/lib/firebase/` path.
- No source files under `tttc-poc/tttc-light-js-ollama/` were modified.

**Committed:** `757b5bf` — plan-000006 step 1: criar patches TypeScript para auth stub

### Step 2 — 2026-05-24

**Status:** SUCCESS

**What was done:**
- Rewrote `tttc-poc/Dockerfile.nextclient-poc` to use `tttc-poc/` as the build context instead of `tttc-poc/tttc-light-js-ollama/`.
- Updated header comment to reflect new build context and add usage hint.
- Prefixed all COPY paths in the `deps` stage with `tttc-light-js-ollama/` (two package.json globs).
- Prefixed all source COPY paths in the `builder` stage with `tttc-light-js-ollama/` (common/ and next-client/).
- Added two COPY commands for auth stub patches after the source COPY block and before the `RUN npm run build` commands.
- Normalized comments from em-dashes/accented chars to ASCII dashes (matching plan spec).

**Discoveries:**
- The original Dockerfile had build context set to `tttc-poc/tttc-light-js-ollama/`, so all COPY paths were relative to that directory with no prefix. The new context is one level up (`tttc-poc/`), requiring the `tttc-light-js-ollama/` prefix on source paths and enabling direct access to `patches/`.
- The patch COPY lines for `auth.ts` and `getIdToken.ts` are correctly inserted between the ENV declarations and the `RUN npm run build` commands, so patches overwrite the real Firebase modules before the Next.js build runs.

**Committed:** `d882035` — plan-000006 step 2: atualizar Dockerfile.nextclient-poc para build context tttc-poc/

### Step 3 — 2026-05-24

**Status:** SUCCESS

**What was done:**
- Changed `next-client` service build block in `tttc-poc/docker-compose.yml`:
  - `context: ./tttc-light-js-ollama` → `context: .`
  - `dockerfile: ../Dockerfile.nextclient-poc` → `dockerfile: Dockerfile.nextclient-poc`
- All other fields (env_file, environment, ports, depends_on) left unchanged.
- Validated with `git diff`: exactly 2 lines changed, no unintended modifications.

**Discoveries:**
- `docker compose config` could not be run non-interactively in this environment (requires sudo + password), but file content was verified via Read and git diff.
- The change is symmetric with Step 2: the Dockerfile was already updated to expect `tttc-poc/` as its build context; the compose file now matches that expectation.

**Committed:** `872d5b7` — plan-000006 step 3: atualizar docker-compose.yml context do next-client para tttc-poc/