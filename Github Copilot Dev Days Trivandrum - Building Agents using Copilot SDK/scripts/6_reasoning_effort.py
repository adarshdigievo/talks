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
            model="gpt-5-mini",
            # reasoning_effort="low",
            reasoning_effort="high",
            on_permission_request=PermissionHandler.approve_all,
            system_message={
                "mode": "replace",
                "content": "1. You are a writing assistant AI. You will accept inputs from user, then correct its grammar and improve the overall impact of the text.",
            },
        )
    )

    user_prompt = "Rewrite this: I am talking at the Github Copilot Dev Days event conducted by TriPy"

    while user_prompt != "quit":

        response = await session.send_and_wait(MessageOptions(prompt=user_prompt))

        if response:
            print(f"Reasoning: {response.data.reasoning_text}")
            print(f"Response: {response.data.content}")
        else:
            print("Model failed to respond")

        user_prompt = input(">> (`quit` to exit): ")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
