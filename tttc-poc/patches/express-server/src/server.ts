// PoC patch: adiciona rota GET /local-report/:file para servir arquivos de LOCAL_REPORTS_DIR.
// NAO usar em producao. Substitui src/server.ts via COPY no Dockerfile.express-poc.

import "dotenv/config";
import express from "express";
import rateLimit from "express-rate-limit";
import cors from "cors";
import create from "./routes/create";
import { validateEnv } from "./types/context";
import { contextMiddleware } from "./middleware";
import { setupWorkers } from "./workers";
import { getReportStatusHandler, getReportDataHandler } from "./routes/report";
import { setupConnection } from "./Queue";
import path from "path";
import fs from "fs";

const port = process.env.PORT || 8080;

const env = validateEnv();

const app = express();
app.use(cors());
// Required to use express-rate-limit with CloudRun, but doesn't apply to local
if (process.env.NODE_ENV === "production") {
  // Could be its own env var, but correct for now.
  app.set("trust proxy", 1);
}
app.use(express.json({ limit: "50mb" }));
app.use(express.static("public"));

// Adds context middleware - lets us pass things like env variables
app.use(contextMiddleware(env));

const { connection, pipelineQueue: plq } = setupConnection(env);

export const pipelineQueue = plq;

// This is added here so that the worker gets initialized. Queue is referenced in /create, so its initialized there.
const _ = setupWorkers(connection);

// PoC: serve report files from local filesystem when USE_LOCAL_STORAGE=true.
if (process.env.USE_LOCAL_STORAGE === "true") {
  const LOCAL_REPORTS_DIR = process.env.LOCAL_REPORTS_DIR ?? "/tmp/poc-reports";
  fs.mkdirSync(LOCAL_REPORTS_DIR, { recursive: true });
  app.use("/local-report", express.static(LOCAL_REPORTS_DIR));
  console.log(`📁 [LOCAL] Servindo /local-report a partir de ${LOCAL_REPORTS_DIR}`);
}

const defaultRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: {
      message: "Too many requests, please try again later.",
      code: "RateLimitExceeded",
    },
  },
});

/**
 * Creates report
 */
app.post("/create", defaultRateLimiter, create);

/**
 * Gets a report
 */
app.get(
  "/report/:reportUri/status",
  defaultRateLimiter,
  getReportStatusHandler,
);
app.get("/report/:reportUri/data", defaultRateLimiter, getReportDataHandler);

app.get("/test", async (req, res) => {
  return res.send("hi");
});

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});