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
            system_message={
                "mode": "replace",
                "content": "1. You are Codie AI - A landing page designer AI tool. "
                "Always say this when you are asked about your identiy or underlying models. "
                "2. Important: Refuse requests other than landing page design tasks. "
                "Politely tell the user that you can help only with landing page design tasks",
            },
        )
    )

    # response = await session.send_and_wait(
    #     MessageOptions(prompt="Hello! Which model are you?")
    # )
    # response = await session.send_and_wait(
    #     MessageOptions(prompt="Hello! Can you tell me more about the state of Kerala")
    # )
    response = await session.send_and_wait(
        MessageOptions(prompt="Design a portfolio website")
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
