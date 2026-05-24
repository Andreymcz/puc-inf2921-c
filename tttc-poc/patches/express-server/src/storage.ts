// PoC patch: LocalFileStorage substitui GCS quando USE_LOCAL_STORAGE=true.
// Mantém a mesma API pública de storage.ts (Storage abstract, Bucket, createStorage).
// Result usa { tag: "success"/"failure" } conforme ./types/result/index.ts.

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
      if (!parsed.success) {
        return { tag: "failure", error: new Error(parsed.error.message) };
      }
      return { tag: "success", value: parsed.data };
    } catch (e) {
      return { tag: "failure", error: e as Error };
    }
  }

  async getUrl(fileName: string): Promise<Result<string, Error>> {
    return { tag: "success", value: `/local-report/${encodeURIComponent(fileName)}` };
  }

  async save(fileName: string, content: string): Promise<Result<string, Error>> {
    const filePath = path.join(LOCAL_REPORTS_DIR, fileName);
    try {
      fs.writeFileSync(filePath, content, "utf-8");
      console.log(`[LOCAL] Saved report: ${filePath}`);
      return { tag: "success", value: `/local-report/${encodeURIComponent(fileName)}` };
    } catch (e) {
      return { tag: "failure", error: e as Error };
    }
  }
}

// Stub de Bucket para manter compatibilidade com report.ts que importa { Bucket }.
// Bucket.parseUri é usado em report.ts para extrair bucket+fileName da URI retornada por save.
export class Bucket extends Storage {
  // Regex que suporta URIs /local-report/{fileName} além de GCS URLs.
  static VALID_FILENAME_REGEX = /^[^(\r\n#\[\]*?\:"<>|)]+$/;
  static MAX_FILENAME_LENGTH = 512;

  constructor(_encodedCreds: string, _bucketName: string) {
    super();
    throw new Error("GCS Bucket não disponível em modo PoC. Use USE_LOCAL_STORAGE=true.");
  }

  async get(_: string): Promise<Result<FileContent, Error>> {
    throw new Error("GCS unavailable in PoC mode");
  }
  async getUrl(_: string): Promise<Result<string, Error>> {
    throw new Error("GCS unavailable in PoC mode");
  }
  async save(_: string, __: string): Promise<Result<string, Error>> {
    throw new Error("GCS unavailable in PoC mode");
  }

  static isValidFileName(fileName: string | undefined): boolean {
    return (
      typeof fileName === "string" &&
      fileName.length > 0 &&
      fileName.length <= Bucket.MAX_FILENAME_LENGTH &&
      Bucket.VALID_FILENAME_REGEX.test(fileName) &&
      !fileName.includes("..") &&
      !fileName.includes("/") &&
      fileName !== "index.js"
    );
  }

  // Em modo local, a URI retornada por save é /local-report/{encodedFileName}.
  // parseUri extrai o fileName original para que report.ts possa chamá-lo.
  static parseUri(
    uri: string,
    defaultBucket: string,
  ): Result<{ bucket: string; fileName: string }, Error> {
    // Formato local: /local-report/{encodeURIComponent(fileName)}
    const localPrefix = "/local-report/";
    if (uri.startsWith(localPrefix)) {
      const fileName = decodeURIComponent(uri.slice(localPrefix.length));
      return { tag: "success", value: { bucket: "local", fileName } };
    }

    // Filename simples (sem path separator)
    if (Bucket.isValidFileName(uri)) {
      return { tag: "success", value: { bucket: defaultBucket, fileName: uri } };
    }

    // GCS URL: https://storage.googleapis.com/bucket/file
    try {
      const url = new URL(uri);
      if (url.hostname === "storage.googleapis.com") {
        const [, bucket, ...fileParts] = url.pathname.split("/");
        if (bucket && fileParts.length > 0) {
          return {
            tag: "success",
            value: { bucket, fileName: decodeURIComponent(fileParts.join("/")) },
          };
        }
      }
    } catch {
      // não é uma URL válida
    }

    return { tag: "failure", error: new Error("Invalid or unsupported URI") };
  }
}

export const createStorage = (env: Env): Storage => {
  if (process.env.USE_LOCAL_STORAGE === "true") {
    console.log("📁 [LOCAL] Usando LocalFileStorage (USE_LOCAL_STORAGE=true)");
    return new LocalFileStorage();
  }
  return new Bucket(env.GOOGLE_CREDENTIALS_ENCODED!, env.GCLOUD_STORAGE_BUCKET!);
};
