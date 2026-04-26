import asyncio
from pathlib import Path

from dotenv import load_dotenv

from copilot import (
    CopilotClient,
    MessageOptions,
    PermissionRequestResult,
    ProviderConfig,
    SessionConfig,
)

load_dotenv()

permission_log: list[str] = []
OUTPUT_PATH = Path(__file__).with_name("permission-demo-output.md")


def describe_permission_request(request) -> str:
    kind = request.kind.value
    if kind == "write":
        return f"write `{getattr(request, 'file_name', None) or OUTPUT_PATH}`"
    if kind == "read":
        return f"read `{getattr(request, 'path', 'unknown path')}`"
    if kind == "shell":
        return f"run `{getattr(request, 'full_command_text', 'unknown command')}`"
    if kind == "mcp":
        server = getattr(request, "server_name", None) or "mcp"
        tool = getattr(request, "tool_name", None) or "unknown"
        return f"use `{server}:{tool}`"
    if kind == "custom-tool":
        return f"use custom tool `{getattr(request, 'tool_name', 'unknown')}`"
    return kind


async def log_permission(request, invocation):
    description = describe_permission_request(request)
    answer = input(f"Approve this request? {description} [y/N]: ").strip().lower()
    approved = answer in {"y", "yes"}
    permission_log.append(f"{'approved' if approved else 'denied'}:{description}")
    return PermissionRequestResult(
        kind="approved" if approved else "denied-interactively-by-user"
    )


async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session(
        SessionConfig(
            model="gemma4:26b",
            provider=ProviderConfig(
                type="openai",
                base_url="http://localhost:11434/v1",
            ),
            on_permission_request=log_permission,
        )
    )

    response = await session.send_and_wait(
        MessageOptions(
            prompt=(
                "Write a short release-note summary about a writing assistant demo and save it "
                f"to `{OUTPUT_PATH}` as Markdown using the write tool. "
                "If the write permission is denied, explain that the save was blocked."
            )
        )
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()

    print("\n--- Permission request log ---")
    for entry in permission_log:
        print(f"  {entry}")
    print(f"\nTotal permission requests: {len(permission_log)}")


if __name__ == "__main__":
    asyncio.run(main())
