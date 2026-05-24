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