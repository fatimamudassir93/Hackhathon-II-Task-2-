from typing import Optional
from src.config import settings
from chatbot.llm.base import BaseLLMProvider
from chatbot.llm.openai_provider import OpenAIProvider
from chatbot.llm.groq_provider import GroqProvider
from chatbot.llm.gemini_provider import GeminiProvider


class ProviderFactory:
    """Factory for creating LLM provider instances"""

    @staticmethod
    def create_provider(
        provider_name: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> BaseLLMProvider:
        """
        Create an LLM provider instance

        Args:
            provider_name: Provider name ("openai", "groq", "gemini"). Defaults to settings.LLM_PROVIDER
            api_key: API key for the provider. Defaults to provider-specific key from settings
            model: Model name. Defaults to provider-specific model from settings

        Returns:
            BaseLLMProvider instance

        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider_name = provider_name or settings.LLM_PROVIDER

        if provider_name == "openai":
            api_key = api_key or settings.OPENAI_API_KEY
            model = model or settings.OPENAI_MODEL
            if not api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            return OpenAIProvider(api_key=api_key, model=model)

        elif provider_name == "groq":
            api_key = api_key or settings.GROQ_API_KEY
            model = model or settings.GROQ_MODEL
            if not api_key:
                raise ValueError("GROQ_API_KEY is required for Groq provider")
            return GroqProvider(api_key=api_key, model=model)

        elif provider_name == "gemini":
            api_key = api_key or settings.GEMINI_API_KEY
            model = model or settings.GEMINI_MODEL
            if not api_key:
                raise ValueError("GEMINI_API_KEY is required for Gemini provider")
            return GeminiProvider(api_key=api_key, model=model)

        else:
            raise ValueError(
                f"Unsupported provider: {provider_name}. "
                f"Supported providers: openai, groq, gemini"
            )


# Convenience function
def get_default_provider() -> BaseLLMProvider:
    """Get the default LLM provider from settings"""
    return ProviderFactory.create_provider()
