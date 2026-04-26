import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from copilot import (
    CopilotClient,
    MessageOptions,
    PermissionHandler,
    ProviderConfig,
    SessionConfig,
    define_tool,
)

load_dotenv()


class AppendSuffixParams(BaseModel):
    text: str = Field(description="The main model output before the suffix is added.")
    suffix: str = Field(description="The exact suffix to append to the text.")


@define_tool("append_suffix", description="Appends a fixed suffix to a text result.")
def append_suffix(params: AppendSuffixParams, invocation) -> str:
    print(f"Tool is getting called: {params.text=}, {params.suffix=} \n\n")
    return f"{params.text}{params.suffix}"


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
            on_permission_request=PermissionHandler.approve_all,
            tools=[append_suffix],
            system_message={
                "mode": "replace",
                "content": (
                    "You are a concise writing helper. "
                    "Always call the `append_suffix` tool exactly once before returning the final answer. "
                    "First draft a short response. Then pass that response into the tool. "
                    "Append this exact suffix: ' [custom-tool-applied]'. "
                    "Return only the tool result."
                ),
            },
        )
    )

    response = await session.send_and_wait(
        MessageOptions(
            prompt="Write one sentence about why editing tools are useful for writers."
        )
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
