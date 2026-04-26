import asyncio
from copilot import CopilotClient, MessageOptions, PermissionHandler, SessionConfig, ProviderConfig


async def main():
    client = CopilotClient()
    await client.start()

    session_config = SessionConfig(
        model="gemma4:e4b",
        provider=ProviderConfig(
            type="openai",
            base_url="http://localhost:11434/v1",
        ),
        on_permission_request=PermissionHandler.approve_all,
        available_tools=[],
        system_message={
            "mode": "replace",
            "content": (
                "You are a writing assistant. Improve short drafts clearly and concisely. "
                "When the time MCP server is available, append the current writing date and time."
            ),
        },
        mcp_servers={
            "time": {
                "type": "http",
                "url": "https://mcp.time.mcpcentral.io",
                "tools": ["*"],
            }
        },
    )

    session = await client.create_session(session_config)

    response = await session.send_and_wait(
        MessageOptions(
            prompt=(
                "Rewrite this sentence to sound more natural and append the current writing "
                "date and time using the time MCP tool: "
                "'I am drafting this note for today's developer workshop.'"
            )
        )
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
