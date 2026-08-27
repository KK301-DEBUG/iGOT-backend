import { FastifyRequest, FastifyReply } from "fastify";
import mongoose from "mongoose";
import { extractTextFromPdf, saveMaterial, listMaterials, getMaterialById } from "./material.service";

export async function uploadMaterialHandler(req: FastifyRequest, reply: FastifyReply) {
  try {
    const file = await req.file();

    if (!file) {
      return reply.status(400).send({ error: "No file uploaded" });
    }

    if (file.mimetype !== "application/pdf") {
      return reply.status(400).send({ error: "Only PDF files are supported right now" });
    }

    const fileBuffer = await file.toBuffer();
    const extractedText = await extractTextFromPdf(fileBuffer);

    if (!extractedText || extractedText.trim().length === 0) {
      return reply.status(422).send({ error: "Could not extract any text from this PDF" });
    }

    const material = await saveMaterial(file.filename, extractedText); 

    return reply.status(201).send({
      id: material.id,
      filename: material.filename,
      textPreview: extractedText.slice(0, 300),
      textLength: extractedText.length,
    });
  } catch (err) {
    if (
      typeof err === "object" &&
      err !== null &&
      "code" in err &&
      err.code === "FST_INVALID_MULTIPART_CONTENT_TYPE"
    ) {
      return reply.status(400).send({ error: "Content-Type must be multipart/form-data" });
    }

    req.log.error(err);
    return reply.status(500).send({ error: "Failed to process the uploaded file" });
  }
}

export async function listMaterialsHandler(req: FastifyRequest, reply: FastifyReply) {
  try {
    const materials = await listMaterials();
    return reply.send(
      materials.map((m) => ({
        id: m.id,
        filename: m.filename,
        textLength: m.extractedText.length,
        createdAt: m.createdAt,
      }))
    );
  } catch (err) {
    req.log.error(err);
    return reply.status(500).send({ error: "Failed to list materials" });
  }
}

export async function getMaterialHandler(
  req: FastifyRequest<{ Params: { id: string } }>,
  reply: FastifyReply
) {
  if (!mongoose.isValidObjectId(req.params.id)) {
    return reply.status(400).send({ error: "Invalid material ID" });
  }

  try {
    const material = await getMaterialById(req.params.id);
    if (!material) {
      return reply.status(404).send({ error: "Material not found" });
    }
    return reply.send(material);
  } catch (err) {
    req.log.error(err);
    return reply.status(500).send({ error: "Failed to retrieve material" });
  }
}