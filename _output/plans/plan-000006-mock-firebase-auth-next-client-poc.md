# DONE | 2026-05-24 23:30 UTC | Plan 000006 | FIX-F | 2026-05-24 21:34 UTC | Mock Firebase Auth no next-client para PoC citizen user | Review: Light
plan_format_version: 1
source: research-000005 -- Firebase Auth stub necessario para criar relatorios na PoC

## User Brief

from research 5

## Agent Interpretation

**Problem:** O site da PoC abre em `localhost:3000`, mas o formulario de criacao de relatorio
exige login via Firebase. As credenciais Firebase sao stubs (`poc-local-key` etc.) e o
`signInWithPopup` falha ao tentar contatar o Google OAuth real. Sem usuario logado e sem token,
o formulario fica desabilitado (`isDisabled = !token`) e o submit falha.

**Approach:** Criar dois arquivos de patch TypeScript que substituem os modulos Firebase Auth
do next-client por stubs que emitem automaticamente um usuario "citizen" ficticio sem fazer
nenhum request externo. Atualizar o `Dockerfile.nextclient-poc` para seguir o mesmo padrao
do `Dockerfile.express-poc`: mudar o build context para `tttc-poc/` (que inclui `patches/`)
e prefixar todos os COPY com `tttc-light-js-ollama/`. Atualizar o `docker-compose.yml` para
refletir o novo build context.

**Root cause identified in research-000005:**
O `Dockerfile.nextclient-poc` usa build context `./tttc-light-js-ollama`, que nao inclui o
diretorio `patches/`. A correcao alinha com o padrao ja estabelecido pelo `Dockerfile.express-poc`
(context: `.`, paths prefixados com `tttc-light-js-ollama/`).

**Alternatives rejected:**
- Copiar patches para dentro de `tttc-light-js-ollama/`: polui o clone do repositorio externo.
- Usar `volumes` em docker-compose para sobrescrever em runtime: incompativel com build estatico
  do Next.js (os modulos sao embutidos no bundle em build time, nao em runtime).

## Files

- `tttc-poc/patches/next-client/src/lib/firebase/auth.ts` -- create (stub onAuthStateChanged)
- `tttc-poc/patches/next-client/src/lib/firebase/getIdToken.ts` -- create (stub fetchToken)
- `tttc-poc/Dockerfile.nextclient-poc` -- modify (build context e COPY patches)
- `tttc-poc/docker-compose.yml` -- modify (next-client build context: . em vez de ./tttc-light-js-ollama)

## Best Practices

- Seguir o padrao `Dockerfile.express-poc`: context `tttc-poc/`, paths prefixados com `tttc-light-js-ollama/`
- Patches ficam em `patches/next-client/` espelhando a estrutura de `patches/express-server/`
- Comentarios nos patches marcam explicitamente que sao PoC-only e nao devem ir para producao
- Sem alteracoes nos arquivos de fonte originais em `tttc-light-js-ollama/`

## Design Decisions

**Build context unificado:** Mudar o build context de `./tttc-light-js-ollama` para `.` (tttc-poc/)
alinha o `Dockerfile.nextclient-poc` com o `Dockerfile.express-poc` e permite COPY de `patches/`.
O custo e que todos os COPY precisam do prefixo `tttc-light-js-ollama/`, o que e explicitado nos
comentarios do Dockerfile como documentacao de intencao.

**Stub via modulo substituido, nao monkey-patch:** Substituir o arquivo inteiro e mais simples e
previsivel do que tentar envolver ou interceptar o modulo original -- ja e o padrao usado pelos
patches do express-server.

---

## Steps

### Step 1: Criar os arquivos de patch TypeScript para auth stub

Criar os dois arquivos de patch que substituem os modulos Firebase Auth do next-client por stubs
de PoC. O stub de `auth.ts` implementa `onAuthStateChanged` emitindo automaticamente um usuario
ficticio `CITIZEN_USER` via `setTimeout`, sem fazer nenhum request externo. O stub de
`getIdToken.ts` implementa `fetchToken` retornando um token fixo `"poc-citizen-token"`.

