"use client";

import { useState, useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import { sendMessage, getHistory, ToolCallInfo, ChatMessage as ChatMsg } from "@/lib/chat-api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCallInfo[];
  timestamp?: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load history on mount
  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getHistory();
        const loaded: Message[] = data.messages.map((m: ChatMsg) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          toolCalls: m.tool_calls ? JSON.parse(m.tool_calls) : undefined,
          timestamp: m.created_at,
        }));
        setMessages(loaded);
      } catch (error) {
        console.error("Failed to load chat history:", error);
        // Non-critical failure - continue with empty messages
        setMessages([]);
      }
    }
    loadHistory();
  }, []);

  // Auto-scroll on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const text = input.trim();
    if (!text || isLoading) return;

    setInput("");
    setError(null);

    // Optimistic user message
    const userMsg: Message = {
      id: `temp-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendMessage(text);
      const assistantMsg: Message = {
        id: `resp-${Date.now()}`,
        role: "assistant",
        content: typeof response.reply === "string" ? response.reply : JSON.stringify(response.reply),
        toolCalls: Array.isArray(response.tool_calls) ? response.tool_calls : [],
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-4xl mx-auto">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full text-center animate-fade-in-up">
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4 animate-float"
              style={{ background: "linear-gradient(135deg, #8b5cf6, #ec4899)" }}
            >
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold gradient-text mb-2">TaskFlow AI</h2>
            <p className="text-gray-400 text-sm max-w-md">
              I can help you manage your tasks. Try saying &quot;Add a task to buy groceries&quot;
              or &quot;Show my tasks&quot;.
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatMessage
            key={msg.id}
            role={msg.role}
            content={msg.content}
            toolCalls={msg.toolCalls}
            timestamp={msg.timestamp}
            index={i}
          />
        ))}

        {/* Typing indicator */}
        {isLoading && (
          <div className="flex justify-start animate-fade-in-up">
            <div className="flex items-start gap-3">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white animate-pulse-glow"
                style={{ background: "linear-gradient(135deg, #8b5cf6, #ec4899)" }}
              >
                AI
              </div>
              <div className="glass px-4 py-3 rounded-2xl rounded-tl-sm">
                <div className="flex gap-1.5">
                  <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0s" }} />
                  <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0.15s" }} />
                  <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0.3s" }} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="flex justify-center animate-fade-in-up">
            <div className="glass px-4 py-2 rounded-xl border border-red-500/30 text-red-400 text-sm flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              {error}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-white/10 px-4 py-4 glass-strong">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message... (e.g., 'Add a task to buy groceries')"
            className="input-field flex-1"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="btn-primary px-6 flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
