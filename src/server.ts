import dotenv from "dotenv";
dotenv.config();

import { buildApp } from "./app";
import { connectDB } from "./config/db";

const start = async () => {
  await connectDB();
  const app = buildApp();

  try {
    const port = Number(process.env.PORT) || 5000;
    await app.listen({ port, host: "0.0.0.0" });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
