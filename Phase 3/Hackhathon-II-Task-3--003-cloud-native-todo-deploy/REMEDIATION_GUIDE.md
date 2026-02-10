# Critical Issue Remediation Guide

## Status: Phase 1 Complete ✅

### Completed Fixes:
- ✅ **C3: Test-First Compliance** - Created test files:
  - `backend/tests/test_tools/test_task_tools.py` (17 tests)
  - `backend/tests/test_agents/test_triage.py` (19 tests)
  - `backend/tests/test_routes/test_chat.py` (10 tests)
- ✅ **C5: Missing Analytics Service** - Created `backend/src/services/analytics_service.py`
- ✅ **C4: Branch Mismatch** - Confirmed focus on 002-todo-ai-chatbot

---

## Phase 2: Architecture Fixes (CRITICAL)

### C1: OpenAI Agents SDK Violation

**Constitution Requirement:**
> "Backend: Python FastAPI with OpenAI Agents SDK for agent orchestration and MCP tool execution"

**Current State:**
- Custom `Agent` and `AgentRunner` classes in `backend/chatbot/llm/agent.py`
- Multi-provider system (OpenAI, Groq, Gemini) not mentioned in constitution
- Comment says "Replaces the OpenAI Agents SDK"

**Why This Violates Constitution:**
The constitution explicitly mandates OpenAI Agents SDK. The custom implementation, while functional, violates Principle I (Technology Binding Adherence) which states: "Responsibilities MUST NOT cross layers — each technology has fixed responsibilities that MUST NOT be mixed."

**Remediation Options:**

#### Option A: Use OpenAI Agents SDK (Recommended - Constitution Compliant)

**Installation:**
```bash
pip install openai-agents-sdk
```

**Replace `backend/chatbot/llm/agent.py` with:**
```python
from openai_agents import Agent, Runner, function_tool
from typing import List, Dict, Any

# Agent definition example
task_agent = Agent(
    name="Task Agent",
    instructions="""You are a task management specialist.
    Help users create, update, complete, and delete tasks.
    Always confirm actions with clear messages.""",
    tools=["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
)

# Runner for execution
async def run_agent(agent: Agent, messages: List[Dict], context: Dict) -> Dict:
    runner = Runner(agent=agent)
    result = await runner.run(messages=messages, context=context)
    return {
        "reply": result.final_message,
        "tool_calls": result.tool_calls
    }
```

**Update tool definitions to use `@function_tool`:**
```python
from openai_agents import function_tool

@function_tool
async def add_task(title: str, description: str = None) -> dict:
    """Add a new task for the user"""
    # Implementation stays the same
    pass
```

**Migration Steps:**
1. Install `openai-agents-sdk`
2. Replace custom Agent/AgentRunner with SDK classes
3. Update tool decorators from `@tool_registry.register` to `@function_tool`
4. Update ChatService to use SDK Runner
5. Test all agent routing and tool execution

**Estimated Effort:** 8-12 hours

---

#### Option B: Update Constitution (Not Recommended)

If the multi-provider approach is genuinely required, update the constitution to reflect this:

**Change in `.specify/memory/constitution.md`:**
```markdown
### I. Technology Binding Adherence

Backend: Python FastAPI with **custom multi-provider LLM system**
(OpenAI, Groq, Gemini) for agent orchestration and MCP tool execution.
```

**However:** This requires explicit user approval and constitution version bump to 4.0.0, as it's a MAJOR change to core principles.

---

### C2: ChatKit UI Violation

**Constitution Requirement:**
> "Frontend: ChatKit UI for conversational interface"
> "Use ChatKit UI components for the conversational interface"

**Current State:**
- Custom React components in `frontend/components/ChatInterface.tsx`
- ChatKit library installed but NOT used
- Custom glassmorphism UI with manual message rendering

**Why This Violates Constitution:**
Principle I explicitly mandates ChatKit UI. The custom implementation, while visually appealing, violates the technology binding.

**Remediation:**

**Replace `frontend/components/ChatInterface.tsx` with ChatKit components:**

```typescript
"use client";

import { useState, useEffect } from "react";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
  Avatar,
} from "@chatscope/chat-ui-kit-react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { sendMessage, getHistory, ChatMessage as ChatMsg } from "@/lib/chat-api";

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getHistory();
        setMessages(data.messages);
      } catch (err) {
        console.error("Failed to load history:", err);
      }
    }
    loadHistory();
  }, []);

  async function handleSend(text: string) {
    if (!text.trim()) return;

    // Add user message
    const userMsg: ChatMsg = {
      id: `temp-${Date.now()}`,
      role: "user",
      content: text,
      tool_calls: null,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const response = await sendMessage(text);
      const assistantMsg: ChatMsg = {
        id: `resp-${Date.now()}`,
        role: "assistant",
        content: response.reply,
        tool_calls: JSON.stringify(response.tool_calls),
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Send failed:", err);
    } finally {
      setIsTyping(false);
    }
  }

  return (
    <div style={{ position: "relative", height: "calc(100vh - 4rem)" }}>
      <MainContainer>
        <ChatContainer>
          <MessageList
            typingIndicator={isTyping ? <TypingIndicator content="AI is thinking" /> : null}
          >
            {messages.map((msg) => (
              <Message
                key={msg.id}
                model={{
                  message: msg.content,
                  sentTime: msg.created_at,
                  sender: msg.role === "user" ? "You" : "TaskFlow AI",
                  direction: msg.role === "user" ? "outgoing" : "incoming",
                  position: "single",
                }}
              >
                <Avatar
                  src={msg.role === "user" ? "/user-avatar.png" : "/ai-avatar.png"}
                  name={msg.role === "user" ? "You" : "AI"}
                />
              </Message>
            ))}
          </MessageList>
          <MessageInput
            placeholder="Type a message..."
            onSend={handleSend}
            attachButton={false}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
}
```

