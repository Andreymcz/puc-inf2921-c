// PoC patch: stub Firebase — todas as operações são no-op em modo local.
// USE_LOCAL_STORAGE=true ativa este patch (montado via Docker volume no Step 3).

import {
  ReportJob,
  ReportRef,
  JobStatus,
  JOB_STATUS,
} from "tttc-common/firebase";

const USE_LOCAL = process.env.USE_LOCAL_STORAGE === "true";

// Quando não estamos em modo local, carregar o Firebase real.
// Isso evita carregar firebase-admin com credenciais inválidas.
let realFirebase: typeof import("./Firebase-real") | null = null;

if (!USE_LOCAL) {
  // Em produção real, substituir este arquivo pela versão original Firebase.ts
  // (renomeie o original para Firebase-real.ts e remova este bloco)
  console.warn("⚠️  Firebase.ts stub: USE_LOCAL_STORAGE não está ativo. Firebase desativado.");
}

export async function addReportRef(id: string, reportRef: ReportRef): Promise<string> {
  if (!USE_LOCAL) throw new Error("Firebase not configured for PoC. Set USE_LOCAL_STORAGE=true.");
  console.log(`[LOCAL] addReportRef: ${id}`);
  return id;
}

export async function addReportJob(job: Omit<ReportJob, "id"> & { id?: string }): Promise<string> {
  if (!USE_LOCAL) throw new Error("Firebase not configured for PoC. Set USE_LOCAL_STORAGE=true.");
  const id = job.id ?? Math.random().toString(36).slice(2);
  console.log(`[LOCAL] addReportJob: ${id}`);
  return id;
}

export async function updateReportJob(
  id: string,
  update: Partial<ReportJob>,
): Promise<void> {
  if (!USE_LOCAL) throw new Error("Firebase not configured for PoC. Set USE_LOCAL_STORAGE=true.");
  console.log(`[LOCAL] updateReportJob: ${id}`, update);
}

export async function getReportJob(id: string): Promise<ReportJob | null> {
  if (!USE_LOCAL) throw new Error("Firebase not configured for PoC. Set USE_LOCAL_STORAGE=true.");
  console.log(`[LOCAL] getReportJob: ${id}`);
  return null;
}

export async function verifyIdToken(token: string): Promise<{ uid: string }> {
  if (!USE_LOCAL) throw new Error("Firebase not configured for PoC. Set USE_LOCAL_STORAGE=true.");
  // PoC: qualquer token é aceito; auth não é validada
  return { uid: "poc-user" };
}
