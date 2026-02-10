import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from .base import BaseLLMProvider, ToolDefinition, Message, ChatResponse


class GeminiProvider(BaseLLMProvider):
    """Google Gemini API provider"""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)

    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """Send chat request to Gemini"""

        # Convert messages to Gemini format
        gemini_messages = []
        system_instruction = None

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            elif msg.role == "user":
                gemini_messages.append({
                    "role": "user",
                    "parts": [msg.content]
                })
            elif msg.role == "assistant":
                gemini_messages.append({
                    "role": "model",
                    "parts": [msg.content]
                })
            elif msg.role == "tool":
                # Gemini handles tool responses differently
                gemini_messages.append({
                    "role": "function",
                    "parts": [{
                        "function_response": {
                            "name": msg.name,
                            "response": {"result": msg.content}
                        }
                    }]
                })

        # Configure generation
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        # Prepare tools if provided
        gemini_tools = None
        if tools:
            gemini_tools = [self.format_tool_for_provider(t) for t in tools]

        # Create model with system instruction if provided
        if system_instruction:
            model = genai.GenerativeModel(
                self.model,
                system_instruction=system_instruction
            )
        else:
            model = self.model_instance

        # Make API call
        if gemini_tools:
            response = await model.generate_content_async(
                gemini_messages,
                generation_config=generation_config,
                tools=gemini_tools
            )
        else:
            response = await model.generate_content_async(
                gemini_messages,
                generation_config=generation_config
            )

        # Extract response
        content = ""
        tool_calls = []

        if response.candidates:
            candidate = response.candidates[0]

            # Extract text content
            if candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        content += part.text
                    elif hasattr(part, 'function_call'):
                        # Extract function call
                        fc = part.function_call
                        tool_calls.append({
                            "id": f"call_{len(tool_calls)}",
                            "type": "function",
                            "function": {
                                "name": fc.name,
                                "arguments": json.dumps(dict(fc.args))
                            }
                        })

            finish_reason = candidate.finish_reason.name if candidate.finish_reason else "stop"
        else:
            finish_reason = "error"

        return ChatResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=finish_reason
        )

    def format_tool_for_provider(self, tool: ToolDefinition) -> Dict[str, Any]:
        """Convert ToolDefinition to Gemini function declaration format"""
        return {
            "function_declarations": [{
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }]
        }
