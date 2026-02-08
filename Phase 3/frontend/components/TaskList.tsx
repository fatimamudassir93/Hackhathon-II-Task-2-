"use client";

import { useState, useEffect, useCallback } from "react";
import TaskForm from "./TaskForm";
import TaskItem from "./TaskItem";
import { useReminders } from "@/hooks/useReminders";

type Filter = "all" | "active" | "completed";

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

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<Filter>("all");
  const [loading, setLoading] = useState(true);

  // Start reminder polling
  useReminders();

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/tasks");
    if (res.ok) {
      const data = await res.json();
      setTasks(data);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const filtered = tasks.filter((t) => {
    if (filter === "active") return !t.completed;
    if (filter === "completed") return t.completed;
    return true;
  });

  const completedCount = tasks.filter((t) => t.completed).length;
  const activeCount = tasks.length - completedCount;

  const tabs: { label: string; value: Filter; count: number }[] = [
    { label: "All", value: "all", count: tasks.length },
    { label: "Active", value: "active", count: activeCount },
    { label: "Completed", value: "completed", count: completedCount },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 animate-fade-in-down">
        <div>
          <h2 className="text-3xl font-bold gradient-text">My Tasks</h2>
          {tasks.length > 0 && (
            <p className="text-gray-400 text-sm mt-1">
              {completedCount} of {tasks.length} completed
            </p>
          )}
        </div>
        <TaskForm onTaskCreated={fetchTasks} />
      </div>

      {/* Progress bar */}
      {tasks.length > 0 && (
        <div className="animate-fade-in-up stagger-1">
          <div className="h-2 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.05)" }}>
            <div
              className="h-full rounded-full transition-all duration-700 ease-out"
              style={{
                width: `${(completedCount / tasks.length) * 100}%`,
                background: "linear-gradient(90deg, #8b5cf6, #ec4899, #f97316)",
              }}
            />
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-1 p-1 rounded-xl w-fit animate-fade-in-up stagger-2" style={{ background: "rgba(255,255,255,0.05)" }}>
        {tabs.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setFilter(tab.value)}
            className={`px-5 py-2 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 ${
              filter === tab.value
                ? "text-white shadow-lg"
                : "text-gray-400 hover:text-gray-200"
            }`}
            style={
              filter === tab.value
                ? { background: "linear-gradient(135deg, rgba(139,92,246,0.4), rgba(236,72,153,0.4))" }
                : undefined
            }
          >
            {tab.label}
            <span
              className={`text-xs px-1.5 py-0.5 rounded-full font-bold transition-all duration-300 ${
                filter === tab.value
                  ? "bg-white/20 text-white"
                  : "bg-white/5 text-gray-500"
              }`}
            >
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Task grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 animate-fade-in-up">
          <div className="w-12 h-12 rounded-full border-2 border-purple-500/30 border-t-purple-500 animate-spin-slow mb-4" />
          <p className="text-gray-400">Loading your tasks...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 animate-fade-in-up">
          <div className="w-20 h-20 rounded-2xl flex items-center justify-center mb-4 animate-float"
               style={{ background: "linear-gradient(135deg, rgba(139,92,246,0.2), rgba(236,72,153,0.2))" }}>
            {filter === "completed" ? (
              <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : (
              <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            )}
          </div>
          <p className="text-gray-300 font-medium text-lg">
            {filter === "all"
              ? "No tasks yet"
              : filter === "active"
              ? "All caught up!"
              : "No completed tasks"}
          </p>
          <p className="text-gray-500 text-sm mt-1">
            {filter === "all"
              ? "Create your first task to get started"
              : filter === "active"
              ? "You've completed everything. Great job!"
              : "Complete a task and it will show up here"}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((task, i) => (
            <div
              key={task.id}
              className="animate-fade-in-up"
              style={{ animationDelay: `${i * 0.06}s` }}
            >
              <TaskItem task={task} onUpdate={fetchTasks} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
