"use client";

import { useState } from "react";
import RecurrenceSelector from "./RecurrenceSelector";
import ReminderToggle from "./ReminderToggle";

interface Task {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: string;
  dueDate: string | null;
  createdAt: string;
  recurrencePattern: string | null;
  recurrenceEndDate: string | null;
  reminderEnabled: boolean;
  reminderOffsetMinutes: number | null;
}

interface TaskItemProps {
  task: Task;
  onUpdate: () => void;
}

const priorityConfig: Record<string, { class: string; icon: string }> = {
  high: { class: "priority-high", icon: "!!!" },
  medium: { class: "priority-medium", icon: "!!" },
  low: { class: "priority-low", icon: "!" },
};

function formatDueDate(dateStr: string): string {
  const d = new Date(dateStr);
  const hours = d.getHours();
  const minutes = d.getMinutes();
  const hasTime = hours !== 0 || minutes !== 0;

  if (hasTime) {
    return d.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  }
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

export default function TaskItem({ task, onUpdate }: TaskItemProps) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [priority, setPriority] = useState(task.priority);
  const [dueDate, setDueDate] = useState(() => {
    if (!task.dueDate) return "";
    const d = new Date(task.dueDate);
    // Format as datetime-local value: YYYY-MM-DDTHH:MM
    const pad = (n: number) => n.toString().padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  });
  const [recurrencePattern, setRecurrencePattern] = useState(task.recurrencePattern || "");
  const [recurrenceEndDate, setRecurrenceEndDate] = useState(
    task.recurrenceEndDate ? task.recurrenceEndDate.split("T")[0] : ""
  );
  const [reminderEnabled, setReminderEnabled] = useState(task.reminderEnabled || false);
  const [reminderOffsetMinutes, setReminderOffsetMinutes] = useState(task.reminderOffsetMinutes || 15);
  const [loading, setLoading] = useState(false);
  const [deleting, setDeleting] = useState(false);

  async function toggleComplete() {
    setLoading(true);
    await fetch(`/api/tasks/${task.id}/complete`, { method: "PATCH" });
    onUpdate();
    setLoading(false);
  }

  async function handleSave() {
    setLoading(true);
    await fetch(`/api/tasks/${task.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description: description || null,
        priority,
        dueDate: dueDate || null,
        recurrencePattern: recurrencePattern || null,
        recurrenceEndDate: recurrenceEndDate || null,
        reminderEnabled,
        reminderOffsetMinutes: reminderEnabled ? reminderOffsetMinutes : null,
      }),
    });
    setEditing(false);
    onUpdate();
    setLoading(false);
  }

  async function handleDelete() {
    setDeleting(true);
    await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
    onUpdate();
  }

  const pc = priorityConfig[task.priority] || priorityConfig.medium;

  // Edit mode
  if (editing) {
    return (
      <div className="card animate-scale-in space-y-3">
        <input
          type="text"
          className="input-field"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          autoFocus
        />
        <textarea
          className="input-field resize-none"
          rows={2}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description"
        />
        <div className="flex gap-2">
          {(["low", "medium", "high"] as const).map((p) => (
            <button
              key={p}
              type="button"
              onClick={() => setPriority(p)}
              className={`flex-1 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider
                transition-all duration-300 border
                ${priority === p
                  ? p === "high"
                    ? "priority-high border-rose-500/60"
                    : p === "medium"
                    ? "priority-medium border-amber-500/60"
                    : "priority-low border-emerald-500/60"
                  : "border-white/10 text-gray-500"
                }
              `}
              style={priority !== p ? { background: "rgba(255,255,255,0.03)" } : undefined}
            >
              {p}
            </button>
          ))}
        </div>
        <input
          type="datetime-local"
          className="input-field"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />
        {dueDate && (
          <>
            <RecurrenceSelector
              pattern={recurrencePattern}
              endDate={recurrenceEndDate}
              onPatternChange={setRecurrencePattern}
              onEndDateChange={setRecurrenceEndDate}
            />
            <ReminderToggle
              enabled={reminderEnabled}
              offsetMinutes={reminderOffsetMinutes}
              onEnabledChange={setReminderEnabled}
              onOffsetChange={setReminderOffsetMinutes}
            />
          </>
        )}
        <div className="flex gap-2 pt-1">
          <button onClick={handleSave} className="btn-primary text-sm flex-1" disabled={loading}>
            {loading ? "Saving..." : "Save Changes"}
          </button>
          <button
            onClick={() => {
              setEditing(false);
              setTitle(task.title);
              setDescription(task.description || "");
              setPriority(task.priority);
              const d = task.dueDate ? new Date(task.dueDate) : null;
              if (d) {
                const pad = (n: number) => n.toString().padStart(2, "0");
                setDueDate(`${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`);
              } else {
                setDueDate("");
              }
              setRecurrencePattern(task.recurrencePattern || "");
              setRecurrenceEndDate(task.recurrenceEndDate ? task.recurrenceEndDate.split("T")[0] : "");
              setReminderEnabled(task.reminderEnabled || false);
              setReminderOffsetMinutes(task.reminderOffsetMinutes || 15);
            }}
            className="btn-ghost"
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  // View mode
  return (
    <div
      className={`card group transition-all duration-500
        ${task.completed ? "opacity-50" : ""}
        ${deleting ? "scale-95 opacity-0" : ""}
      `}
    >
      {/* Priority strip at top */}
      <div className={`h-1 rounded-full -mt-2 mb-4 transition-all duration-300
        ${task.priority === "high" ? "bg-gradient-to-r from-rose-500 to-pink-500" :
          task.priority === "medium" ? "bg-gradient-to-r from-amber-500 to-orange-500" :
          "bg-gradient-to-r from-emerald-500 to-teal-500"}`}
      />

      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={toggleComplete}
          disabled={loading}
          className="checkbox-custom mt-0.5"
        />

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold text-[15px] transition-all duration-300 ${
              task.completed
                ? "line-through text-gray-500"
                : "text-white"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-400 mt-1.5 line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}

          {/* Meta row */}
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className={`text-[11px] px-2.5 py-1 rounded-full font-bold uppercase tracking-wider border ${pc.class}`}>
              {pc.icon} {task.priority}
            </span>
            {task.recurrencePattern && (
              <span className="badge-recurring">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {task.recurrencePattern}
              </span>
            )}
            {task.reminderEnabled && (
              <span className="text-[11px] px-2.5 py-1 rounded-full font-bold uppercase tracking-wider border border-purple-500/40 text-purple-300 inline-flex items-center gap-1"
                    style={{ background: "rgba(139, 92, 246, 0.15)" }}>
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                reminder
              </span>
            )}
            {task.dueDate && (
              <span className="text-xs text-gray-500 flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {formatDueDate(task.dueDate)}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Action buttons - appear on hover */}
      <div className="flex gap-2 mt-4 pt-3 border-t border-white/5
                      opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
        <button
          onClick={() => setEditing(true)}
          className="btn-ghost flex items-center gap-1.5 flex-1 justify-center"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="btn-danger flex items-center gap-1.5 flex-1 justify-center"
          disabled={deleting}
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete
        </button>
      </div>
    </div>
  );
}
