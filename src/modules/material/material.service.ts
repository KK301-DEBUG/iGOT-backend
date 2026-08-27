import pdfParse from "pdf-parse";
import { Material, IMaterial } from "./material.model";

export async function extractTextFromPdf(fileBuffer: Buffer): Promise<string> {
  const data = await pdfParse(fileBuffer);
  return data.text;
}

export async function saveMaterial(
  filename: string,
  extractedText: string,
  uploadedBy?: string
): Promise<IMaterial> {
  const material = new Material({ filename, extractedText, uploadedBy });
  return material.save();
}

export async function getMaterialById(id: string): Promise<IMaterial | null> {
  return Material.findById(id);
}

export async function listMaterials(): Promise<IMaterial[]> {
  return Material.find().sort({ createdAt: -1 });
}