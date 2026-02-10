"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api-client";

interface TaskFormProps {
  onTaskCreated: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // Get user ID from localStorage
      const userStr = localStorage.getItem('user');
      if (!userStr) {
        setError("User not found. Please sign in again.");
        setLoading(false);
        return;
      }

      const user = JSON.parse(userStr);
      const result = await apiClient.createTask(user.id, {
        title,
        description: description || undefined,
        priority,
        dueDate: dueDate || undefined,
      });

      if (result.error) {
        setError(result.error);
        setLoading(false);
        return;
      }

      // Reset form
      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate("");
      setOpen(false);
      onTaskCreated();
    } catch {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="btn-primary flex items-center gap-2 group"
      >
        <span className="text-xl leading-none transition-transform duration-300 group-hover:rotate-90">+</span>
        Add New Task
      </button>
    );
  }

  return (
    <div className="card animate-scale-in w-full sm:w-auto sm:min-w-[380px]">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold gradient-text">New Task</h2>
        <button onClick={() => setOpen(false)} className="btn-ghost">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="animate-fade-in-up stagger-1">
          <input
            type="text"
            className="input-field"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div className="animate-fade-in-up stagger-2">
          <textarea
            className="input-field resize-none"
            placeholder="Add a description (optional)"
            rows={2}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="flex gap-3 animate-fade-in-up stagger-3">
          <div className="flex-1">
            <label className="block text-xs font-medium text-gray-400 mb-1.5 uppercase tracking-wider">
              Priority
            </label>
            <div className="flex gap-2">
              {(["low", "medium", "high"] as const).map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPriority(p)}
                  className={`flex-1 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider
                    transition-all duration-300 border
                    ${priority === p
                      ? p === "high"
                        ? "priority-high border-rose-500/60 shadow-lg shadow-rose-500/20"
                        : p === "medium"
                        ? "priority-medium border-amber-500/60 shadow-lg shadow-amber-500/20"
                        : "priority-low border-emerald-500/60 shadow-lg shadow-emerald-500/20"
                      : "border-white/10 text-gray-500 hover:border-white/20 hover:text-gray-300"
                    }
                  `}
                  style={priority !== p ? { background: "rgba(255,255,255,0.03)" } : undefined}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        </div>
        <div className="animate-fade-in-up stagger-4">
          <label className="block text-xs font-medium text-gray-400 mb-1.5 uppercase tracking-wider">
            Due Date & Time
          </label>
          <input
            type="datetime-local"
            className="input-field"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
          />
        </div>

        {error && (
          <div className="animate-fade-in-up flex items-center gap-2 text-rose-400 text-sm bg-rose-500/10 border border-rose-500/20 rounded-xl px-3 py-2">
            <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </div>
        )}

        <button type="submit" className="btn-primary w-full animate-fade-in-up stagger-5" disabled={loading}>
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="w-5 h-5 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Creating...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Create Task
            </span>
          )}
        </button>
      </form>
    </div>
  );
}
