import "dotenv/config";
import { z } from "zod";

declare global {
  namespace Express {
    interface Request {
      context: {
        env: Env;
      };
    }
  }
}

class EnvValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.stack = "";
    this.name = "";
  }
}

// PoC patch: USE_LOCAL_STORAGE=true bypasses Firebase/GCS credential requirements.
const useLocalStorage = process.env.USE_LOCAL_STORAGE === "true";

export const env = z.object({
  OPENAI_API_KEY: z.string({ required_error: "Missing OpenAI Key" }),
  OPENAI_API_KEY_PASSWORD: z.string().optional(),
  GCLOUD_STORAGE_BUCKET: useLocalStorage
    ? z.string().optional().default("local")
    : z.string({ required_error: "Missing GCloud storage bucket" }),
  GOOGLE_CREDENTIALS_ENCODED: useLocalStorage
    ? z.string().optional().default("")
    : z.string({ required_error: "Missing encoded GCloud credentials" }),
  FIREBASE_CREDENTIALS_ENCODED: useLocalStorage
    ? z.string().optional().default("")
    : z.string({ required_error: "Missing encoded Firebase credentials" }),
  CLIENT_BASE_URL: z.string({ required_error: "Missing CLIENT_BASE_URL" }).url(),
  PYSERVER_URL: z.string({ required_error: "Missing PYSERVER_URL" }).url(),
  NODE_ENV: z.union([z.literal("development"), z.literal("production")], {
    required_error: "Missing NODE_ENV",
    invalid_type_error: "Invalid input for NODE_ENV",
  }),
  FIREBASE_DATABASE_URL: useLocalStorage
    ? z.string().optional().default("https://poc-local.firebaseio.com/")
    : z.string({ required_error: "Missing FIREBASE_DATABASE_URL" }).url(),
  REDIS_URL: z.string({ required_error: "Missing REDIS_URL" }),
  ALLOWED_GCS_BUCKETS: z.string().optional().default("local").transform((val) => val.split(",")),
  USE_LOCAL_STORAGE: z.string().optional().default("false"),
});

export type Env = z.infer<typeof env>;

export function validateEnv(): Env {
  const parsed = env.safeParse(process.env);
  if (parsed.success === false) {
    throw new EnvValidationError(
      `❌ Invalid environment variables: \n\n${parsed.error.errors
        .map((e, i) => `${i}) ${e.message} \n`)
        .join("")}`,
    );
  }
  return parsed.data;
}
