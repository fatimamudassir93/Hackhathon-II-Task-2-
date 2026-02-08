import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { task } from "@/lib/schema";
import { eq, and, inArray } from "drizzle-orm";
import { headers } from "next/headers";

export async function PATCH(request: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { taskIds } = body;

  if (!Array.isArray(taskIds) || taskIds.length === 0) {
    return NextResponse.json({ error: "taskIds array required" }, { status: 400 });
  }

  await db
    .update(task)
    .set({ reminderSentAt: new Date() })
    .where(
      and(
        eq(task.userId, session.user.id),
        inArray(task.id, taskIds)
      )
    );

  return NextResponse.json({ acknowledged: taskIds.length });
}
