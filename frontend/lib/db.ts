import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "./schema";

// Ensure DATABASE_URL_NEON is available
if (!process.env.DATABASE_URL_NEON) {
  throw new Error("DATABASE_URL_NEON environment variable is not set");
}

const sql = neon(process.env.DATABASE_URL_NEON);

export const db = drizzle(sql, { schema });
