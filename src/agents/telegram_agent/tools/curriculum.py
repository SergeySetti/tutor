from container import injector
from infrastructure.curriculum_repository import CurriculumRepository


def save_curriculum_state(curriculum_stat_json: str) -> dict:
    """A tool to save the curriculum state.

    Args:
        curriculum_stat_json: A JSON string representing the curriculum state.
    Returns: Result of the operation validation and saving.
    """

    try:
        curriculum_repository = injector.get(CurriculumRepository)
        results = curriculum_repository.save_state(curriculum_stat_json)
    except Exception as e:
        return {
            "status": "error",
            "message": e,
        }

    return {"status": "success", "results": results}

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

def reset_curriculum_state(user_id: str) -> dict:
    """A tool to reset the curriculum state.

    Returns: Result of the operation validation and resetting.
    """

    try:
        # Replace with actual resetting logic
        results = "Curriculum state has been reset."
    except Exception as e:
        return {
            "status": "error",
            "message": e,
        }

    return {"status": "success", "results": results}
