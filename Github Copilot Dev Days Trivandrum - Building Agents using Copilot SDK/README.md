# Building Agents using Copilot SDK

## Setup

Install `uv` first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the project requirements from `pyproject.toml`:

```bash
uv sync
```

Run any demo script with `uv run python`, for example:

```bash
uv run python scripts/1_llm.py
```

Some demos use a local OpenAI-compatible model endpoint at `http://localhost:11434/v1`, so start Ollama, LM Studio, or another compatible server before running those scripts.

## Scripts

`scripts/0_setup.md` captures the manual setup checklist for the workshop: install and log in to GitHub Copilot CLI, open the CLI in the working directory, use slash commands for models and tools, and install a local model runner such as Ollama or LM Studio for demos that talk to local models.

`scripts/1_llm.py` is the smallest Copilot SDK example. It starts a `CopilotClient`, creates a `gpt-5-mini` session with permissive approvals, sends a simple "Which model are you" prompt, prints the response, and disconnects the session.

`scripts/2_local_llm.py` shows how to use the SDK with a local OpenAI-compatible provider. It loads environment variables, points the provider at `http://localhost:11434/v1`, selects a local `gemma4:e4b` model, sends the same identity prompt, and prints the local model response.

`scripts/3_system_prompt.py` demonstrates replacing the default system message. The session is configured as "Codie AI", a landing-page-design-only assistant, then the script sends a portfolio website request so you can see how the custom identity and task boundary steer the model.

`scripts/4_session_history.py` demonstrates the problem with recreating sessions in a loop. Each user prompt is sent to a newly created writing-assistant session, so responses work one at a time but conversation history is not preserved across turns.

`scripts/5_session_history_fixed.py` keeps one session alive for the whole input loop. Because each prompt goes through the same writing-assistant session, the model can retain session context until the user types `quit` and the script disconnects.

`scripts/6_reasoning_effort.py` demonstrates configuring reasoning effort for `gpt-5-mini`. It sets `reasoning_effort="high"`, sends rewrite prompts in a loop, and prints both the reasoning text and final response so the difference is visible during the demo.

`scripts/7_custom_tool.py` defines a typed custom tool with Pydantic and `define_tool`. The model is instructed to call `append_suffix` exactly once, the tool logs its parameters, and the final answer proves the tool result was used by appending `[custom-tool-applied]`.

`scripts/8_copilot_perms.py` demonstrates interactive permission handling. It asks the user to approve or deny read, write, shell, MCP, or custom-tool requests, prompts the model to write release notes to `permission-demo-output.md`, then prints a permission request log.

`scripts/9_copilot_hooks.py` demonstrates lifecycle and tool hooks. The script adds context at session start, modifies the submitted prompt to use `sample-style-guide.md`, records pre- and post-tool events, handles errors, and prints the hook execution log after disconnecting.

`scripts/10_mcp.py` shows how to attach an MCP server to a Copilot SDK session. It configures the remote time MCP server, asks the writing assistant to rewrite a sentence, and instructs it to append the current date and time using the MCP tool.

`scripts/11_skills.py` demonstrates loading local skills from `scripts/sample-skills`. The session points at the sample skill directory, instructs the assistant to use the humanizer skill for writing edits, rewrites a paragraph, and prints which skill directory was configured.
