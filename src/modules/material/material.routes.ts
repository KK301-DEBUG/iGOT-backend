// material module - routes go here
import { FastifyInstance } from "fastify";
import {
  uploadMaterialHandler,
  listMaterialsHandler,
  getMaterialHandler,
} from "./material.controller";

export async function materialRoutes(app: FastifyInstance) {
  app.post("/upload", uploadMaterialHandler);
  app.get("/", listMaterialsHandler);
  app.get("/:id", getMaterialHandler);
}