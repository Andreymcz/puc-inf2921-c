// PoC patch: LocalFileStorage substitui GCS quando USE_LOCAL_STORAGE=true.
// Salva relatórios como JSON em /tmp/poc-reports/ dentro do container.

import * as fs from "fs";
import * as path from "path";
import * as schema from "tttc-common/schema";
import { z } from "zod";
import { Result } from "./types/result";
import { Env } from "./types/context";

const fileContent = z.union([schema.pipelineOutput, schema.uiReportData]);
type FileContent = z.infer<typeof fileContent>;

export abstract class Storage {
  abstract get(fileName: string): Promise<Result<FileContent, Error>>;
  abstract getUrl(fileName: string): Promise<Result<string, Error>>;
  abstract save(fileName: string, fileContent: string): Promise<Result<string, Error>>;
}

const LOCAL_REPORTS_DIR = process.env.LOCAL_REPORTS_DIR ?? "/tmp/poc-reports";

export class LocalFileStorage extends Storage {
  constructor() {
    super();
    fs.mkdirSync(LOCAL_REPORTS_DIR, { recursive: true });
  }

  async get(fileName: string): Promise<Result<FileContent, Error>> {
    const filePath = path.join(LOCAL_REPORTS_DIR, fileName);
    try {
      const raw = fs.readFileSync(filePath, "utf-8");
      const parsed = fileContent.safeParse(JSON.parse(raw));
      if (!parsed.success) return { ok: false, error: new Error(parsed.error.message) };
      return { ok: true, value: parsed.data };
    } catch (e) {
      return { ok: false, error: e as Error };
    }
  }

  async getUrl(fileName: string): Promise<Result<string, Error>> {
    // Serve via express-server /local-report/:name (adicionado no Step 3)
    return { ok: true, value: `/local-report/${encodeURIComponent(fileName)}` };
  }

  async save(fileName: string, content: string): Promise<Result<string, Error>> {
    const filePath = path.join(LOCAL_REPORTS_DIR, fileName);
    try {
      fs.writeFileSync(filePath, content, "utf-8");
      console.log(`[LOCAL] Saved report: ${filePath}`);
      return { ok: true, value: `/local-report/${encodeURIComponent(fileName)}` };
    } catch (e) {
      return { ok: false, error: e as Error };
    }
  }
}

// GCS Bucket — importado apenas quando não estamos em modo local
export class Bucket extends Storage {
  constructor(_encodedCreds: string, _bucketName: string) {
    super();
    throw new Error("GCS Bucket não disponível em modo PoC. Use USE_LOCAL_STORAGE=true.");
  }
  async get(_: string): Promise<Result<FileContent, Error>> { throw new Error("GCS unavailable"); }
  async getUrl(_: string): Promise<Result<string, Error>> { throw new Error("GCS unavailable"); }
  async save(_: string, __: string): Promise<Result<string, Error>> { throw new Error("GCS unavailable"); }
}

export const createStorage = (env: Env): Storage => {
  if (process.env.USE_LOCAL_STORAGE === "true") {
    console.log("📁 [LOCAL] Usando LocalFileStorage (USE_LOCAL_STORAGE=true)");
    return new LocalFileStorage();
  }
  return new Bucket(env.GOOGLE_CREDENTIALS_ENCODED!, env.GCLOUD_STORAGE_BUCKET!);
};