from pathlib import Path

from google.adk import Agent

from agents.telegram_agent.tools.curriculum import save_curriculum_state

system_prompt_path = Path(__file__).parent / "prompts" / "system_prompt.md"
system_prompt = system_prompt_path.read_text(encoding='utf-8')
system_prompt = system_prompt.replace("{CURRICULUM_JSON_STATE}", "{}")

root_agent = Agent(
    name="agents",
    model="gemini-2.5-flash",
    description=(
        " Agent."
    ),
    instruction=(
        system_prompt
    ),
    tools=[save_curriculum_state],
)
