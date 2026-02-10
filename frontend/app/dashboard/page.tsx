"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import TaskList from "@/components/TaskList";

export default function DashboardPage() {
  const [userName, setUserName] = useState("User");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Try to get user info from localStorage or just use default
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser);
        setUserName(user.name || "User");
      } catch (e) {
        console.error("Failed to parse user data:", e);
      }
    }
  }, []);

  if (!mounted) {
    return (
      <div className="min-h-screen bg-mesh flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-2 border-purple-500/30 border-t-purple-500 animate-spin-slow mx-auto mb-4" />
          <p className="text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-mesh">
      <Navbar userName={userName} />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <TaskList />
      </main>
    </div>
  );
}
