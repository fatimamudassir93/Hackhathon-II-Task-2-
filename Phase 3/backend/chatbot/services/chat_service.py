import json
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from chatbot.llm.provider_factory import get_default_provider
from chatbot.llm.agent import AgentRunner, AgentContext
from chatbot.llm.base import Message
from chatbot.agents.triage import get_agent_for_message
from chatbot.services.conversation_service import ConversationService


class ChatService:

    @staticmethod
    async def process_message(
        user_id: str,
        message: str,
        db_session: AsyncSession,
    ) -> dict:
        """
        Process a chat message from the user.

        Args:
            user_id: User ID
            message: User's message text
            db_session: Database session

        Returns:
            Dict with 'reply' (str) and 'tool_calls' (list)
        """
        # Save the user message
        await ConversationService.save_message(
            user_id=user_id,
            role="user",
            content=message,
            tool_calls=None,
            db_session=db_session,
        )

        # Load recent conversation history for context
        recent_messages = await ConversationService.get_recent_messages(
            user_id=user_id,
            db_session=db_session,
            limit=20,
        )

        # Convert to Message objects
        # Skip assistant messages with tool calls to avoid format mismatch
        conversation_history = []
        for msg in recent_messages:
            # Skip assistant messages that have tool calls (they're reconstructed by the agent)
            if msg.role == "assistant" and msg.tool_calls:
                continue
            conversation_history.append(Message(
                role=msg.role,
                content=msg.content,
                tool_calls=None  # Don't include tool_calls from DB
            ))

        # Route to appropriate agent
        agent = get_agent_for_message(message)

        # Create context
        context = AgentContext(
            db_session=db_session,
            user_id=user_id
        )

        # Get LLM provider
        provider = get_default_provider()

        # Run agent
        runner = AgentRunner(provider=provider, max_turns=10)
        result = await runner.run(
            agent=agent,
            messages=conversation_history,
            context=context
        )

        # Extract reply and tool calls
        reply = result.get("reply", "I'm sorry, I couldn't process your request.")
        tool_calls_info = result.get("tool_calls", [])

        # Save the assistant response
        tool_calls_json = json.dumps(tool_calls_info) if tool_calls_info else None
        await ConversationService.save_message(
            user_id=user_id,
            role="assistant",
            content=reply,
            tool_calls=tool_calls_json,
            db_session=db_session,
        )

        return {
            "reply": reply,
            "tool_calls": tool_calls_info,
        }
