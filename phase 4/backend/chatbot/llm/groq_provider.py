import json
from typing import List, Dict, Any, Optional
from groq import AsyncGroq
from .base import BaseLLMProvider, ToolDefinition, Message, ChatResponse


class GroqProvider(BaseLLMProvider):
    """Groq API provider (OpenAI-compatible)"""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = AsyncGroq(api_key=api_key)

    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """Send chat request to Groq"""

        # Convert messages to Groq format (OpenAI-compatible)
        groq_messages = []
        for msg in messages:
            message_dict = {"role": msg.role, "content": msg.content}
            if msg.tool_calls:
                message_dict["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                message_dict["tool_call_id"] = msg.tool_call_id
            if msg.name:
                message_dict["name"] = msg.name
            groq_messages.append(message_dict)

        # Prepare request
        request_params = {
            "model": self.model,
            "messages": groq_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Add tools if provided
        if tools:
            request_params["tools"] = [self.format_tool_for_provider(t) for t in tools]
            request_params["tool_choice"] = "auto"

        # Make API call
        response = await self.client.chat.completions.create(**request_params)

        # Extract response
        choice = response.choices[0]
        content = choice.message.content or ""
        tool_calls = []

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                tool_calls.append({
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                })

        return ChatResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason
        )

    def format_tool_for_provider(self, tool: ToolDefinition) -> Dict[str, Any]:
        """Convert ToolDefinition to Groq function calling format (OpenAI-compatible)"""
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        }
