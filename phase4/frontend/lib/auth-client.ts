"use client";

import { createAuthClient } from "better-auth/react";

// Use production URL directly to avoid environment variable issues
const baseURL = typeof window !== "undefined"
  ? window.location.origin
  : process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000";

export const { signIn, signUp, signOut, useSession } = createAuthClient({
  baseURL,
});
