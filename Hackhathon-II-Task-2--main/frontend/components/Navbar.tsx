"use client";

import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

export default function Navbar({ userName }: { userName: string }) {
  const router = useRouter();

  async function handleSignOut() {
    // Clear token and user data
    apiClient.clearToken();
    router.push("/sign-in");
  }

  return (
    <nav className="glass-strong border-b border-white/10 sticky top-0 z-50 animate-fade-in-down"
         style={{ borderRadius: 0 }}>
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center"
               style={{ background: "linear-gradient(135deg, #8b5cf6, #ec4899)" }}>
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <h1 className="text-lg font-bold gradient-text">TaskFlow</h1>
        </div>

        {/* User area */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white"
                 style={{ background: "linear-gradient(135deg, #3b82f6, #8b5cf6)" }}>
              {userName.charAt(0).toUpperCase()}
            </div>
            <span className="text-sm text-gray-300 hidden sm:block font-medium">
              {userName}
            </span>
          </div>
          <button onClick={handleSignOut} className="btn-signout">
            <span className="flex items-center gap-1.5">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign Out
            </span>
          </button>
        </div>
      </div>
    </nav>
  );
}
