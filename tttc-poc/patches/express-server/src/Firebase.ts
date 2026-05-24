// PoC patch: stub Firebase — todas as operações são no-op em modo local.
// Substitui o Firebase.ts original; mantém a mesma API pública exportada.

import {
  ReportJob,
  ReportRef,
  JobStatus,
  JOB_STATUS,
} from "tttc-common/firebase";

export class JobNotFoundError extends Error {
  constructor(message = "Job not found") {
    super(message);
    this.name = "JobNotFoundError";
  }
}

export async function addReportRef(id: string, _reportRef: ReportRef): Promise<string> {
  console.log(`[LOCAL] addReportRef: ${id}`);
  return id;
}

export async function addReportJob({
  status = JOB_STATUS.PENDING,
  createdAt = new Date(),
  ...jobDetails
}: ReportJob): Promise<string> {
  const id = Math.random().toString(36).slice(2);
  console.log(`[LOCAL] addReportJob: ${id}`, { status, ...jobDetails });
  return id;
}

export async function updateReportJobStatus(
  jobId: string,
  status: JobStatus,
): Promise<void> {
  console.log(`[LOCAL] updateReportJobStatus: ${jobId} → ${status}`);
}

// verifyUser: em modo PoC aceita qualquer token e retorna um usuário stub.
// Se o next-client não enviar token, create.ts receberá null e lançará erro —
// nesse caso é necessário também patchear create.ts para bypassar auth.
export async function verifyUser(_token: string): Promise<{ uid: string }> {
  console.log("[LOCAL] verifyUser: retornando poc-user stub");
  return { uid: "poc-user" };
}
