from pathlib import Path

from google.adk.agents import Agent

from agents.telegram_agent.tools.curriculum import save_curriculum_state

system_prompt_path = Path(__file__).parent / "prompts" / "system_prompt.md"
system_prompt = system_prompt_path.read_text(encoding='utf-8')

root_agent = Agent(
    name="telegram_agent",
    model="gemini-2.5-flash",
    description=(
        "DataScience Agent Tutor for kids."
    ),
    instruction=(
        system_prompt
    ),
    tools=[save_curriculum_state],
)
