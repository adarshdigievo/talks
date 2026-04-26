import asyncio
from pathlib import Path

from copilot import CopilotClient, MessageOptions, PermissionHandler, SessionConfig


async def main():
    client = CopilotClient()
    await client.start()

    skills_dir = Path(__file__).resolve().parent / "sample-skills"

    session = await client.create_session(
        SessionConfig(
            model="gpt-5-mini",
            on_permission_request=PermissionHandler.approve_all,
            skill_directories=[str(skills_dir)],
            system_message={
                "mode": "replace",
                "content": "You are an AI writing assistant. When asked to write/rewrite/edit any text, use "
                "the humanizer skill to rewrite so it sounds less AI-like "
                "and more natural while keeping the meaning",
            },
        )
    )

    response = await session.send_and_wait(
        MessageOptions(
            prompt=(
                "Rewrite this paragraph: AI writing assistants serve as a powerful testament "
                "to the evolving landscape of communication, helping teams unlock productivity, "
                "streamline collaboration, and deliver impactful messaging at scale."
            )
        )
    )

    if response:
        print(response.data.content)
    else:
        print("Model failed to respond")

    print(f"\nHumanizer skill directory configured: {skills_dir}")

    await session.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
