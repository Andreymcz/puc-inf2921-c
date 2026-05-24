// PoC patch: retorna token fixo; verifyUser no express-server aceita qualquer string.
// NAO usar em producao. Substitui o modulo real getIdToken.ts via COPY no Dockerfile.nextclient-poc.
import { User } from "firebase/auth";
import { AsyncData, AsyncError } from "../hooks/useAsyncState";

export async function fetchToken(
  _user: User | null,
): Promise<AsyncData<string | null> | AsyncError<Error>> {
  return ["data", "poc-citizen-token"];
}