O fluxo que isso desbloqueia:
1. `useUser()` chama `onAuthStateChanged(callback)` no `useEffect`
2. O stub chama `callback(CITIZEN_USER)` via `setTimeout` -> `setUser(CITIZEN_USER)`
3. `fetchToken` retorna `["data", "poc-citizen-token"]` -> `isDisabled = !token` avalia como false
4. Submit envia token para express-server -> `verifyUser` (ja patchado) aceita qualquer token

**Criar `tttc-poc/patches/next-client/src/lib/firebase/auth.ts`:**

```typescript
// PoC patch: stub Firebase Auth -- auto-loga como 'citizen' sem credenciais reais.
// NAO usar em producao. Substitui o modulo real auth.ts via COPY no Dockerfile.nextclient-poc.
import { User } from "firebase/auth";

const CITIZEN_USER = {
  uid: "citizen",
  displayName: "Citizen",
  email: "citizen@poc.local",
  photoURL: null,
  getIdToken: async () => "poc-citizen-token",
} as unknown as User;

export function onAuthStateChanged(callback: (user: User | null) => void) {
  setTimeout(() => callback(CITIZEN_USER), 0);
  return () => {};
}

export async function signInWithGoogle(): Promise<void> {}

export async function signOut(): Promise<void> {}
```

**Criar `tttc-poc/patches/next-client/src/lib/firebase/getIdToken.ts`:**

```typescript
// PoC patch: retorna token fixo; verifyUser no express-server aceita qualquer string.
// NAO usar em producao. Substitui o modulo real getIdToken.ts via COPY no Dockerfile.nextclient-poc.
import { User } from "firebase/auth";
import { AsyncData, AsyncError } from "../hooks/useAsyncState";

export async function fetchToken(
  _user: User | null,
): Promise<AsyncData<string | null> | AsyncError<Error>> {
  return ["data", "poc-citizen-token"];
}
```

- **Files**: `tttc-poc/patches/next-client/src/lib/firebase/auth.ts` (create), `tttc-poc/patches/next-client/src/lib/firebase/getIdToken.ts` (create)
- **References**: N/A
- **Interface**: N/A
- **Verify**: Os dois arquivos existem com o conteudo correto; TypeScript compila sem erros (verificado no step 3 via docker build)
- **Tests**: N/A (PoC patch -- sem test harness no tttc-poc)
- [x] Done

---

### Step 2: Atualizar Dockerfile.nextclient-poc para usar build context tttc-poc/

Reescrever `tttc-poc/Dockerfile.nextclient-poc` para seguir o padrao do `Dockerfile.express-poc`:
- Cabecalho atualizado para refletir o novo build context (`tttc-poc/`)
- Todos os `COPY` no estagio `deps` prefixados com `tttc-light-js-ollama/`
- Todos os `COPY` no estagio `builder` prefixados com `tttc-light-js-ollama/`
- Adicionar dois `COPY` dos patches **apos** os COPY de fonte e **antes** dos `RUN npm run build`

O novo conteudo do estagio `builder` (apos as linhas de COPY existentes e antes dos RUN build):

```dockerfile
# PoC: auth stub patches -- substituem modulos Firebase para login automatico como 'citizen'.
COPY patches/next-client/src/lib/firebase/auth.ts ./next-client/src/lib/firebase/auth.ts
COPY patches/next-client/src/lib/firebase/getIdToken.ts ./next-client/src/lib/firebase/getIdToken.ts
```

**Conteudo completo esperado do Dockerfile.nextclient-poc apos esta etapa:**

