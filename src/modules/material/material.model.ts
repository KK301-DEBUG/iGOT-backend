import mongoose, { Schema, Document } from "mongoose";

export interface IMaterial extends Document {
  filename: string;
  extractedText: string;
  uploadedBy?: string;
  createdAt: Date;
}

const materialSchema = new Schema<IMaterial>({
  filename: { type: String, required: true },
  extractedText: { type: String, required: true },
  uploadedBy: { type: String },
  createdAt: { type: Date, default: Date.now },
});

export const Material = mongoose.model<IMaterial>("Material", materialSchema);
