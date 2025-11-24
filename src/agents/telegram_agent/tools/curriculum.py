from google.adk.tools import ToolContext
from pydantic import ValidationError

from container import injector
from domain.models.corriculum_state import CurriculumState
from infrastructure.curriculum_repository import CurriculumRepository


def save_curriculum_state(tool_context: ToolContext, curriculum_state_json: str):
    """A tool to save the curriculum state. Structure must be consistent, so that tool validat data before saving.

    Args:
    :param curriculum_state_json: A JSON string representing the curriculum state. Keep JSON structure but update values as needed.
    :param tool_context:

    Returns: Result of the operation validation and saving.
    """

    try:
        curriculum_repository = injector.get(CurriculumRepository)
        print("SAVING CURRICULUM STATE:")
        print(curriculum_state_json)
        curriculum = CurriculumState.from_json(curriculum_state_json)
        curriculum_repository.insert_update_curriculum_state(tool_context.state['user_name'], curriculum)
    except Exception as e:
        return {
            "status": "error",
            "message": e,
        }

    return {"status": "success", "results": "Curriculum state has been saved."}


def load_curriculum_state(user_id: str) -> dict:
    """A tool to load the curriculum state.

    Returns: The curriculum state as a JSON string.
    """

    try:
        curriculum_state_json = "{}"  # Replace with actual loading logic
    except Exception as e:
        return {
            "status": "error",
            "message": e,
        }

    return {"status": "success", "curriculum_state": curriculum_state_json}


def reset_curriculum_state(user_name: str) -> dict:
    """A tool to reset the curriculum state. Use only when necessary. For example, when the curriculum is or not existing for the current user.

    Returns: Result of the operation.
    """

    try:
        initial_curriculum_json_path = "./src/agents/telegram_agent/data/empty_curriculum.json"
        with open(initial_curriculum_json_path, "r", encoding="utf-8") as file:
            initial_curriculum_json = file.read()
            curriculum_repository = injector.get(CurriculumRepository)
            curriculum_repository.insert_update_curriculum_state(user_name, initial_curriculum_json)
        results = "Curriculum state has been reset."
    except Exception as e:
        return {
            "status": "error",
            "message": e,
        }

    return {"status": "success", "results": results}
