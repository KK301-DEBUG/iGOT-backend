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

  app.register(cors, { origin: "*" }); // tighten this before production

  app.get("/health", async () => {
    return { status: "ok" };
  });

  // Module routes will be registered here as they're built, e.g.:
  // app.register(materialRoutes, { prefix: "/api/material" });
  // app.register(quizRoutes, { prefix: "/api/quiz" });
  // app.register(competencyRoutes, { prefix: "/api/competency" });
  // app.register(igotRoutes, { prefix: "/api/igot" });

  return app;
}
