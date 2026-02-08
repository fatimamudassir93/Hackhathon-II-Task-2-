import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { sql } from "drizzle-orm";

export async function GET() {
  try {
    // Test 1: Check if we can connect
    const result = await db.execute(sql`SELECT current_database(), current_schema()`);

    // Test 2: List all tables
    const tables = await db.execute(sql`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);

    // Test 3: Check if session table exists
    const sessionCheck = await db.execute(sql`
      SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'session'
      )
    `);

    return NextResponse.json({
      success: true,
      connection: result.rows[0],
      tables: tables.rows,
      sessionExists: sessionCheck.rows[0]
    });
  } catch (error: any) {
    return NextResponse.json({
      success: false,
      error: error.message,
      code: error.code,
      detail: error.detail
    }, { status: 500 });
  }
}
