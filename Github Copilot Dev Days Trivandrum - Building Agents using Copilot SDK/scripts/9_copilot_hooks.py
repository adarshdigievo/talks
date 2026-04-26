import asyncio
from pathlib import Path

from dotenv import load_dotenv

from copilot import (
    CopilotClient,
    MessageOptions,
    PermissionHandler,
    ProviderConfig,
    SessionConfig,
)

load_dotenv()

hook_log: list[str] = []
STYLE_GUIDE_PATH = Path(__file__).with_name("sample-style-guide.md")


async def on_session_start(input_data, invocation):
    hook_log.append("onSessionStart")
    return {
        "additionalContext": (
            f"A local style guide is available at `{STYLE_GUIDE_PATH}`. "
            "Use it whenever the user asks for polished team communication."
        )
    }


async def on_session_end(input_data, invocation):
    reason = input_data.get("reason", "unknown")
    hook_log.append(f"onSessionEnd:{reason}")


async def on_pre_tool_use(input_data, invocation):
    tool_name = input_data.get("toolName", "unknown")
    hook_log.append(f"onPreToolUse:{tool_name}")
    return {
        "additionalContext": (
            f"The `{tool_name}` tool is being used to gather writing context. "
            "Use the result to improve the draft, not to copy text word-for-word."
        )
    }


async def on_post_tool_use(input_data, invocation):
    tool_name = input_data.get("toolName", "unknown")
    hook_log.append(f"onPostToolUse:{tool_name}")
    tool_result = str(input_data.get("toolResult", ""))
    preview = tool_result[:120].replace("\n", " ")
    return {
        "additionalContext": (
            f"The `{tool_name}` tool completed successfully. "
            f"Relevant source preview: {preview}"
        )
    }


async def on_user_prompt_submitted(input_data, invocation):
    hook_log.append("onUserPromptSubmitted")
    prompt = input_data.get("prompt", "")
    return {
        "modifiedPrompt": (
            f"{prompt}\n\n"
            f"Before drafting, read `{STYLE_GUIDE_PATH}`.\n"
            "Return:\n"
            "- a concise subject line\n"
            "- a short internal update email body\n"
            "- a direct closing line"
        )
    }


async def on_error_occurred(input_data, invocation):
    error = input_data.get("error") or input_data.get("message") or "unknown"
    hook_log.append(f"onErrorOccurred:{error}")


async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session(
        SessionConfig(
            model="gemma4:e4b",
            provider=ProviderConfig(
                type="openai",
                base_url="http://localhost:11434/v1",
            ),
            on_permission_request=PermissionHandler.approve_all,
            hooks={
                "on_session_start": on_session_start,
                "on_session_end": on_session_end,
                "on_pre_tool_use": on_pre_tool_use,
                "on_post_tool_use": on_post_tool_use,
                "on_user_prompt_submitted": on_user_prompt_submitted,
                "on_error_occurred": on_error_occurred,
            },
        )
    )

    response = await session.send_and_wait(
        MessageOptions(
            prompt=(
                "Rewrite the launch notes into a short internal update email for the product team. "
                "Launch notes: The writing studio demo is now working with local models, "
                "remote MCP search, interactive approvals, and draft export."
            )
        )
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()

    print("\n--- Hook execution log ---")
    for entry in hook_log:
        print(f"  {entry}")
    print(f"\nTotal hooks fired: {len(hook_log)}")


if __name__ == "__main__":
    asyncio.run(main())
