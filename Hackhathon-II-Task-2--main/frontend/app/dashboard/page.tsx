"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import TaskList from "@/components/TaskList";
import type { User } from "@/lib/api-client";

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const userStr = localStorage.getItem('user');
    const token = localStorage.getItem('auth_token');

    if (!userStr || !token) {
      router.push('/sign-in');
      return;
    }

    try {
      const userData = JSON.parse(userStr);
      setUser(userData);
    } catch (error) {
      console.error('Failed to parse user data:', error);
      router.push('/sign-in');
    } finally {
      setLoading(false);
    }
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-mesh flex items-center justify-center">
        <div className="text-white text-lg">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-mesh">
      <Navbar userName={user.name} />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <TaskList userId={user.id} />
      </main>
    </div>
  );
}
