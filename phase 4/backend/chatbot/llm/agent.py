import json
from typing import List, Dict, Any, Optional
from .base import BaseLLMProvider, Message, ToolDefinition
from .tool_registry import ToolRegistry


class AgentContext:
    """Context passed to tool functions"""

    def __init__(self, db_session, user_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.db_session = db_session
        self.user_id = user_id
        self.metadata = metadata or {}


class Agent:
    """
    Agent that can use tools and handle conversations

    Replaces the OpenAI Agents SDK Agent class
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        tools: List[str],
        tool_registry: ToolRegistry
    ):
        """
        Initialize an agent

        Args:
            name: Agent name
            instructions: System instructions for the agent
            tools: List of tool names this agent can use
            tool_registry: Tool registry to look up tools
        """
        self.name = name
        self.instructions = instructions
        self.tool_names = tools
        self.tool_registry = tool_registry

    def get_tools(self) -> List[ToolDefinition]:
        """Get tool definitions for this agent"""
        return self.tool_registry.get_tools_by_names(self.tool_names)


class AgentRunner:
    """
    Orchestrates agent execution with tool calling

    Replaces the OpenAI Agents SDK Runner class
    """

    def __init__(self, provider: BaseLLMProvider, max_turns: int = 10):
        """
        Initialize the agent runner

        Args:
            provider: LLM provider to use
            max_turns: Maximum number of conversation turns
        """
        self.provider = provider
        self.max_turns = max_turns

    async def run(
        self,
        agent: Agent,
        messages: List[Message],
        context: AgentContext
    ) -> Dict[str, Any]:
        """
        Run the agent with the given messages and context

        Args:
            agent: Agent to run
            messages: Conversation history
            context: Context with db_session, user_id, etc.

        Returns:
            Dict with 'reply' (str) and 'tool_calls' (list)
        """
        # Prepend system instructions
        full_messages = [
            Message(role="system", content=agent.instructions)
        ] + messages

        tools = agent.get_tools()
        conversation_history = full_messages.copy()
        tool_call_history = []

        for turn in range(self.max_turns):
            # Call LLM
            response = await self.provider.chat(
                messages=conversation_history,
                tools=tools if tools else None,
                temperature=0.7,
                max_tokens=1500
            )

            # If no tool calls, we're done
            if not response.tool_calls:
                return {
                    "reply": response.content,
                    "tool_calls": tool_call_history
                }

            # Add assistant message with tool calls to history
            conversation_history.append(Message(
                role="assistant",
                content=response.content or "",
                tool_calls=response.tool_calls
            ))

            # Execute tool calls
            for tool_call in response.tool_calls:
                function_name = tool_call["function"]["name"]
                function_args_str = tool_call["function"]["arguments"]

                # Parse arguments
                try:
                    function_args = json.loads(function_args_str)
                except json.JSONDecodeError:
                    function_args = {}

                # Get tool definition
                tool_def = agent.tool_registry.get_tool(function_name)
                if not tool_def:
                    result = {"error": f"Tool {function_name} not found"}
                else:
                    # Execute tool
                    try:
                        result = await tool_def.function(context, **function_args)
                    except Exception as e:
                        result = {"error": str(e)}

                # Record tool call for response
                tool_call_history.append({
                    "tool": function_name,
                    "args": function_args,
                    "result": result
                })

                # Add tool result to conversation
                conversation_history.append(Message(
                    role="tool",
                    content=json.dumps(result),
                    tool_call_id=tool_call.get("id"),
                    name=function_name
                ))

        # Max turns reached, return last response
        return {
            "reply": "I've completed the requested actions.",
            "tool_calls": tool_call_history
        }
