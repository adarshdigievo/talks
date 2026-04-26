import asyncio
from dotenv import load_dotenv
from copilot import (
    CopilotClient,
    SessionConfig,
    MessageOptions,
    PermissionHandler,
    ProviderConfig,
)

load_dotenv()


async def main():
    client = CopilotClient()

    await client.start()
    session = await client.create_session(
        SessionConfig(
            model="gemma4:e4b",
            provider=ProviderConfig(
                type="openai", base_url="http://localhost:11434/v1"
            ),
            on_permission_request=PermissionHandler.approve_all,
        )
    )

    response = await session.send_and_wait(
        MessageOptions(prompt="Hello! Which model are you")
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