```dockerfile
# PoC Dockerfile for next-client -- aplica patches de auth antes do build.
# Build context: tttc-poc/ (inclui patches/ e tttc-light-js-ollama/).
# Usage: docker compose build next-client

# syntax=docker.io/docker/dockerfile:1
FROM node:18-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY tttc-light-js-ollama/common/package*.json ./common/
COPY tttc-light-js-ollama/next-client/package*.json ./next-client/
RUN npm ci --prefix ./common --frozen-lockfile
RUN npm ci --prefix ./next-client --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/common/node_modules ./common/node_modules
COPY --from=deps /app/next-client/node_modules ./next-client/node_modules
COPY tttc-light-js-ollama/common/ ./common/
COPY tttc-light-js-ollama/next-client/ ./next-client/

# PoC: Firebase client stubs -- qualquer valor nao-vazio satisfaz a validacao Zod.
ARG NEXT_PUBLIC_FIREBASE_API_KEY=poc-local-key
ARG NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=poc-local.firebaseapp.com
ARG NEXT_PUBLIC_FIREBASE_PROJECT_ID=poc-local
ARG NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=poc-local.appspot.com
ARG NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=000000000000
ARG NEXT_PUBLIC_FIREBASE_APP_ID=1:000000000000:web:poc000000000000

ENV NEXT_PUBLIC_FIREBASE_API_KEY=$NEXT_PUBLIC_FIREBASE_API_KEY
ENV NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=$NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
ENV NEXT_PUBLIC_FIREBASE_PROJECT_ID=$NEXT_PUBLIC_FIREBASE_PROJECT_ID
ENV NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=$NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
ENV NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=$NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
ENV NEXT_PUBLIC_FIREBASE_APP_ID=$NEXT_PUBLIC_FIREBASE_APP_ID

# PoC: auth stub patches -- substituem modulos Firebase para login automatico como 'citizen'.
# NAO usar em producao.
COPY patches/next-client/src/lib/firebase/auth.ts ./next-client/src/lib/firebase/auth.ts
COPY patches/next-client/src/lib/firebase/getIdToken.ts ./next-client/src/lib/firebase/getIdToken.ts

RUN npm run build --prefix ./common
RUN npm run build --prefix ./next-client

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/next-client/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/next-client/next.config.js ./
COPY --from=builder --chown=nextjs:nodejs /app/next-client/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/next-client/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/common ./node_modules/tttc-common
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1
EXPOSE 3000
USER nextjs
CMD ["node", "server.js"]
```

- **Files**: `tttc-poc/Dockerfile.nextclient-poc` (modify)
- **References**: N/A
- **Depends on**: Step 1
- **Interface**: N/A
- **Verify**: `docker compose build next-client` (a partir do diretorio `tttc-poc/`) conclui sem erros de COPY ou TypeScript
- **Tests**: N/A (build Docker e o teste de compilacao)
- [x] Done

---

### Step 3: Atualizar docker-compose.yml -- build context do next-client

Alterar o campo `context` do servico `next-client` no `tttc-poc/docker-compose.yml` de
`./tttc-light-js-ollama` para `.` para que o Docker passe `tttc-poc/` como build context,
tornando `patches/` acessivel durante o build.

```yaml
  next-client:
    build:
      context: .
      dockerfile: Dockerfile.nextclient-poc
```

O campo `dockerfile: ../Dockerfile.nextclient-poc` tambem muda para `dockerfile: Dockerfile.nextclient-poc`
porque com o novo context (`.` = `tttc-poc/`), o Dockerfile esta no proprio context.

- **Files**: `tttc-poc/docker-compose.yml` (modify)
- **References**: N/A
- **Depends on**: Step 2
- **Interface**: N/A
- **Verify**: `docker compose config` nao emite warnings sobre contexto; `docker compose build next-client` usa o contexto correto
- **Tests**: N/A
- [x] Done

---

### Step 4: Rebuild e smoke test -- verificar login como citizen

Com os patches e Dockerfiles atualizados, fazer o rebuild e verificar que a PoC funciona de ponta a ponta com login automatico.

**Comandos (a partir do diretorio `tttc-poc/`):**

```bash
# Rebuild apenas o next-client (os outros servicos nao mudaram)
docker compose build next-client

# Subir (ou reiniciar) o stack
docker compose up -d

# Verificar logs (aguardar "Ready" do Next.js)
docker compose logs -f next-client
```

**Verificacoes no browser (`http://localhost:3000`):**
1. O avatar ou nome "Citizen" aparece na navbar (confirma que `useUser()` recebeu `CITIZEN_USER`)
2. O formulario "Create Report" esta habilitado (`isDisabled = !token` == false)
3. Submeter um relatorio de teste com o CSV de amostra nao retorna erro de autenticacao

