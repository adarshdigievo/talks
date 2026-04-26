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

    user_prompt = "Rewrite this: I am talking at the Github Copilot Dev Days event conducted by TriPy"

    while user_prompt != "quit":

        session = await client.create_session(
            SessionConfig(
                model="gemma4:e4b",
                provider=ProviderConfig(
                    type="openai", base_url="http://localhost:11434/v1"
                ),
                on_permission_request=PermissionHandler.approve_all,
                system_message={
                    "mode": "replace",
                    "content": "1. You are a writing assistant AI. "
                    "You will accept inputs from user, "
                    "then correct its grammar and improve the overall impact "
                    "of the text.",
                },
            )
        )

        response = await session.send_and_wait(MessageOptions(prompt=user_prompt))

        if response:
            print(response.data.content)
        else:
            print("Model failed to respond")

        await session.disconnect()

        user_prompt = input(">> (`quit` to exit): ")


if __name__ == "__main__":
    asyncio.run(main())