**Add ChatKit styles to `frontend/app/layout.tsx`:**
```typescript
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
```

**Migration Steps:**
1. Import ChatKit components
2. Replace custom message rendering with `<Message>` components
3. Replace custom input with `<MessageInput>`
4. Replace custom typing indicator with `<TypingIndicator>`
5. Apply custom theme via ChatKit's theming system (if needed)
6. Remove custom ChatMessage and ToolCallDisplay components

**Estimated Effort:** 4-6 hours

---

### C6: Agent Architecture - Keyword Routing

**Constitution Requirement:**
> "The OpenAI Agents SDK MUST be used for agent orchestration, routing, and handoffs"

**Current State:**
- Simple keyword matching in `backend/chatbot/agents/triage.py`
- No AI-powered intent classification
- No handoff mechanism

**Remediation with OpenAI Agents SDK:**

```python
from openai_agents import Agent

# Triage agent with handoff capabilities
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a routing specialist. Analyze user messages and hand off to:
    - Task Agent: for creating, updating, completing, deleting tasks
    - Tag Agent: for adding, removing, listing tags
    - Reminder Agent: for scheduling, canceling reminders
    - Analytics Agent: for task counts and statistics

    Use handoffs to route to the appropriate specialist.""",
    tools=[],  # No tools, only handoffs
    handoffs=[task_agent, tag_agent, reminder_agent, analytics_agent]
)
```

**Update ChatService:**
```python
async def process_message(user_id: str, message: str, db_session: AsyncSession) -> dict:
    # Start with triage agent
    runner = Runner(agent=triage_agent)
    result = await runner.run(
        messages=[{"role": "user", "content": message}],
        context={"db_session": db_session, "user_id": user_id}
    )
    return {"reply": result.final_message, "tool_calls": result.tool_calls}
```

**Estimated Effort:** 6-8 hours (depends on SDK handoff API)

---

### C7: Stateless Violation

**Issue:** `conversation_history` stored in memory during agent execution

**Fix:** Ensure all state is immediately persisted to database

**Update `backend/chatbot/services/chat_service.py`:**

```python
async def process_message(user_id: str, message: str, db_session: AsyncSession) -> dict:
    # Save user message IMMEDIATELY
    await ConversationService.save_message(
        user_id=user_id,
        role="user",
        content=message,
        tool_calls=None,
        db_session=db_session,
    )
    await db_session.commit()  # ← ADD THIS: Commit immediately

    # Load history from DB (not memory)
    recent_messages = await ConversationService.get_recent_messages(
        user_id=user_id,
        db_session=db_session,
        limit=20,
    )

    # Process with agent (stateless - no in-memory state)
    result = await runner.run(agent=agent, messages=conversation_history, context=context)

    # Save assistant response IMMEDIATELY
    await ConversationService.save_message(
        user_id=user_id,
        role="assistant",
        content=reply,
        tool_calls=tool_calls_json,
        db_session=db_session,
    )
    await db_session.commit()  # ← ADD THIS: Commit immediately

    return {"reply": reply, "tool_calls": tool_calls_info}
```

**Verification Test:**
```python
# Test stateless behavior
async def test_server_restart_preserves_state():
    # Send message
    await send_message("Add task 1")

    # Simulate server restart (clear all in-memory state)
    restart_server()

    # Verify conversation history is intact
    history = await get_history()
    assert len(history.messages) > 0
```

**Estimated Effort:** 2 hours

---

## Summary of Remaining Work

| Issue | Effort | Priority | Blocking? |
|-------|--------|----------|-----------|
| C1: OpenAI Agents SDK | 8-12h | CRITICAL | Yes |
| C2: ChatKit UI | 4-6h | CRITICAL | Yes |
| C6: AI-powered routing | 6-8h | CRITICAL | Yes |
| C7: Stateless fixes | 2h | HIGH | No |

**Total Estimated Effort:** 20-28 hours

**Recommended Sequence:**
1. Fix C7 (stateless) - Quick win, 2 hours
2. Fix C1 (OpenAI SDK) - Unblocks C6, 8-12 hours
3. Fix C6 (AI routing) - Depends on C1, 6-8 hours
4. Fix C2 (ChatKit UI) - Can be done in parallel, 4-6 hours

---

## Decision Required

**Question for User:** The constitution mandates OpenAI Agents SDK and ChatKit UI, but the current implementation uses custom alternatives. Do you want to:

A. **Refactor to comply with constitution** (20-28 hours of work)
B. **Update constitution to reflect current architecture** (requires approval + version bump)
C. **Defer architectural fixes and focus on functionality** (accept constitution violations)

Please advise on preferred approach.
