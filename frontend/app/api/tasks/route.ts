import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import { task } from "@/lib/schema";
import { eq, desc } from "drizzle-orm";
import { headers } from "next/headers";
import crypto from "crypto";

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const tasks = await db
    .select()
    .from(task)
    .where(eq(task.userId, session.user.id))
    .orderBy(desc(task.createdAt));

  return NextResponse.json(tasks);
}

export async function POST(request: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { title, description, priority, dueDate, recurrencePattern, recurrenceEndDate, reminderEnabled, reminderOffsetMinutes } = body;

  if (!title || typeof title !== "string" || title.trim().length === 0) {
    return NextResponse.json({ error: "Title is required" }, { status: 400 });
  }

  if (recurrencePattern && !dueDate) {
    return NextResponse.json({ error: "Recurrence requires a due date" }, { status: 400 });
  }

  if (reminderEnabled && !dueDate) {
    return NextResponse.json({ error: "Reminder requires a due date" }, { status: 400 });
  }

  const newTask = await db
    .insert(task)
    .values({
      id: crypto.randomUUID(),
      userId: session.user.id,
      title: title.trim(),
      description: description?.trim() || null,
      priority: priority || "medium",
      dueDate: dueDate ? new Date(dueDate) : null,
      recurrencePattern: recurrencePattern || null,
      recurrenceEndDate: recurrenceEndDate ? new Date(recurrenceEndDate) : null,
      reminderEnabled: reminderEnabled || false,
      reminderOffsetMinutes: reminderOffsetMinutes || null,
      completed: false,
    })
    .returning();

  return NextResponse.json(newTask[0], { status: 201 });
}
