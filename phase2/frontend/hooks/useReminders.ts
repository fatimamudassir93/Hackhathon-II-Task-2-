"use client";

import { useEffect, useRef } from "react";

export function useReminders() {
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    // Request notification permission on mount
    if (typeof window !== "undefined" && "Notification" in window) {
      if (Notification.permission === "default") {
        Notification.requestPermission();
      }
    }

    async function checkReminders() {
      try {
        const res = await fetch("/api/tasks/reminders");
        if (!res.ok) return;

        const dueTasks = await res.json();
        if (!Array.isArray(dueTasks) || dueTasks.length === 0) return;

        // Fire notifications
        if ("Notification" in window && Notification.permission === "granted") {
          for (const t of dueTasks) {
            const dueTime = t.dueDate
              ? new Date(t.dueDate).toLocaleTimeString("en-US", {
                  hour: "numeric",
                  minute: "2-digit",
                })
              : "";
            new Notification(`Task Reminder: ${t.title}`, {
              body: dueTime ? `Due at ${dueTime}` : "Task is due soon!",
              icon: "/favicon.ico",
            });
          }
        }

        // Acknowledge so they don't re-fire
        const taskIds = dueTasks.map((t: { id: string }) => t.id);
        await fetch("/api/tasks/reminders/ack", {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ taskIds }),
        });
      } catch {
        // Silently fail - polling will retry
      }
    }

    // Initial check
    checkReminders();

    // Poll every 60 seconds
    intervalRef.current = setInterval(checkReminders, 60_000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);
}
