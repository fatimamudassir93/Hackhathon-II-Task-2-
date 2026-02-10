import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { task } from "@/lib/schema";
import { eq, and } from "drizzle-orm";
import { headers } from "next/headers";

export async function GET(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const result = await db
    .select()
    .from(task)
    .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)));

  if (result.length === 0) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  return NextResponse.json(result[0]);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { title, description, priority, dueDate, recurrencePattern, recurrenceEndDate, reminderEnabled, reminderOffsetMinutes } = body;

  if (title !== undefined && (typeof title !== "string" || title.trim().length === 0)) {
    return NextResponse.json({ error: "Title cannot be empty" }, { status: 400 });
  }

  // Check if dueDate is changing so we can re-arm the reminder
  let dueDateChanged = false;
  if (dueDate !== undefined) {
    const current = await db
      .select({ dueDate: task.dueDate })
      .from(task)
      .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)));
    if (current.length > 0) {
      const oldDue = current[0].dueDate?.toISOString() || null;
      const newDue = dueDate ? new Date(dueDate).toISOString() : null;
      dueDateChanged = oldDue !== newDue;
    }
  }

  const updated = await db
    .update(task)
    .set({
      ...(title !== undefined && { title: title.trim() }),
      ...(description !== undefined && { description: description?.trim() || null }),
      ...(priority !== undefined && { priority }),
      ...(dueDate !== undefined && { dueDate: dueDate ? new Date(dueDate) : null }),
      ...(recurrencePattern !== undefined && { recurrencePattern: recurrencePattern || null }),
      ...(recurrenceEndDate !== undefined && { recurrenceEndDate: recurrenceEndDate ? new Date(recurrenceEndDate) : null }),
      ...(reminderEnabled !== undefined && { reminderEnabled }),
      ...(reminderOffsetMinutes !== undefined && { reminderOffsetMinutes: reminderOffsetMinutes || null }),
      ...(dueDateChanged && { reminderSentAt: null }),
      updatedAt: new Date(),
    })
    .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)))
    .returning();

  if (updated.length === 0) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  return NextResponse.json(updated[0]);
}

export async function DELETE(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const deleted = await db
    .delete(task)
    .where(and(eq(task.id, params.id), eq(task.userId, session.user.id)))
    .returning();

  if (deleted.length === 0) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }

  return NextResponse.json({ message: "Task deleted" });
}
