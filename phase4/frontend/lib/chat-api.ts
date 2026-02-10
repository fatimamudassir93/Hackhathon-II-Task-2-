export interface ToolCallInfo {
  tool: string;
  args: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatResponse {
  reply: string;
  tool_calls: ToolCallInfo[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  tool_calls: string | null;
  created_at: string;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
  total: number;
}

function extractErrorMessage(error: Record<string, unknown>, fallback: string): string {
  // Backend returns: { detail: "..." } or { error: { message: "...", type: "...", code: "..." } }
  if (typeof error?.detail === "string") return error.detail;
  if (typeof error?.error === "string") return error.error;
  if (error?.error && typeof (error.error as Record<string, unknown>)?.message === "string") {
    return (error.error as Record<string, string>).message;
  }
  return fallback;
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Chat request failed" }));
    throw new Error(extractErrorMessage(error, `Error ${res.status}`));
  }

  return res.json();
}

export async function getHistory(
  limit = 50,
  offset = 0
): Promise<ChatHistoryResponse> {
  const res = await fetch(`/api/chat/history?limit=${limit}&offset=${offset}`);

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Failed to load history" }));
    throw new Error(extractErrorMessage(error, `Error ${res.status}`));
  }

  return res.json();
}
