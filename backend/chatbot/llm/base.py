from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass


@dataclass
class ToolDefinition:
    """Represents a tool that can be called by the LLM"""
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable


@dataclass
class Message:
    """Represents a chat message"""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class ChatResponse:
    """Response from LLM provider"""
    content: str
    tool_calls: List[Dict[str, Any]]
    finish_reason: str


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """
        Send a chat request to the LLM provider

        Args:
            messages: List of conversation messages
            tools: Optional list of tools the LLM can call
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Returns:
            ChatResponse with content and tool calls
        """
        pass

    @abstractmethod
    def format_tool_for_provider(self, tool: ToolDefinition) -> Dict[str, Any]:
        """Convert ToolDefinition to provider-specific format"""
        pass
