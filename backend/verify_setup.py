"""
Startup verification script for the multi-provider LLM system.

Run this script to verify your configuration before starting the server.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import settings


def check_provider_config():
    """Check if the selected provider is properly configured"""
    print("🔍 Checking LLM Provider Configuration...\n")

    provider = settings.LLM_PROVIDER
    print(f"Selected Provider: {provider}")

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            print("❌ ERROR: OPENAI_API_KEY is not set")
            return False
        print(f"✅ OpenAI API Key: {'*' * 20}{settings.OPENAI_API_KEY[-4:]}")
        print(f"✅ Model: {settings.OPENAI_MODEL}")

    elif provider == "groq":
        if not settings.GROQ_API_KEY:
            print("❌ ERROR: GROQ_API_KEY is not set")
            return False
        print(f"✅ Groq API Key: {'*' * 20}{settings.GROQ_API_KEY[-4:]}")
        print(f"✅ Model: {settings.GROQ_MODEL}")

    elif provider == "gemini":
        if not settings.GEMINI_API_KEY:
            print("❌ ERROR: GEMINI_API_KEY is not set")
            return False
        print(f"✅ Gemini API Key: {'*' * 20}{settings.GEMINI_API_KEY[-4:]}")
        print(f"✅ Model: {settings.GEMINI_MODEL}")

    else:
        print(f"❌ ERROR: Unsupported provider '{provider}'")
        print("   Supported providers: openai, groq, gemini")
        return False

    return True


def check_database_config():
    """Check database configuration"""
    print("\n🔍 Checking Database Configuration...\n")

    if not settings.DATABASE_URL:
        print("❌ ERROR: DATABASE_URL is not set")
        return False

    # Mask password in URL
    db_url = settings.DATABASE_URL
    if "@" in db_url:
        parts = db_url.split("@")
        masked = parts[0].split(":")[0] + ":****@" + parts[1]
        print(f"✅ Database URL: {masked}")
    else:
        print(f"✅ Database URL: {db_url}")

    return True


def check_auth_config():
    """Check authentication configuration"""
    print("\n🔍 Checking Authentication Configuration...\n")

    if not settings.BETTER_AUTH_SECRET:
        print("❌ ERROR: BETTER_AUTH_SECRET is not set")
        return False

    print(f"✅ Auth Secret: {'*' * 20}{settings.BETTER_AUTH_SECRET[-4:]}")
    print(f"✅ Token Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")

    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking Dependencies...\n")

    required = {
        "fastapi": "FastAPI",
        "sqlmodel": "SQLModel",
        "uvicorn": "Uvicorn",
        "openai": "OpenAI SDK",
        "groq": "Groq SDK",
        "google.generativeai": "Google Generative AI",
    }

    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            missing.append(module)

    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False

    return True


def check_tool_registry():
    """Check if tools are registered"""
    print("\n🔍 Checking Tool Registry...\n")

    try:
        from src.llm.tool_registry import tool_registry

        # Import all tool modules to trigger registration
        from src.tools import task_tools, analytics_tools, tag_tools, reminder_tools

        tools = tool_registry.get_all_tools()
        print(f"✅ Registered Tools: {len(tools)}")

        for tool in tools:
            print(f"   - {tool.name}")

        if len(tools) == 0:
            print("⚠️  WARNING: No tools registered")
            return False

        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("🚀 Phase 3 TODO AI Chatbot - Startup Verification")
    print("=" * 60)

    checks = [
        ("Dependencies", check_dependencies),
        ("Database Config", check_database_config),
        ("Auth Config", check_auth_config),
        ("Provider Config", check_provider_config),
        ("Tool Registry", check_tool_registry),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to start the server.")
        print("\nRun: uvicorn src.main:app --reload")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
