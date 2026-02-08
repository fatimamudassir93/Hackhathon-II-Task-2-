import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { task } from "@/lib/schema";
import { eq, and } from "drizzle-orm";
import { headers } from "next/headers";
import crypto from "crypto";

function computeNextDueDate(current: Date, pattern: string): Date {
  const next = new Date(current);
  switch (pattern) {
    case "daily":
      next.setDate(next.getDate() + 1);
      break;
    case "weekly":
      next.setDate(next.getDate() + 7);
      break;
    case "monthly":
      next.setMonth(next.getMonth() + 1);
      break;
    case "yearly":
      next.setFullYear(next.getFullYear() + 1);
      break;
  }
  return next;
}

export async function PATCH(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Get the current task to toggle its completion status
  const current = await db
    .select()
    .from(task)
    .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)));

  if (current.length === 0) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  const updated = await db
    .update(task)
    .set({
      completed: !current[0].completed,
      updatedAt: new Date(),
    })
    .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)))
    .returning();

  const completedTask = updated[0];
  let nextTask = null;

  // If toggling to completed and task has recurrence, generate next occurrence
  if (
    !current[0].completed &&
    completedTask.completed &&
    completedTask.recurrencePattern &&
    completedTask.dueDate
  ) {
    const nextDueDate = computeNextDueDate(
      completedTask.dueDate,
      completedTask.recurrencePattern
    );

    // Skip if recurrence end date has passed
    const shouldCreate =
      !completedTask.recurrenceEndDate ||
      nextDueDate <= completedTask.recurrenceEndDate;

    if (shouldCreate) {
      const created = await db
        .insert(task)
        .values({
          id: crypto.randomUUID(),
          userId: session.user.id,
          title: completedTask.title,
          description: completedTask.description,
          priority: completedTask.priority,
          dueDate: nextDueDate,
          recurrencePattern: completedTask.recurrencePattern,
          recurrenceEndDate: completedTask.recurrenceEndDate,
          parentTaskId: completedTask.id,
          reminderEnabled: completedTask.reminderEnabled,
          reminderOffsetMinutes: completedTask.reminderOffsetMinutes,
          reminderSentAt: null,
          completed: false,
        })
        .returning();

      nextTask = created[0];
    }
  }

  return NextResponse.json({ completedTask, nextTask });
}
