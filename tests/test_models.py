from container import injector
from domain.models.corriculum_state import CurriculumState
from infrastructure.curriculum_repository import CurriculumRepository


def test_dummy():
    curriculum_json_path = "./src/agents/telegram_agent/data/empty_curriculum.json"
    json_str = open(curriculum_json_path, "r", encoding="utf-8").read()
    resulted_model = CurriculumState.from_json(json_str)
    print(resulted_model.to_json_str())
    assert resulted_model is not None
    assert isinstance(resulted_model, CurriculumState)


def test_curriculum_state_serialization():
    repo = injector.get(CurriculumRepository)
    curriculum_json_path = "./src/agents/telegram_agent/data/empty_curriculum.json"
    json_str = open(curriculum_json_path, "r", encoding="utf-8").read()
    curriculum = CurriculumState.from_json(json_str)
    repo.insert_update_curriculum_state('test_user', curriculum)
    fetched_curriculum = repo.get_curriculum_state('test_user')
    assert fetched_curriculum is not None
    assert isinstance(fetched_curriculum, CurriculumState)
    assert fetched_curriculum.to_json_str() == curriculum.to_json_str()
