import { neon } from "@neondatabase/serverless";
import { config } from "dotenv";

config();

const sql = neon(process.env.DATABASE_URL_NEON);

async function createTables() {
  console.log("Creating Better Auth tables...");

  // Create "user" table (Better Auth)
  await sql`
    CREATE TABLE IF NOT EXISTS "user" (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      email_verified BOOLEAN NOT NULL DEFAULT false,
      image TEXT,
      created_at TIMESTAMP NOT NULL DEFAULT now(),
      updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
  `;
  console.log("  [ok] user");

  // Create "session" table (Better Auth)
  await sql`
    CREATE TABLE IF NOT EXISTS "session" (
      id TEXT PRIMARY KEY,
      expires_at TIMESTAMP NOT NULL,
      token TEXT NOT NULL UNIQUE,
      created_at TIMESTAMP NOT NULL DEFAULT now(),
      updated_at TIMESTAMP NOT NULL DEFAULT now(),
      ip_address TEXT,
      user_agent TEXT,
      user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
    )
  `;
  console.log("  [ok] session");

  // Create "account" table (Better Auth)
  await sql`
    CREATE TABLE IF NOT EXISTS "account" (
      id TEXT PRIMARY KEY,
      account_id TEXT NOT NULL,
      provider_id TEXT NOT NULL,
      user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
      access_token TEXT,
      refresh_token TEXT,
      id_token TEXT,
      access_token_expires_at TIMESTAMP,
      refresh_token_expires_at TIMESTAMP,
      scope TEXT,
      password TEXT,
      created_at TIMESTAMP NOT NULL DEFAULT now(),
      updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
  `;
  console.log("  [ok] account");

  // Create "verification" table (Better Auth)
  await sql`
    CREATE TABLE IF NOT EXISTS "verification" (
      id TEXT PRIMARY KEY,
      identifier TEXT NOT NULL,
      value TEXT NOT NULL,
      expires_at TIMESTAMP NOT NULL,
      created_at TIMESTAMP DEFAULT now(),
      updated_at TIMESTAMP DEFAULT now()
    )
  `;
  console.log("  [ok] verification");

  // Create "task" table (app)
  await sql`
    CREATE TABLE IF NOT EXISTS "task" (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
      title VARCHAR(255) NOT NULL,
      description TEXT,
      completed BOOLEAN NOT NULL DEFAULT false,
      priority VARCHAR(20) NOT NULL DEFAULT 'medium',
      due_date TIMESTAMP,
      created_at TIMESTAMP NOT NULL DEFAULT now(),
      updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
  `;
  console.log("  [ok] task");

  // Add recurring task + reminder columns (safe to re-run)
  console.log("\nAdding recurring task & reminder columns...");

  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20)`;
  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS recurrence_end_date TIMESTAMP`;
  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS parent_task_id TEXT`;
  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS reminder_enabled BOOLEAN NOT NULL DEFAULT false`;
  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS reminder_offset_minutes INTEGER`;
  await sql`ALTER TABLE "task" ADD COLUMN IF NOT EXISTS reminder_sent_at TIMESTAMP`;

  console.log("  [ok] recurring + reminder columns");

  console.log("\nAll tables created successfully!");
}

createTables().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
