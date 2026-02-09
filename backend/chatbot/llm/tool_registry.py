from typing import Dict, Any, Callable, List, Optional
from inspect import signature, Parameter
from .base import ToolDefinition


class ToolRegistry:
    """Registry for managing tools that can be called by LLMs"""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Decorator to register a function as a tool

        Usage:
            @tool_registry.register(
                name="add_task",
                description="Add a new task",
                parameters={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title"}
                    },
                    "required": ["title"]
                }
            )
            async def add_task(ctx, title: str):
                ...
        """
        def decorator(func: Callable):
            # Auto-generate parameters schema if not provided
            if parameters is None:
                params = self._generate_parameters_schema(func)
            else:
                params = parameters

            tool_def = ToolDefinition(
                name=name,
                description=description,
                parameters=params,
                function=func
            )
            self._tools[name] = tool_def
            return func

        return decorator

    def _generate_parameters_schema(self, func: Callable) -> Dict[str, Any]:
        """Auto-generate JSON schema from function signature"""
        sig = signature(func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Skip 'ctx' parameter
            if param_name == "ctx":
                continue

            # Basic type mapping
            param_type = "string"
            if param.annotation != Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"

            properties[param_name] = {"type": param_type}

            # Mark as required if no default value
            if param.default == Parameter.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name"""
        return self._tools.get(name)

    def get_all_tools(self) -> List[ToolDefinition]:
        """Get all registered tools"""
        return list(self._tools.values())

    def get_tools_by_names(self, names: List[str]) -> List[ToolDefinition]:
        """Get specific tools by their names"""
        return [self._tools[name] for name in names if name in self._tools]


# Global tool registry instance
tool_registry = ToolRegistry()
