import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

// Mark as dynamic to ensure runtime environment variables are available
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const handlers = toNextJsHandler(auth);

export const POST = handlers.POST;
export const GET = handlers.GET;
