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
    json_str = """{"curriculum":{"what_is_data":{"name":"What is Data?","description":"Understanding what data means and finding it in everyday life","prerequisites":[],"difficulty":1,"key_concepts":["observation","recording","examples","information"],"student_progress":{"status":"completed","mastery_level":1.0,"attempts":4,"last_interaction":"2025-11-23T10:00:00Z","struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}},"data_types":{"name":"Types of Data","description":"Numbers, categories, text - different kinds of information","prerequisites":["what_is_data"],"difficulty":2,"key_concepts":["numerical","categorical","text","dates","boolean"],"student_progress":{"status":"not_started","mastery_level":0.0,"attempts":0,"last_interaction":null,"struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}},"collecting_organizing":{"name":"Collecting and Organizing Data","description":"How to gather information and put it in order","prerequisites":["data_types"],"difficulty":2,"key_concepts":["tables","rows","columns","sorting","grouping"],"student_progress":{"status":"not_started","mastery_level":0.0,"attempts":0,"last_interaction":null,"struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}},"visualizing_data":{"name":"Visualizing Data","description":"Making charts and graphs to see patterns clearly","prerequisites":["collecting_organizing"],"difficulty":3,"key_concepts":["bar_charts","line_graphs","pie_charts","axes","labels"],"student_progress":{"status":"not_started","mastery_level":0.0,"attempts":0,"last_interaction":null,"struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}},"finding_patterns":{"name":"Finding Patterns and Trends","description":"Spotting what's typical, what's changing, and what's unusual","prerequisites":["visualizing_data"],"difficulty":3,"key_concepts":["trends","mean","median","mode","outliers","range"],"student_progress":{"status":"not_started","mastery_level":0.0,"attempts":0,"last_interaction":null,"struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}},"making_predictions":{"name":"Making Predictions from Data","description":"Using patterns to make informed guesses about what might happen","prerequisites":["finding_patterns"],"difficulty":4,"key_concepts":["correlation","causation","prediction","probability","testing_ideas"],"student_progress":{"status":"not_started","mastery_level":0.0,"attempts":0,"last_interaction":null,"struggle_signals":{"help_requests":0,"error_count":0,"confusion_indicators":0}}}},"student_profile":{"interests":[],"learning_velocity":1.0,"active_concepts":[]},"metadata":{"schema_version":"1.0","created_at":"2025-11-23T10:00:00Z","last_updated":"2025-11-23T10:00:00Z"}}"""
    curriculum = CurriculumState.from_json(json_str)
    repo.insert_update_curriculum_state('test_user', curriculum)
    fetched_curriculum = repo.get_curriculum_state('test_user')
    assert fetched_curriculum is not None
    assert isinstance(fetched_curriculum, CurriculumState)
    assert fetched_curriculum.to_json_str() == curriculum.to_json_str()
