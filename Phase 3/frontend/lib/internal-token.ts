import jwt from "jsonwebtoken";

const SECRET = process.env.BETTER_AUTH_SECRET || "";

/**
 * Create a short-lived JWT for server-to-server calls to the FastAPI backend.
 * Uses the same BETTER_AUTH_SECRET that the backend verifies against.
 */
export function mintInternalToken(userId: string): string {
  return jwt.sign({ sub: userId }, SECRET, { expiresIn: "5m" });
}
