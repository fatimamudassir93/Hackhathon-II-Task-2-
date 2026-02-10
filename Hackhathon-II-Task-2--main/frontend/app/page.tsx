"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('user');

    if (token && user) {
      // User is logged in, redirect to dashboard
      router.push('/dashboard');
    } else {
      // User is not logged in, redirect to sign-in
      router.push('/sign-in');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-mesh flex items-center justify-center">
      <div className="text-white text-lg">Loading...</div>
    </div>
  );
}
