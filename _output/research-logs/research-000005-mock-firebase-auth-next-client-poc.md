# Research 000005 | FIX-F | 2026-05-24 21:28 UTC | Mock Firebase Auth no next-client para PoC citizen user

tags: firebase-auth, mock-stub, poc, next-client, authentication
spawned: plan-000006

## User Brief

o step 3 do plano 1 esta pronto. abri o site em localhost:3000. para fazer um report precico fazer o login. mas nos desabilidamos o login do firebase, e agora ? sera que conseguimos mockar ? criamos um usuario 'citizen' que sera usado na hora do login.

## Agent Interpretation

O usuario completou o step 3 do plan-000001 (docker-compose.yml para PoC TRL 3 com Ollama local). O site esta no ar em localhost:3000, mas o formulario de criacao de relatorio exige login (Firebase Auth). Como as credenciais Firebase sao stubs (poc-local-key etc.) e o Google Auth nao esta configurado, signInWithPopup falha. O objetivo e mockar a autenticacao no next-client para que o app abra ja logado como um usuario ficticio "citizen", sem precisar de credenciais reais.

## Files

- `tttc-poc/tttc-light-js-ollama/next-client/src/lib/firebase/auth.ts` -- modulo real de auth (alvo do patch)
- `tttc-poc/tttc-light-js-ollama/next-client/src/lib/firebase/getIdToken.ts` -- modulo de token (alvo do patch)
- `tttc-poc/tttc-light-js-ollama/next-client/src/lib/hooks/getUser.ts` -- hook useUser() que chama onAuthStateChanged
- `tttc-poc/tttc-light-js-ollama/next-client/src/components/create/CreateReport.tsx` -- linha 224: isDisabled = !token
- `tttc-poc/tttc-light-js-ollama/next-client/src/features/submission/actions/SubmitAction.ts` -- verifica token != null
- `tttc-poc/patches/express-server/src/Firebase.ts` -- verifyUser ja aceita qualquer token (ja mockado)
- `tttc-poc/Dockerfile.nextclient-poc` -- precisa de novos COPY para os patches

---

## Q&A Log

**Q1:** O step 3 do plano 1 esta pronto. O site abre em localhost:3000 mas nao consigo fazer login para criar o report. O Firebase esta desabilitado (credentials stub). Criamos um usuario 'citizen'. Conseguimos mockar o login?

**A1:** Sim, e a abordagem correta para a PoC. O bloqueio esta inteiramente no next-client: o express-server ja foi patchado e aceita qualquer token via verifyUser(). Faltam dois patches no next-client.

**Diagnostico completo:**

O fluxo de criacao de relatorio exige:
1. Usuario logado: `useUser()` retorna `user != null`
2. Token nao-nulo: `fetchToken(user)` retorna uma string
3. Formulario habilitado: `!token` em CreateReport.tsx:224 precisa ser false
4. Submit: `submitAction` verifica `if (!firebaseAuthToken) throw Error("You need to be logged in")`
5. Express-server: recebe o token e chama `verifyUser(token)` -- ja patchado, aceita tudo

O problema: `signInWithGoogle()` chama `signInWithPopup(auth, GoogleAuthProvider)` com credenciais stub. O Firebase SDK tenta fazer um request real ao Google OAuth e falha porque `poc-local-key` nao e valido.

**Solucao: tres patches**

**Patch 1** -- `patches/next-client/src/lib/firebase/auth.ts`:
Stub que auto-emite o usuario 'citizen' via onAuthStateChanged, sem chamar Firebase real.

```typescript
// PoC patch: stub Firebase Auth -- auto-loga como 'citizen' sem credenciais reais.
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

**Patch 2** -- `patches/next-client/src/lib/firebase/getIdToken.ts`:
Retorna token fixo; o express-server aceita qualquer string.

```typescript
// PoC patch: retorna token fixo; verifyUser no express-server aceita qualquer string.
import { User } from "firebase/auth";
import { AsyncData, AsyncError } from "../hooks/useAsyncState";

export async function fetchToken(
  _user: User | null,
): Promise<AsyncData<string | null> | AsyncError<Error>> {
  return ["data", "poc-citizen-token"];
}
```

**Patch 3** -- `Dockerfile.nextclient-poc`:
Adicionar dois COPY no estagio builder, antes do `RUN npm run build`:

```dockerfile
# PoC: auth stub patches
COPY patches/next-client/src/lib/firebase/auth.ts ./next-client/src/lib/firebase/auth.ts
COPY patches/next-client/src/lib/firebase/getIdToken.ts ./next-client/src/lib/firebase/getIdToken.ts
```

**Por que funciona:**
- `useUser()` chama `onAuthStateChanged(callback)` no useEffect
- O patch chama callback(CITIZEN_USER) via setTimeout, emitindo o usuario citizen automaticamente
- `setUser(CITIZEN_USER)` popula o estado -- app aparece "logado" como Citizen
- `fetchToken` retorna "poc-citizen-token" sem chamar `user.getIdToken()`
- `isDisabled` avalia `!token` como false -- formulario habilitado
- Express-server recebe "poc-citizen-token", verifyUser retorna { uid: "poc-user" } -- ok

**Nota de segurança:** Estes patches sao apenas para a PoC TRL 3. Nao devem ir para producao. O usuario 'citizen' nao tem controle de acesso real.

---

## Recommendations Summary

| Priority | Recommendation |
|----------|---------------|
| HIGH | Adicionar patch `patches/next-client/src/lib/firebase/auth.ts` com stub de onAuthStateChanged que emite CITIZEN_USER automaticamente |
| HIGH | Adicionar patch `patches/next-client/src/lib/firebase/getIdToken.ts` que retorna "poc-citizen-token" fixo |
| HIGH | Atualizar `Dockerfile.nextclient-poc` para copiar os dois novos patches antes do build |
| MEDIUM | Apos rebuild, verificar que o avatar "Citizen" aparece na navbar e o formulario de criacao esta habilitado |
