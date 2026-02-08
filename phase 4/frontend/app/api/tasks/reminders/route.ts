import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { task } from "@/lib/schema";
import { eq, and, isNull, lte } from "drizzle-orm";
import { headers } from "next/headers";
import { sql } from "drizzle-orm";

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Find tasks where:
  // - reminder is enabled
  // - task is not completed
  // - reminder hasn't been sent yet
  // - dueDate minus offset is <= now
  const dueTasks = await db
    .select()
    .from(task)
    .where(
      and(
        eq(task.userId, session.user.id),
        eq(task.reminderEnabled, true),
        eq(task.completed, false),
        isNull(task.reminderSentAt),
        lte(
          sql`${task.dueDate} - COALESCE(${task.reminderOffsetMinutes}, 0) * interval '1 minute'`,
          sql`now()`
        )
      )
    );

  return NextResponse.json(dueTasks);
}
