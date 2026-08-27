import multipart from "@fastify/multipart";
import { materialRoutes } from "./modules/material/material.routes";
import Fastify, { FastifyInstance } from "fastify";
import cors from "@fastify/cors";

export function buildApp(): FastifyInstance {
  const app = Fastify({
    logger: {
      transport: {
        target: "pino-pretty",
      },
    },
  });

  app.register(cors, { origin: "*" });
  app.register(multipart, {
  limits: { fileSize: 10 * 1024 * 1024 },
});

 app.get("/health", async () => {
  return { status: "ok", version: "v2-test" };
});
  app.register(materialRoutes, { prefix: "/api/material" });

  // Module routes will be registered here as they're built, e.g.:
  // app.register(materialRoutes, { prefix: "/api/material" });
  // app.register(quizRoutes, { prefix: "/api/quiz" });
  // app.register(competencyRoutes, { prefix: "/api/competency" });
  // app.register(igotRoutes, { prefix: "/api/igot" });

  return app;
}