- **Files**: N/A (step de verificacao, sem alteracoes em arquivo)
- **References**: N/A
- **Depends on**: Step 3
- **Interface**: N/A
- **Verify**: Browser mostra nome "Citizen" na navbar e formulario de criacao de relatorio habilitado; submit nao retorna "You need to be logged in"
- **Tests**: N/A (verificacao manual -- PoC sem test harness)
- [x] Done

---

## Review: Light

**Perspectives evaluated:**

| Tag | Finding | Status |
|-----|---------|--------|
| SEC | Stubs marcados explicitamente como PoC-only com comentarios "NAO usar em producao". Nenhuma credencial real exposita. O token ficticio "poc-citizen-token" e aceito pelo express-server (ja patchado) sem impacto fora do ambiente Docker local. | Adopted |
| OPS | Alinhamento com o padrao Dockerfile.express-poc reduz inconsistencia operacional. Mudanca de build context aumenta levemente o tamanho do contexto enviado ao Docker daemon (inclui patches/), mas o impacto e desprezivel (arquivos pequenos). | Adopted |
| ARCH | Patches isolados em `patches/next-client/` seguindo a mesma estrutura de `patches/express-server/`. Nenhum arquivo do repositorio externo `tttc-light-js-ollama/` e modificado. Separacao limpa entre fonte original e overrides de PoC. | Adopted |
| TEST | N/A -- tttc-poc nao tem test harness. A verificacao e manual (smoke test no browser). | N/A |
| DX | Comentarios no Dockerfile documentam o build context e o proposito dos patches. Consistencia com o padrao express-poc reduz a carga cognitiva para quem trabalha nos dois Dockerfiles. | Adopted |

**Conclusion:** Nenhum bloqueio identificado. O plano esta aprovado para implementacao.

---

## Commit Message

```
fix(tttc-poc): stub Firebase Auth no next-client para PoC citizen user

Cria patches/next-client com stubs de onAuthStateChanged e fetchToken
que emitem automaticamente o usuario 'citizen' sem credenciais reais.

Atualiza Dockerfile.nextclient-poc e docker-compose.yml para seguir o
padrao do Dockerfile.express-poc: build context tttc-poc/, COPY paths
prefixados com tttc-light-js-ollama/, patches aplicados antes do build.
```

---

## Summary

**Steps completed:** 4/4 | **Iterations used:** 4 + debugging pos-plano

**Changes beyond the original plan scope** (bugs descobertos durante smoke test):

- `tttc-poc/Dockerfile.pyserver-poc` (criado): pyserver crashava com `ImportError: attempted relative import with no known parent package`. Novo Dockerfile corrige imports relativos de `main.py` em build-time via heredoc Python e copia `json_response_parser.py` do diretorio de testes.
- `tttc-poc/docker-compose.yml`: pyserver agora usa `context: .` + `Dockerfile.pyserver-poc`; express-server recebeu `PORT: "8080"` override (o `PORT=8000` do `.env.poc` destinado ao pyserver estava sendo herdado pelo express-server, causando `ECONNREFUSED` no next-client).
- `tttc-poc/Makefile` (criado): targets para todo o ciclo de vida da PoC (build, up, logs, stop, clean, rebuild por servico, pull-model).
- `patches/express-server/src/routes/report.ts` (criado): `getReportDataHandler` sempre instanciava `new Bucket()` que e um stub que joga excecao em modo PoC; o fallback tentava uma URL GCS publica que retornava 403. O patch curto-circuita para `createStorage().getUrl()` e retorna URL absoluta `http://express-server:8080/local-report/{hash}`.
- `patches/express-server/src/server.ts` (criado): adiciona rota `GET /local-report/*` como `express.static` servindo de `LOCAL_REPORTS_DIR` para que next-client possa buscar o JSON do relatorio.
- `Dockerfile.express-poc`: atualizado para copiar os dois novos patches de express-server.

**Resultado final verificado:** submit de relatorio de ponta a ponta funcionando -- login automatico como "citizen", pyserver gera o relatorio via Ollama, express-server salva localmente, next-client renderiza o relatorio.
