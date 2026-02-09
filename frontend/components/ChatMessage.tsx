"use client";

import { ToolCallInfo } from "@/lib/chat-api";
import ToolCallDisplay from "./ToolCallDisplay";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCallInfo[];
  timestamp?: string;
  index: number;
}

export default function ChatMessage({ role, content, toolCalls, timestamp, index }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} animate-fade-in-up`}
      style={{ animationDelay: `${index * 0.03}s` }}
    >
      <div className={`max-w-[80%] ${isUser ? "order-2" : "order-1"}`}>
        {/* Avatar */}
        <div className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
          <div
            className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0 ${
              isUser ? "" : "animate-pulse-glow"
            }`}
            style={{
              background: isUser
                ? "linear-gradient(135deg, #3b82f6, #8b5cf6)"
                : "linear-gradient(135deg, #8b5cf6, #ec4899)",
            }}
          >
            {isUser ? "U" : "AI"}
          </div>

          {/* Message bubble */}
          <div
            className={`glass px-4 py-3 rounded-2xl ${
              isUser
                ? "rounded-tr-sm border-blue-500/20"
                : "rounded-tl-sm border-purple-500/20"
            }`}
          >
            <p className="text-sm text-gray-200 whitespace-pre-wrap leading-relaxed">
              {content}
            </p>

            {/* Tool calls */}
            {toolCalls && toolCalls.length > 0 && (
              <ToolCallDisplay toolCalls={toolCalls} />
            )}

            {/* Timestamp */}
            {timestamp && (
              <p className="text-[10px] text-gray-500 mt-2">
                {new Date(timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
